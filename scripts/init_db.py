#!/usr/bin/env python3
"""Database initialization script."""

import asyncio
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sqlalchemy.ext.asyncio import create_async_engine

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import configure_logging, get_logger
from submissions_checker.db.base import Base

configure_logging()
logger = get_logger(__name__)


async def init_database() -> None:
    """Initialize the database by creating all tables."""
    settings = get_settings()
    logger.info("initializing_database", url=str(settings.database_url))

    # Create async engine
    engine = create_async_engine(str(settings.database_url), echo=True)

    try:
        # Create all tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("database_initialized_successfully")
        print("✓ Database initialized successfully")

    except Exception as e:
        logger.error("database_initialization_failed", error=str(e))
        print(f"✗ Database initialization failed: {e}")
        sys.exit(1)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_database())
