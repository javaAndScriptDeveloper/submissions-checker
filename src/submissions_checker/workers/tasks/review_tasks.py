"""AI code review tasks."""

from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


async def perform_ai_review(code_data: dict) -> None:
    """
    Perform AI code review for a submission (skeleton).

    This task:
    1. Retrieves submission from database
    2. Loads code files from cloned repository
    3. Sends code to AI for review
    4. Parses AI response
    5. Updates submission with review results
    6. Posts review as PR comment

    Args:
        code_data: Code data including submission ID
    """
    submission_id = code_data.get("submission_id")
    logger.info("perform_ai_review_started", submission_id=submission_id)

    try:
        # TODO: Implement AI code review
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
        # 5. Post review to PR
        # github_client = GitHubClient()
        # await github_client.post_comment(
        #     repo=submission.repository_name,
        #     pr_number=submission.pull_request_number,
        #     comment=format_ai_review(review),
        # )

        logger.info("perform_ai_review_completed", submission_id=submission_id)

    except Exception as e:
        logger.error("perform_ai_review_failed", error=str(e), submission_id=submission_id)
        # Error handling - could implement retry logic at application level if needed
        raise
