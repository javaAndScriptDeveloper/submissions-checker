"""Health check endpoints."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from submissions_checker.api.dependencies import DBSession
from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Basic health check endpoint.

    Returns:
        Simple status indicating the service is running
    """
    return {"status": "healthy"}


@router.get("/health/ready")
async def readiness_check(db: DBSession) -> dict[str, str]:
    """
    Readiness check with database connectivity test.

    Args:
        db: Database session

    Returns:
        Status with database connectivity information

    Raises:
        HTTPException: If database is not accessible
    """
    try:
        # Test database connectivity
        result = await db.execute(text("SELECT 1"))
        result.scalar()

        logger.info("readiness_check_passed")
        return {"status": "ready", "database": "connected"}

    except Exception as e:
        logger.error("readiness_check_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from e
