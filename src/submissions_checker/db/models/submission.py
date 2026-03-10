"""Student submission tracking for PR-based assignments."""

from sqlalchemy import String, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from submissions_checker.db.models.base import Base, TimestampMixin
from submissions_checker.db.models.enums import SubmissionStatus


class Submission(Base, TimestampMixin):
    """Student submission tracking for PR-based assignments."""

    __tablename__ = "submissions"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Pull request information
    pr_number: Mapped[int] = mapped_column(Integer, nullable=False)

    # Repository information
    fork_full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    base_full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Git information
    head_ref: Mapped[str] = mapped_column(String(255), nullable=False)
    head_sha: Mapped[str] = mapped_column(String(255), nullable=False)

    # Student information
    github_username: Mapped[str] = mapped_column(String(255), nullable=False)

    # Local storage path (set by PULL task)
    repository_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Processing status
    status: Mapped[SubmissionStatus] = mapped_column(
        SQLEnum(
            SubmissionStatus,
            name="submission_status",
            native_enum=True,
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=SubmissionStatus.PENDING,
    )

    # Results (populated by REVIEW and TEST tasks)
    test_results: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ai_review: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Google Form link (populated by GENERATE_QUIZ task)
    quiz_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    # Quiz scores (populated by quiz-submission callback)
    quiz_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quiz_max_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
