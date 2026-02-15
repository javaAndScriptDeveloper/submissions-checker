-- Migration: 003_add_outbox_event_type_enum
-- Description: Convert event_type column to use PostgreSQL ENUM for type safety
-- Date: 2026-02-15

-- Create the ENUM type
CREATE TYPE outbox_event_type AS ENUM (
    'pr_webhook_received',
    'tests_requested',
    'review_requested'
);

-- Alter the table to use the ENUM type
-- First, we need to convert the existing VARCHAR column to the ENUM type
ALTER TABLE outbox_messages
    ALTER COLUMN event_type TYPE outbox_event_type
    USING event_type::outbox_event_type;

-- Add a comment explaining the enum
COMMENT ON TYPE outbox_event_type IS
    'Valid event types for outbox messages - ensures type safety and prevents invalid event types';
