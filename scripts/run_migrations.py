#!/usr/bin/env python3
"""Migration runner script."""

import subprocess
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


def run_migrations() -> None:
    """Run Alembic migrations to upgrade database to latest version."""
    settings = get_settings()
    logger.info("running_migrations", environment=settings.environment)

    try:
        # Run alembic upgrade head
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            check=True,
        )

        logger.info("migrations_completed_successfully")
        print("✓ Migrations completed successfully")
        if result.stdout:
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        logger.error("migrations_failed", error=str(e), stderr=e.stderr)
        print(f"✗ Migrations failed: {e}")
        if e.stderr:
            print(e.stderr)
        sys.exit(1)

    except FileNotFoundError:
        logger.error("alembic_not_found")
        print("✗ Alembic not found. Please install dependencies first.")
        sys.exit(1)


def create_migration(message: str) -> None:
    """
    Create a new migration with autogenerate.

    Args:
        message: Migration message
    """
    logger.info("creating_migration", message=message)

    try:
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", message],
            capture_output=True,
            text=True,
            check=True,
        )

        logger.info("migration_created_successfully")
        print(f"✓ Migration created: {message}")
        if result.stdout:
            print(result.stdout)

    except subprocess.CalledProcessError as e:
        logger.error("migration_creation_failed", error=str(e))
        print(f"✗ Migration creation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        if len(sys.argv) < 3:
            print("Usage: python run_migrations.py create <message>")
            sys.exit(1)
        create_migration(sys.argv[2])
    else:
        run_migrations()
