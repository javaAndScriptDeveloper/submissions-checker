"""Submission model (skeleton - to be implemented)."""

from submissions_checker.db.models.base import Base, TimestampMixin


class Submission(Base, TimestampMixin):
    """Submission model - skeleton for future implementation."""

    __tablename__ = "submissions"

    # TODO: Implement submission model fields
    # - id: Submission ID
    # - user_id: Foreign key to User
    # - repository_url: GitHub repository URL
    # - pull_request_number: PR number
    # - commit_sha: Commit SHA
    # - status: Submission status (pending, running, completed, failed)
    # - test_results: Test execution results
    # - ai_review: AI-generated code review
    # - etc.
    pass
