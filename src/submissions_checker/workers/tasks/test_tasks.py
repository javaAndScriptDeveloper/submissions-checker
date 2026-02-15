"""Test execution tasks."""

from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


async def run_cli_tests(submission_data: dict) -> None:
    """
    Run CLI tests for a submission (skeleton).

    This task:
    1. Retrieves submission from database
    2. Runs configured tests using TestRunner
    3. Parses test results
    4. Updates submission with test results
    5. Posts test results as PR comment

    Args:
        submission_data: Submission data including ID and test configuration
    """
    submission_id = submission_data.get("submission_id")
    logger.info("run_cli_tests_started", submission_id=submission_id)

    try:
        # TODO: Implement test execution
        # 1. Fetch submission from database
        # async with get_session() as db:
        #     result = await db.execute(
        #         select(Submission).where(Submission.id == submission_id)
        #     )
        #     submission = result.scalar_one()
        #
        # 2. Run tests using TestRunner
        # test_runner = TestRunner()
        # test_results = await test_runner.run_tests(
        #     repo_path=Path(f"/tmp/repos/{submission_id}"),
        #     test_command=submission.test_command,
        # )
        #
        # 3. Parse test results
        # parser = TestResultParser()
        # parsed_results = parser.parse_pytest_output(test_results["stdout"])
        #
        # 4. Update submission with results
        # submission.test_results = parsed_results
        # submission.status = "tests_completed"
        # await db.commit()
        #
        # 5. Post test results to PR
        # github_client = GitHubClient()
        # await github_client.post_comment(
        #     repo=submission.repository_name,
        #     pr_number=submission.pull_request_number,
        #     comment=format_test_results(parsed_results),
        # )

        logger.info("run_cli_tests_completed", submission_id=submission_id)

    except Exception as e:
        logger.error("run_cli_tests_failed", error=str(e), submission_id=submission_id)
        # Error handling - could implement retry logic at application level if needed
        raise
