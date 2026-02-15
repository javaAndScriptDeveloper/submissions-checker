"""Database migration runner using Alembic programmatically."""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)


def _run_migrations_sync() -> None:
    """Synchronous function that runs Alembic migrations."""
    # Get the project root (where alembic.ini is located)
    # This file is at: src/submissions_checker/core/migrations.py
    # So project root is 3 levels up
    project_root = Path(__file__).parent.parent.parent.parent
    alembic_ini_path = project_root / "alembic.ini"

    if not alembic_ini_path.exists():
        raise FileNotFoundError(f"alembic.ini not found at {alembic_ini_path}")

    # Create Alembic config
    alembic_cfg = Config(str(alembic_ini_path))

    # Set the script location (migrations directory)
    migrations_dir = project_root / "migrations"
    alembic_cfg.set_main_option("script_location", str(migrations_dir))

    # Run upgrade to head
    command.upgrade(alembic_cfg, "head")


async def run_migrations() -> None:
    """Run all pending database migrations using Alembic (async wrapper)."""
    logger.info("Running database migrations")

    # Run migrations in a thread pool to avoid asyncio.run() conflicts
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        try:
            await loop.run_in_executor(executor, _run_migrations_sync)
            logger.info("Database migrations completed successfully")
        except Exception as e:
            logger.error(f"Database migration failed: {e}")
            raise
