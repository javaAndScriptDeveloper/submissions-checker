"""User management endpoints (skeleton)."""

from fastapi import APIRouter

from submissions_checker.api.dependencies import DBSession
from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("")
async def create_user(db: DBSession) -> dict[str, str]:
    """
    Create a new user (skeleton).

    TODO: Implement user creation:
    1. Validate user data with Pydantic schema
    2. Check if user already exists
    3. Hash password if applicable
    4. Create user in database
    5. Return user response

    Args:
        db: Database session

    Returns:
        Created user data
    """
    logger.info("create_user_called")

    # TODO: Implement user creation
    # user = User(email=user_data.email, username=user_data.username)
    # db.add(user)
    # await db.commit()
    # await db.refresh(user)

    return {"status": "not_implemented", "message": "User creation not yet implemented"}


@router.get("/{user_id}")
async def get_user(user_id: int, db: DBSession) -> dict[str, str]:
    """
    Get user by ID (skeleton).

    TODO: Implement user retrieval:
    1. Query user by ID
    2. Return 404 if not found
    3. Return user data

    Args:
        user_id: User ID
        db: Database session

    Returns:
        User data
    """
    logger.info("get_user_called", user_id=user_id)

    # TODO: Implement user retrieval
    # result = await db.execute(select(User).where(User.id == user_id))
    # user = result.scalar_one_or_none()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    return {"status": "not_implemented", "message": "User retrieval not yet implemented"}
