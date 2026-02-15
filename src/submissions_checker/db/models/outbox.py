"""Transactional outbox pattern model for reliable event processing."""

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from submissions_checker.db.models.base import Base, TimestampMixin


class OutboxMessage(Base, TimestampMixin):
    """
    Outbox message for transactional event processing.

    The transactional outbox pattern ensures reliable event processing:
    1. Business logic writes to database + outbox table in same transaction
    2. Background worker polls outbox table for unprocessed messages
    3. Worker dispatches messages to appropriate handlers (Arq tasks)
    4. Messages marked as processed on success, retry on failure
    """

    __tablename__ = "outbox_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Aggregate information (what entity triggered this event)
    aggregate_type: Mapped[str] = mapped_column(String(100), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(255), nullable=False)

    # Event information
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    # Processing status
    processed: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Retry handling
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        # Index for efficient queries of unprocessed messages
        Index("ix_outbox_messages_unprocessed", "processed", "created_at"),
        # Index for tracking events by aggregate
        Index("ix_outbox_messages_aggregate", "aggregate_type", "aggregate_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<OutboxMessage(id={self.id}, "
            f"aggregate={self.aggregate_type}:{self.aggregate_id}, "
            f"event={self.event_type}, "
            f"processed={self.processed})>"
        )

    def mark_processed(self) -> None:
        """Mark the message as successfully processed."""
        self.processed = True
        self.processed_at = datetime.now(timezone.utc)

    def mark_failed(self, error: str) -> None:
        """Mark the message as failed and increment retry count."""
        self.retry_count += 1
        self.error_message = error
