"""Dependency injection helpers for FastAPI routes."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from submissions_checker.core.config import Settings, get_settings
from submissions_checker.core.database import get_db

# Type aliases for common dependencies
DBSession = Annotated[AsyncSession, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]
