"""Pull and test execution tasks."""

import shutil
from pathlib import Path

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


async def execute_pull_task(pull_data: dict) -> None:
    """
    Clone fork repository for evaluation.

    This task extracts the fork repository information from the webhook payload
    and clones it to the configured workspace directory. The cloned repository
    can later be used for running tests or AI review.

    Expected payload structure:
    {
        "pr_number": int,
        "fork_clone_url": str,        # HTTPS clone URL of the fork
        "fork_full_name": str,        # e.g., "raiseAndCall/basics_of_python"
        "head_ref": str,              # Branch name (e.g., "main")
        "head_sha": str,              # Commit SHA
        "base_full_name": str,        # Parent repo (e.g., "javaAndScriptDeveloper/basics_of_python")
        "action": str,                # "opened" or "synchronize"
    }

    Args:
        pull_data: Pull request and repository data from webhook payload

    Raises:
        ValueError: If required fields are missing from payload
        RuntimeError: If git clone fails
    """
    # Extract required fields
    pr_number = pull_data.get("pr_number")
    fork_clone_url = pull_data.get("fork_clone_url")
    fork_full_name = pull_data.get("fork_full_name")
    head_ref = pull_data.get("head_ref")
    head_sha = pull_data.get("head_sha")
    base_full_name = pull_data.get("base_full_name")

    logger.info(
        "execute_pull_task_started",
        pr_number=pr_number,
        fork_repo=fork_full_name,
        parent_repo=base_full_name,
        branch=head_ref,
        commit=head_sha,
    )

    # Validate required fields
    if not all([fork_clone_url, fork_full_name, head_ref, head_sha]):
        missing = [
            field for field, value in [
                ("fork_clone_url", fork_clone_url),
                ("fork_full_name", fork_full_name),
                ("head_ref", head_ref),
                ("head_sha", head_sha),
            ] if not value
        ]
        logger.error("execute_pull_task_missing_fields", missing_fields=missing)
        raise ValueError(f"Missing required fields in payload: {missing}")

    try:
        # Get workspace directory from settings
        settings = get_settings()
        workspace_base = Path(settings.workspace_dir)

        # Create unique directory for this submission
        # Using format: workspace_dir/fork_owner/fork_repo/pr_number
        fork_owner, fork_repo = fork_full_name.split("/")
        clone_path = workspace_base / fork_owner / fork_repo / str(pr_number)

        # Remove existing directory if it exists (for PR updates)
        if clone_path.exists():
            logger.info("removing_existing_clone", path=str(clone_path))
            shutil.rmtree(clone_path)

        # Clone the fork repository
        from submissions_checker.utils.git import clone_repository

        await clone_repository(
            repo_url=fork_clone_url,
            target_dir=clone_path,
            branch=head_ref,
            depth=1,  # Shallow clone for efficiency
        )

        logger.info(
            "execute_pull_task_completed",
            fork_repo=fork_full_name,
            clone_path=str(clone_path),
            commit=head_sha,
        )

    except Exception as e:
        logger.error(
            "execute_pull_task_failed",
            error=str(e),
            fork_repo=fork_full_name,
            pr_number=pr_number,
        )
        raise
