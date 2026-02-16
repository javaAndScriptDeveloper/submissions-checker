"""AI code review tasks."""

from sqlalchemy.ext.asyncio import AsyncSession

from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


async def execute_review_task(db: AsyncSession, review_data: dict) -> None:
    """
    Perform AI code review for a submission (skeleton).

    This task:
    1. Retrieves submission from database
    2. Loads code files from cloned repository
    3. Sends code to AI for review
    4. Parses AI response
    5. Updates submission with review results
    6. Creates NOTIFY outbox message for posting review

    Args:
        db: Database session for transactional operations
        review_data: Review data including submission ID
    """
    submission_id = review_data.get("submission_id")
    logger.info("execute_review_task_started", submission_id=submission_id)

    try:
        # TODO: Implement REVIEW task
        # 1. Fetch submission from database
        # async with get_session() as db:
        #     result = await db.execute(
        #         select(Submission).where(Submission.id == submission_id)
        #     )
        #     submission = result.scalar_one()
        #
        # 2. Load code files
        # repo_path = Path(f"/tmp/repos/{submission_id}")
        # code_files = load_code_files(repo_path)
        #
        # 3. Send to AI for review
        # ai_client = AIClient()
        # review = await ai_client.review_code(
        #     code=combine_code_files(code_files),
        #     context=submission.assignment_requirements,
        # )
        #
        # 4. Update submission with review
        # submission.ai_review = review
        # submission.status = "review_completed"
        # await db.commit()
        #
        # 5. Create NOTIFY outbox message for posting results
        # notify_message = OutboxMessage(
        #     event_type=OutboxEventType.NOTIFY,
        #     payload={"submission_id": submission.id, "result_type": "review"}
        # )
        # db.add(notify_message)
        # await db.commit()

        logger.info("execute_review_task_completed", submission_id=submission_id)

    except Exception as e:
        logger.error("execute_review_task_failed", error=str(e), submission_id=submission_id)
        raise
