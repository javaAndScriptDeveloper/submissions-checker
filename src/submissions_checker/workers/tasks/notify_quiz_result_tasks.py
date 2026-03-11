"""Quiz result notification task — sends pass/fail email to student."""

import re

from sqlalchemy.ext.asyncio import AsyncSession

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger
from submissions_checker.db.models.submission import Submission
from submissions_checker.services.notifications import build_dispatcher
from submissions_checker.services.notifications.templates import failed_template, passed_template

logger = get_logger(__name__)


async def execute_notify_quiz_result_task(db: AsyncSession, payload: dict) -> None:
    """Send a quiz result email to the student.

    Expected payload:
        {
            "submission_id": int,
            "student_email": str,
            "score": int,
            "max_score": int,
        }

    The email content depends on whether score >= settings.quiz_pass_threshold:
    - Passed: congratulations + score
    - Failed: failure notice + instructions to push a new commit to re-trigger the pipeline
    """
    submission_id = payload["submission_id"]
    student_email = payload["student_email"]
    score = payload["score"]
    max_score = payload["max_score"]

    logger.info("execute_notify_quiz_result_task_started", submission_id=submission_id, score=score)

    if not student_email:
        logger.warning("quiz_result_no_email", submission_id=submission_id)
        return

    submission = await db.get(Submission, submission_id)
    if submission is None:
        raise ValueError(f"Submission {submission_id} not found")

    settings = get_settings()

    match = re.search(r"\d+", submission.head_ref or "")
    lab_id = int(match.group()) if match else 1

    passed = score >= settings.quiz_pass_threshold
    if passed:
        subject, body = passed_template(submission.github_username, score, max_score, lab_id)
    else:
        subject, body = failed_template(submission.github_username, score, max_score, lab_id)

    dispatcher = build_dispatcher(settings)
    await dispatcher.notify(student_email, subject, body)

    logger.info(
        "quiz_result_notification_sent",
        submission_id=submission_id,
        passed=passed,
        score=score,
        max_score=max_score,
    )
