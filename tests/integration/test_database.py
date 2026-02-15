"""Database integration tests."""

import pytest
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from submissions_checker.db.models.outbox import OutboxMessage


@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession) -> None:
    """Test basic database connectivity."""
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_create_outbox_message(db_session: AsyncSession) -> None:
    """Test creating an outbox message."""
    message = OutboxMessage(
        aggregate_type="test_aggregate",
        aggregate_id="test-123",
        event_type="test_event",
        payload={"key": "value"},
    )

    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)

    assert message.id is not None
    assert message.aggregate_type == "test_aggregate"
    assert message.aggregate_id == "test-123"
    assert message.event_type == "test_event"
    assert message.payload == {"key": "value"}
    assert message.processed is False
    assert message.retry_count == 0


@pytest.mark.asyncio
async def test_outbox_message_mark_processed(db_session: AsyncSession) -> None:
    """Test marking an outbox message as processed."""
    message = OutboxMessage(
        aggregate_type="test_aggregate",
        aggregate_id="test-456",
        event_type="test_event",
        payload={},
    )

    db_session.add(message)
    await db_session.commit()

    # Mark as processed
    message.mark_processed()
    await db_session.commit()
    await db_session.refresh(message)

    assert message.processed is True
    assert message.processed_at is not None


@pytest.mark.asyncio
async def test_outbox_message_mark_failed(db_session: AsyncSession) -> None:
    """Test marking an outbox message as failed."""
    message = OutboxMessage(
        aggregate_type="test_aggregate",
        aggregate_id="test-789",
        event_type="test_event",
        payload={},
    )

    db_session.add(message)
    await db_session.commit()

    # Mark as failed
    error_msg = "Test error message"
    message.mark_failed(error_msg)
    await db_session.commit()
    await db_session.refresh(message)

    assert message.retry_count == 1
    assert message.error_message == error_msg
    assert message.processed is False


@pytest.mark.asyncio
async def test_query_unprocessed_outbox_messages(db_session: AsyncSession) -> None:
    """Test querying unprocessed outbox messages."""
    # Create processed message
    processed_msg = OutboxMessage(
        aggregate_type="test",
        aggregate_id="processed",
        event_type="test",
        payload={},
    )
    processed_msg.mark_processed()
    db_session.add(processed_msg)

    # Create unprocessed message
    unprocessed_msg = OutboxMessage(
        aggregate_type="test",
        aggregate_id="unprocessed",
        event_type="test",
        payload={},
    )
    db_session.add(unprocessed_msg)

    await db_session.commit()

    # Query unprocessed messages
    result = await db_session.execute(
        select(OutboxMessage).where(OutboxMessage.processed == False)  # noqa: E712
    )
    messages = result.scalars().all()

    assert len(messages) == 1
    assert messages[0].aggregate_id == "unprocessed"
