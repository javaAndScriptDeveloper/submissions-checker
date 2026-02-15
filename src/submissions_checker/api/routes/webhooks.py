"""GitHub webhook endpoints (skeleton)."""

from fastapi import APIRouter, Header, Request

from submissions_checker.api.dependencies import DBSession
from submissions_checker.core.logging import get_logger

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
    Handle GitHub webhook events (skeleton).

    TODO: Implement webhook handling:
    1. Verify webhook signature using x_hub_signature_256
    2. Parse webhook payload
    3. Create outbox message for async processing
    4. Return 202 Accepted

    Args:
        request: FastAPI request object
        db: Database session
        x_hub_signature_256: GitHub webhook signature
        x_github_event: GitHub event type

    Returns:
        Acknowledgment response
    """
    logger.info(
        "github_webhook_received",
        event_type=x_github_event,
        has_signature=x_hub_signature_256 is not None,
    )

    # TODO: Implement webhook validation and processing
    # body = await request.body()
    # if not verify_github_signature(body, x_hub_signature_256):
    #     raise HTTPException(status_code=401, detail="Invalid signature")
    #
    # payload = await request.json()
    # outbox_message = OutboxMessage(
    #     aggregate_type="github_webhook",
    #     aggregate_id=payload.get("delivery_id", "unknown"),
    #     event_type=x_github_event,
    #     payload=payload,
    # )
    # db.add(outbox_message)
    # await db.commit()

    return {"status": "accepted", "message": "Webhook received (not yet implemented)"}
