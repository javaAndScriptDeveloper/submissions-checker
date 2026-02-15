"""Database migration runner using raw SQL files."""

import hashlib
import logging
import time
from pathlib import Path
from typing import List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from submissions_checker.core.database import get_engine

logger = logging.getLogger(__name__)


class Migration:
    """Represents a single SQL migration file."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.name = file_path.stem  # "002_create_outbox_messages"
        self.sequence = int(file_path.stem.split("_")[0])  # 2
        self.sql = file_path.read_text(encoding="utf-8")
        self.checksum = self._calculate_checksum()

    def _calculate_checksum(self) -> str:
        """Calculate SHA-256 checksum of normalized SQL."""
        normalized = "\n".join(
            line.strip()
            for line in self.sql.splitlines()
            if line.strip() and not line.strip().startswith("--")
        )
        return hashlib.sha256(normalized.encode()).hexdigest()


async def _ensure_migrations_table(engine: AsyncEngine) -> None:
    """Create schema_migrations table if it doesn't exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        id SERIAL PRIMARY KEY,
        migration_name VARCHAR(255) NOT NULL UNIQUE,
        checksum VARCHAR(64) NOT NULL,
        executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        execution_time_ms INTEGER,
        success BOOLEAN NOT NULL DEFAULT TRUE
    );
    """

    async with engine.begin() as conn:
        await conn.execute(text(create_table_sql))

    logger.debug("schema_migrations table ensured")


async def _get_executed_migrations(engine: AsyncEngine) -> dict[str, str]:
    """Get mapping of migration_name -> checksum."""
    query = "SELECT migration_name, checksum FROM schema_migrations WHERE success = TRUE"
    async with engine.connect() as conn:
        result = await conn.execute(text(query))
        return {row[0]: row[1] for row in result}


def _discover_migrations(migrations_dir: Path) -> List[Migration]:
    """Find and sort all SQL migration files."""
    sql_files = sorted(migrations_dir.glob("*.sql"))
    migrations = [Migration(f) for f in sql_files]
    migrations.sort(key=lambda m: m.sequence)
    return migrations


async def _execute_migration(engine: AsyncEngine, migration: Migration) -> None:
    """Execute migration in a transaction and record success."""
    start_time = time.time()

    async with engine.begin() as conn:
        # Get underlying asyncpg connection to execute multiple statements
        # asyncpg doesn't support multiple statements in prepared statements,
        # so we need to use the raw connection
        raw_conn = await conn.get_raw_connection()
        await raw_conn.driver_connection.execute(migration.sql)

        execution_time_ms = int((time.time() - start_time) * 1000)
        await conn.execute(
            text(
                "INSERT INTO schema_migrations "
                "(migration_name, checksum, execution_time_ms, success) "
                "VALUES (:name, :checksum, :execution_time_ms, TRUE)"
            ),
            {"name": migration.name, "checksum": migration.checksum, "execution_time_ms": execution_time_ms}
        )

    logger.info(f"migration completed: {migration.name} ({execution_time_ms}ms)")


async def run_migrations() -> None:
    """
    Run all pending database migrations.

    Process:
    1. Ensure schema_migrations table exists
    2. Discover all SQL files in migrations/sql/
    3. Check which migrations executed
    4. Execute pending migrations in sequence
    5. Validate checksums for executed migrations
    """
    logger.info("starting migration runner")

    engine = get_engine()
    await _ensure_migrations_table(engine)

    # Find migrations directory: migrations/sql/
    project_root = Path(__file__).parent.parent.parent.parent
    migrations_dir = project_root / "migrations" / "sql"

    if not migrations_dir.exists():
        migrations_dir.mkdir(parents=True, exist_ok=True)
        logger.info("no migrations to run")
        return

    migrations = _discover_migrations(migrations_dir)
    if not migrations:
        logger.info("no migrations found")
        return

    logger.info(f"discovered {len(migrations)} migration file(s)")

    executed = await _get_executed_migrations(engine)

    pending_count = 0
    for migration in migrations:
        if migration.name in executed:
            # Verify checksum hasn't changed
            if executed[migration.name] != migration.checksum:
                raise RuntimeError(
                    f"Migration checksum mismatch for '{migration.name}'. "
                    f"File was modified after execution."
                )
            logger.debug(f"skipping: {migration.name}")
        else:
            logger.info(f"executing migration: {migration.name}")
            await _execute_migration(engine, migration)
            pending_count += 1

    if pending_count > 0:
        logger.info(f"executed {pending_count} new migration(s)")
    else:
        logger.info("all migrations up to date")
