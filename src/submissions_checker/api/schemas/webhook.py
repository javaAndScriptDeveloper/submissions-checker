"""Webhook schemas (skeleton - to be implemented)."""

from pydantic import BaseModel


class GitHubPullRequestEvent(BaseModel):
    """Schema for GitHub pull request webhook event (skeleton)."""

    # TODO: Add fields based on GitHub webhook payload
    # action: str
    # pull_request: dict
    # repository: dict
    # sender: dict
    pass


class WebhookResponse(BaseModel):
    """Schema for webhook response (skeleton)."""

    # status: str
    # message: str
    pass
