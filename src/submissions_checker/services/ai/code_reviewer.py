"""Code review orchestration logic (skeleton)."""

from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


class CodeReviewer:
    """
    Orchestrates code review process (skeleton).

    TODO: Implement code review orchestration:
    - Prepare code for AI review (extract relevant files, add context)
    - Call AI client for review
    - Post-process AI responses
    - Format review comments for GitHub
    """

    async def review_submission(self, submission_id: int) -> dict:
        """
        Review a code submission (skeleton).

        Args:
            submission_id: Submission database ID

        Returns:
            Review results
        """
        logger.info("review_submission", submission_id=submission_id)

        # TODO: Implement submission review
        # 1. Fetch submission from database
        # 2. Load code files from cloned repository
        # 3. Send to AI for review
        # 4. Parse and structure review results
        # 5. Update submission record with review
        # 6. Post review as PR comment

        raise NotImplementedError("review_submission not yet implemented")
