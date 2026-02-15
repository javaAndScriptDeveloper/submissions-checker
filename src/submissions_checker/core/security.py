"""Security utilities for webhook validation and authentication."""

import hashlib
import hmac
from typing import Any

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger

logger = get_logger(__name__)


def verify_github_signature(payload: bytes, signature_header: str) -> bool:
    """
    Verify GitHub webhook signature using HMAC-SHA256.

    Args:
        payload: Raw request body bytes
        signature_header: Value of X-Hub-Signature-256 header

    Returns:
        True if signature is valid, False otherwise
    """
    settings = get_settings()

    if not signature_header:
        logger.warning("github_webhook_missing_signature")
        return False

    # GitHub signature format: "sha256=<hash>"
    if not signature_header.startswith("sha256="):
        logger.warning("github_webhook_invalid_signature_format")
        return False

    expected_signature = signature_header[7:]  # Remove "sha256=" prefix

    # Compute HMAC-SHA256 signature
    secret = settings.github_webhook_secret.encode("utf-8")
    computed_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()

    # Constant-time comparison to prevent timing attacks
    is_valid = hmac.compare_digest(computed_signature, expected_signature)

    if not is_valid:
        logger.warning("github_webhook_signature_mismatch")

    return is_valid


def create_webhook_signature(payload: bytes) -> str:
    """
    Create GitHub-style webhook signature for testing.

    Args:
        payload: Raw request body bytes

    Returns:
        Signature in format "sha256=<hash>"
    """
    settings = get_settings()
    secret = settings.github_webhook_secret.encode("utf-8")
    signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return f"sha256={signature}"


# JWT utilities for future authentication implementation
# These are placeholders for when user authentication is implemented

def create_access_token(data: dict[str, Any], expires_delta: int = 3600) -> str:
    """Create JWT access token (placeholder)."""
    raise NotImplementedError("JWT token creation not yet implemented")


def verify_access_token(token: str) -> dict[str, Any]:
    """Verify JWT access token (placeholder)."""
    raise NotImplementedError("JWT token verification not yet implemented")
