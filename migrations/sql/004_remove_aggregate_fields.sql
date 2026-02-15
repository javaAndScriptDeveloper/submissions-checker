-- Migration: 004_remove_aggregate_fields
-- Description: Remove unused aggregate_type and aggregate_id columns from outbox_messages
-- Date: 2026-02-15

-- Drop the aggregate index first (references the columns we're removing)
DROP INDEX IF EXISTS ix_outbox_messages_aggregate;

-- Drop the aggregate columns
ALTER TABLE outbox_messages
    DROP COLUMN IF EXISTS aggregate_type,
    DROP COLUMN IF EXISTS aggregate_id;
