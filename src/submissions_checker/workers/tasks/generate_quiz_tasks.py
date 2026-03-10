"""Google Forms quiz generation task."""

import re

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger
from submissions_checker.db.models import OutboxEventType, OutboxMessage, Submission

logger = get_logger(__name__)


async def execute_generate_quiz_task(db: AsyncSession, quiz_data: dict) -> None:
    """Call Google Apps Script to generate a Google Form quiz from AI review questions.

    Reads the ``ai_review`` dict directly from the outbox payload (no extra DB
    fetch needed), POSTs it to the configured Google Apps Script endpoint, saves
    the returned form URL to ``submission.quiz_url``, and enqueues a NOTIFY
    outbox message so the next stage can publish the link.

    Expected payload: ``{"submission_id": int, "ai_review": dict}``
    Enqueued NOTIFY payload: ``{"submission_id": int, "form_url": str}``
    """
    submission_id = quiz_data.get("submission_id")
    ai_review = quiz_data.get("ai_review")
    logger.info("execute_generate_quiz_task_started", submission_id=submission_id)

    if not ai_review:
        raise ValueError(
            f"No ai_review in GENERATE_QUIZ payload for submission {submission_id}"
        )

    settings = get_settings()

    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one()

    match = re.search(r"\d+", submission.head_ref or "")
    lab_id = int(match.group()) if match else 1
    title = f"Lab {lab_id} Quiz — {submission.github_username}"

    callback_url = f"{settings.base_url}/webhooks/quiz-submission?submission_id={submission_id}"
    gas_payload = {"title": title, "callback_url": callback_url, **ai_review}

    logger.info("sending_to_google_apps_script", submission_id=submission_id, title=title)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.google_script_url,
            json=gas_payload,
            timeout=30.0,
            follow_redirects=True,
        )
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "text/html" in content_type:
            raise ValueError(
                f"Google Apps Script returned an HTML error page: {response.text[:300]}"
            )

        try:
            body = response.json()
            form_url = body.get("formUrl") or body.get("url") or str(body)
        except Exception:
            form_url = response.text

    logger.info("google_form_created", submission_id=submission_id, form_url=form_url)

    submission.quiz_url = form_url

    notify_message = OutboxMessage(
        event_type=OutboxEventType.NOTIFY,
        payload={"submission_id": submission.id, "form_url": form_url},
    )
    db.add(notify_message)

    logger.info("execute_generate_quiz_task_completed", submission_id=submission_id)
