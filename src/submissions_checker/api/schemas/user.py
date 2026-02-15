"""User schemas (skeleton - to be implemented)."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Schema for creating a user (skeleton)."""

    # TODO: Add fields
    # email: str
    # username: str
    # password: str | None = None
    pass


class UserResponse(BaseModel):
    """Schema for user response (skeleton)."""

    # TODO: Add fields
    # id: int
    # email: str
    # username: str
    # is_active: bool
    # created_at: datetime
    pass
