-- Migration: 005_replace_processed_with_state
-- Description: Replace boolean 'processed' field with state enum (pending, finished, error)
-- Date: 2026-02-15

-- Create the state enum type (lowercase to match Python enum)
CREATE TYPE outbox_message_state AS ENUM ('pending', 'finished', 'error');

-- Add the new state column with default value
ALTER TABLE outbox_messages
    ADD COLUMN state outbox_message_state NOT NULL DEFAULT 'pending';

-- Migrate existing data: processed=true -> finished, processed=false -> pending
UPDATE outbox_messages
    SET state = CASE
        WHEN processed = TRUE THEN 'finished'::outbox_message_state
        ELSE 'pending'::outbox_message_state
    END;

-- Rename processed_at to finished_at
ALTER TABLE outbox_messages
    RENAME COLUMN processed_at TO finished_at;

-- Drop old indexes that used the processed column
DROP INDEX IF EXISTS ix_outbox_messages_unprocessed;
DROP INDEX IF EXISTS ix_outbox_messages_processed;

-- Drop the old processed column
ALTER TABLE outbox_messages
    DROP COLUMN processed;

-- Create new composite indexes
CREATE INDEX IF NOT EXISTS ix_outbox_messages_state_event_type
    ON outbox_messages(state, event_type);

CREATE INDEX IF NOT EXISTS ix_outbox_messages_pending
    ON outbox_messages(state, created_at);

-- Add comment
COMMENT ON TYPE outbox_message_state IS
    'Processing states for outbox messages: pending (awaiting processing), finished (completed successfully), error (failed, will retry)';
