"""Transactional outbox message processor."""

import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from submissions_checker.core.config import get_settings
from submissions_checker.core.logging import get_logger
from submissions_checker.db.models.outbox import OutboxMessage
from submissions_checker.db.session import get_session
from submissions_checker.workers.tasks.pr_tasks import process_pr_webhook
from submissions_checker.workers.tasks.review_tasks import perform_ai_review
from submissions_checker.workers.tasks.test_tasks import run_cli_tests

logger = get_logger(__name__)


async def process_outbox_messages() -> None:
    """
    Process unprocessed outbox messages (scheduled job).

    This function runs periodically (every 10 seconds) to:
    1. Query unprocessed outbox messages
    2. Dispatch messages to appropriate background tasks
    3. Mark messages as processed on success
    4. Handle retry logic on failure

    The transactional outbox pattern ensures reliable event processing:
    - Business logic writes to database + outbox table in same transaction
    - This job polls for unprocessed messages
    - Messages are dispatched to background tasks (via asyncio.create_task)
    - Processing is idempotent and handles retries
    """
    settings = get_settings()
    logger.info("process_outbox_messages_started")

    processed_count = 0
    failed_count = 0

    try:
        async with get_session() as db:
            # Query unprocessed messages (with retry limit)
            result = await db.execute(
                select(OutboxMessage)
                .where(OutboxMessage.processed == False)  # noqa: E712
                .where(OutboxMessage.retry_count < settings.outbox_max_retries)
                .order_by(OutboxMessage.created_at.asc())
                .limit(settings.outbox_batch_size)
            )
            messages = result.scalars().all()

            logger.info("outbox_messages_fetched", count=len(messages))

            for message in messages:
                try:
                    # Dispatch message to appropriate task based on event type
                    await dispatch_outbox_message(message)

                    # Mark as processed
                    message.mark_processed()
                    processed_count += 1

                except Exception as e:
                    logger.error(
                        "outbox_message_dispatch_failed",
                        message_id=message.id,
                        event_type=message.event_type,
                        error=str(e),
                    )

                    # Mark as failed and increment retry count
                    message.mark_failed(str(e))
                    failed_count += 1

            # Commit all changes (processed and failed messages)
            await db.commit()

        logger.info(
            "process_outbox_messages_completed",
            processed=processed_count,
            failed=failed_count,
        )

    except Exception as e:
        logger.error("process_outbox_messages_error", error=str(e))


async def dispatch_outbox_message(message: OutboxMessage) -> None:
    """
    Dispatch an outbox message to the appropriate background task.

    Args:
        message: Outbox message to dispatch

    Raises:
        Exception: If dispatch fails
    """
    logger.info(
        "dispatching_outbox_message",
        message_id=message.id,
        aggregate_type=message.aggregate_type,
        event_type=message.event_type,
    )

    # Route messages to appropriate tasks based on event type
    if message.event_type == "pr_webhook_received":
        # Dispatch to PR processing task (fire and forget)
        asyncio.create_task(process_pr_webhook(message.payload))

    elif message.event_type == "tests_requested":
        # Dispatch to test execution task (fire and forget)
        asyncio.create_task(run_cli_tests(message.payload))

    elif message.event_type == "review_requested":
        # Dispatch to AI review task (fire and forget)
        asyncio.create_task(perform_ai_review(message.payload))

    else:
        logger.warning(
            "unknown_outbox_event_type",
            message_id=message.id,
            event_type=message.event_type,
        )
        raise ValueError(f"Unknown event type: {message.event_type}")

    logger.info("outbox_message_dispatched", message_id=message.id)
