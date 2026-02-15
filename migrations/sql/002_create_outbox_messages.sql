-- Migration: 002_create_outbox_messages
-- Description: Create transactional outbox pattern table
-- Date: 2026-02-15

CREATE TABLE IF NOT EXISTS outbox_messages (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    processed_at TIMESTAMPTZ,
    retry_count INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index for efficient queries of unprocessed messages
CREATE INDEX IF NOT EXISTS ix_outbox_messages_unprocessed
    ON outbox_messages(processed, created_at) WHERE processed = FALSE;

-- Index for efficient queries by processed status
CREATE INDEX IF NOT EXISTS ix_outbox_messages_processed
    ON outbox_messages(processed, event_type);

COMMENT ON TABLE outbox_messages IS
    'Transactional outbox: ensures reliable event processing';

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_outbox_messages_updated_at
    BEFORE UPDATE ON outbox_messages
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
