"""
Database base configuration and model imports.

This module imports all models to ensure they are registered with SQLAlchemy
and available for Alembic auto-detection.
"""

from submissions_checker.db.models.base import Base

# Import all models for Alembic auto-detection
from submissions_checker.db.models.outbox import OutboxMessage

# Skeleton models (not yet implemented - uncomment when ready)
# from submissions_checker.db.models.submission import Submission
# from submissions_checker.db.models.user import User

__all__ = [
    "Base",
    "OutboxMessage",
    # "User",
    # "Submission",
]
