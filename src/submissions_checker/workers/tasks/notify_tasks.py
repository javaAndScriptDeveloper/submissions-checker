"""Notification and result posting tasks."""

from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


async def execute_notify_task(notify_data: dict) -> None:
    """
    Send notifications and post results (skeleton).

    This task:
    1. Retrieves results from database
    2. Formats results for posting
    3. Posts results to GitHub PR
    4. Sends any additional notifications
    5. Updates submission status

    Args:
        notify_data: Notification data including submission ID and result type
    """
    submission_id = notify_data.get("submission_id")
    result_type = notify_data.get("result_type")  # "test" or "review"
    logger.info(
        "execute_notify_task_started",
        submission_id=submission_id,
        result_type=result_type
    )

    try:
        # TODO: Implement NOTIFY task
        # 1. Fetch submission and results from database
        # async with get_session() as db:
        #     result = await db.execute(
        #         select(Submission).where(Submission.id == submission_id)
        #     )
        #     submission = result.scalar_one()
        #
        # 2. Format results based on result_type
        # if result_type == "test":
        #     message = format_test_results(submission.test_results)
        # elif result_type == "review":
        #     message = format_ai_review(submission.ai_review)
        #
        # 3. Post to GitHub PR as comment
        # github_client = GitHubClient()
        # await github_client.post_comment(
        #     repo=submission.repository_name,
        #     pr_number=submission.pull_request_number,
        #     comment=message,
        # )
        #
        # 4. Update commit status
        # await github_client.update_commit_status(
        #     repo=submission.repository_name,
        #     commit_sha=submission.commit_sha,
        #     state="success" if submission.tests_passed else "failure",
        # )
        #
        # 5. Send any additional notifications (email, Slack, etc.)
        # await send_slack_notification(...)

        logger.info("execute_notify_task_completed", submission_id=submission_id)

    except Exception as e:
        logger.error(
            "execute_notify_task_failed",
            error=str(e),
            submission_id=submission_id
        )
        raise
