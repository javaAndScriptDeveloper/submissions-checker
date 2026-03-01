"""Notification and result posting tasks."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from submissions_checker.core.logging import get_logger
from submissions_checker.db.models import Submission
from submissions_checker.services.github.client import GitHubClient

logger = get_logger(__name__)

_COMMENT_TEMPLATE = """\
Hi @{username}! 👋

Your lab submission has been reviewed by our AI assistant and a personalized quiz \
has been generated based on your code.

**Please complete the quiz to finish your lab submission:**
➡️ {form_url}

Good luck! The quiz is timed, so make sure you're ready before opening the link.
"""


async def execute_notify_task(db: AsyncSession, notify_data: dict) -> None:
    """Post the generated quiz link as a comment on the student's GitHub PR.

    Reads ``form_url`` from the outbox payload, formats a welcome message, and
    posts it to the pull request that triggered the submission.  No additional
    DB writes are needed — this is the terminal stage of the pipeline.

    Expected payload: ``{"submission_id": int, "form_url": str}``
    """
    submission_id = notify_data.get("submission_id")
    form_url = notify_data.get("form_url")
    logger.info(
        "execute_notify_task_started",
        submission_id=submission_id,
        form_url=form_url,
    )

    if not form_url:
        raise ValueError(
            f"No form_url in NOTIFY payload for submission {submission_id}"
        )

    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one()

    comment = _COMMENT_TEMPLATE.format(
        username=submission.github_username,
        form_url=form_url,
    )

    github = GitHubClient()
    await github.post_comment(
        repo=submission.base_full_name,
        pr_number=submission.pr_number,
        comment=comment,
    )

    logger.info(
        "execute_notify_task_completed",
        submission_id=submission_id,
        repo=submission.base_full_name,
        pr_number=submission.pr_number,
    )
