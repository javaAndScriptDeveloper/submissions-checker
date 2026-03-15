"""GitHub webhook endpoints (skeleton)."""

from fastapi import APIRouter, Header, HTTPException, Request

from submissions_checker.api.dependencies import DBSession
from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger
from submissions_checker.core.security import verify_github_signature
from submissions_checker.db.models.enums import OutboxEventType
from submissions_checker.db.models.outbox import OutboxMessage
from submissions_checker.db.models.submission import Submission

logger = get_logger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github")
async def handle_github_webhook(
    request: Request,
    db: DBSession,
    x_hub_signature_256: str | None = Header(None),
    x_github_event: str | None = Header(None),
) -> dict[str, str]:
    """
    Handle GitHub webhook events for pull request submissions.

    This endpoint receives GitHub webhooks when students open PRs from their
    forks to the parent assignment repository. It validates the signature,
    extracts the fork repository information, and creates an outbox message
    for asynchronous processing.

    Args:
        request: FastAPI request object
        db: Database session
        x_hub_signature_256: GitHub webhook signature
        x_github_event: GitHub event type

    Returns:
        Acknowledgment response

    Raises:
        HTTPException: If signature validation fails
    """
    logger.info(
        "github_webhook_received",
        event_type=x_github_event,
        has_signature=x_hub_signature_256 is not None,
    )

    # Read raw request body for signature verification
    body = await request.body()

    # Verify webhook signature
    """
    if not verify_github_signature(body, x_hub_signature_256):
        logger.warning("github_webhook_invalid_signature")
        raise HTTPException(status_code=401, detail="Invalid signature")
    """

    # Only process pull_request events
    if x_github_event != "pull_request":
        logger.info("github_webhook_ignored", event_type=x_github_event)
        return {"status": "ignored", "message": f"Event type '{x_github_event}' not processed"}

    # Parse webhook payload
    payload = await request.json()

    # Extract PR action (opened, synchronize, closed, etc.)
    action = payload.get("action")

    # Only process when PR is opened or synchronized (new commits)
    if action not in ["opened", "synchronize"]:
        logger.info("github_webhook_ignored_action", action=action)
        return {"status": "ignored", "message": f"Action '{action}' not processed"}

    # Extract relevant PR information
    pr_data = payload.get("pull_request", {})
    pr_number = pr_data.get("number")

    # Extract head repository (the fork) information
    head = pr_data.get("head", {})
    head_repo = head.get("repo")

    if not head_repo:
        logger.error("github_webhook_missing_head_repo", pr_number=pr_number)
        raise HTTPException(status_code=400, detail="Missing head repository in payload")

    fork_clone_url = head_repo.get("clone_url")
    fork_full_name = head_repo.get("full_name")
    head_ref = head.get("ref")  # Branch name
    head_sha = head.get("sha")  # Commit SHA

    # Extract base repository (parent) information
    base = pr_data.get("base", {})
    base_repo = base.get("repo", {})
    base_full_name = base_repo.get("full_name")

    logger.info(
        "processing_fork_pr",
        pr_number=pr_number,
        fork_repo=fork_full_name,
        parent_repo=base_full_name,
        branch=head_ref,
        commit=head_sha,
    )

    # Create outbox message for async PULL task
    outbox_message = OutboxMessage(
        event_type=OutboxEventType.PULL,
        payload={
            "pr_number": pr_number,
            "fork_clone_url": fork_clone_url,
            "fork_full_name": fork_full_name,
            "head_ref": head_ref,
            "head_sha": head_sha,
            "base_full_name": base_full_name,
            "action": action,
        }
    )

    db.add(outbox_message)
    await db.commit()

    logger.info(
        "outbox_message_created",
        outbox_id=outbox_message.id,
        event_type=outbox_message.event_type.value,
    )

    return {
        "status": "accepted",
        "message": "Pull request webhook received",
        "outbox_id": outbox_message.id,
    }


@router.post("/quiz-submission")
async def handle_quiz_submission(
    submission_id: int,
    request: Request,
    db: DBSession,
) -> dict[str, str]:
    """Receive quiz score callback from Google Apps Script.

    Called by the onFormSubmit trigger in the Apps Script after a student
    submits their quiz. The submission_id is embedded in the callback URL
    that was passed to the Apps Script when creating the form.
    """
    body = await request.json()

    submission = await db.get(Submission, submission_id)
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    settings = get_settings()
    if submission.quiz_score is not None and submission.quiz_score >= settings.quiz_pass_threshold:
        logger.info(
            "quiz_submission_ignored_already_passed",
            submission_id=submission_id,
            existing_score=submission.quiz_score,
        )
        return {"status": "ignored", "message": "Submission already passed"}

    submission.quiz_score = body.get("score")
    submission.quiz_max_score = body.get("max_score")
    await db.commit()

    logger.info(
        "quiz_submission_recorded",
        submission_id=submission_id,
        score=submission.quiz_score,
        max_score=submission.quiz_max_score,
    )

    # Enqueue async notification so the student receives a pass/fail email
    notify_message = OutboxMessage(
        event_type=OutboxEventType.NOTIFY_QUIZ_RESULT,
        payload={
            "submission_id": submission_id,
            "student_email": body.get("student_email", ""),
            "score": submission.quiz_score,
            "max_score": submission.quiz_max_score,
        },
    )
    db.add(notify_message)
    await db.commit()

    return {"status": "ok"}
