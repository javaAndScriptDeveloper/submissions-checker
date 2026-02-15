"""Submission schemas (skeleton - to be implemented)."""

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    """Schema for creating a submission (skeleton)."""

    # TODO: Add fields
    # repository_url: str
    # pull_request_number: int
    # commit_sha: str
    pass


class SubmissionResponse(BaseModel):
    """Schema for submission response (skeleton)."""

    # TODO: Add fields
    # id: int
    # user_id: int
    # status: str
    # created_at: datetime
    pass
