"""GitHub API client for interacting with GitHub."""

import httpx

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """Client for GitHub API operations."""

    def __init__(self) -> None:
        """Initialize GitHub client with configuration."""
        self.settings = get_settings()

    def _auth_headers(self) -> dict[str, str]:
        """Return Authorization headers using the configured GitHub token."""
        if not self.settings.github_token:
            raise ValueError("GITHUB_TOKEN is not set in environment configuration")
        return {
            "Authorization": f"Bearer {self.settings.github_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def get_pull_request(self, repo: str, pr_number: int) -> dict:
        """Fetch pull request metadata from the GitHub REST API.

        Args:
            repo: Repository full name (``owner/repo``)
            pr_number: Pull request number
        """
        logger.info("get_pull_request", repo=repo, pr_number=pr_number)
        url = f"{self.settings.github_api_base_url}/repos/{repo}/pulls/{pr_number}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self._auth_headers())
            response.raise_for_status()
            return response.json()

    async def clone_repository(self, repo_url: str, target_dir: str, ref: str) -> None:
        """
        Clone a repository to a target directory (skeleton).

        Args:
            repo_url: Repository URL
            target_dir: Target directory for cloning
            ref: Git reference (branch, tag, or commit SHA)
        """
        logger.info("clone_repository", repo_url=repo_url, ref=ref)

        # TODO: Implement repository cloning
        # Use subprocess or GitPython to clone the repository
        # subprocess.run(["git", "clone", "--depth", "1", "--branch", ref, repo_url, target_dir])

        raise NotImplementedError("clone_repository not yet implemented")

    async def post_comment(self, repo: str, pr_number: int, comment: str) -> None:
        """Post a comment on a pull request via the GitHub Issues API.

        GitHub PRs share the Issues comment endpoint — ``pr_number`` is the
        issue number for the PR.

        Args:
            repo: Repository full name (``owner/repo``)
            pr_number: Pull request / issue number
            comment: Markdown comment body
        """
        logger.info("post_comment", repo=repo, pr_number=pr_number)
        url = f"{self.settings.github_api_base_url}/repos/{repo}/issues/{pr_number}/comments"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=self._auth_headers(),
                json={"body": comment},
            )
            response.raise_for_status()
        logger.info("comment_posted", repo=repo, pr_number=pr_number)

    async def update_commit_status(
        self,
        repo: str,
        commit_sha: str,
        state: str,
        description: str,
        context: str = "submissions-checker",
    ) -> None:
        """
        Update commit status (skeleton).

        Args:
            repo: Repository full name (owner/repo)
            commit_sha: Commit SHA
            state: Status state (pending, success, failure, error)
            description: Status description
            context: Status context identifier
        """
        logger.info(
            "update_commit_status",
            repo=repo,
            commit_sha=commit_sha,
            state=state,
        )

        # TODO: Implement commit status update
        # url = f"{self.settings.github_api_base_url}/repos/{repo}/statuses/{commit_sha}"
        # async with httpx.AsyncClient() as client:
        #     response = await client.post(url, headers=self._auth_headers(), json={
        #         "state": state,
        #         "description": description,
        #         "context": context,
        #     })
        #     response.raise_for_status()

        raise NotImplementedError("update_commit_status not yet implemented")
