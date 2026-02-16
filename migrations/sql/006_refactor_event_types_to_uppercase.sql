-- Migration: 006_refactor_event_types_to_uppercase
-- Description: Refactor outbox event types to uppercase (PULL, REVIEW, NOTIFY)
-- Date: 2026-02-15

-- Drop the constraint temporarily to allow type conversion
ALTER TABLE outbox_messages ALTER COLUMN event_type TYPE VARCHAR(100);

-- Drop old enum type
DROP TYPE IF EXISTS outbox_event_type;

-- Create new enum with uppercase values
CREATE TYPE outbox_event_type AS ENUM ('PULL', 'REVIEW', 'NOTIFY');

-- Update any existing data (map old values to new)
UPDATE outbox_messages
SET event_type = CASE
    WHEN event_type = 'pr_webhook_received' THEN 'PULL'
    WHEN event_type = 'tests_requested' THEN 'PULL'
    WHEN event_type = 'review_requested' THEN 'REVIEW'
    ELSE event_type
END;

-- Convert column back to enum type
ALTER TABLE outbox_messages
    ALTER COLUMN event_type TYPE outbox_event_type
    USING event_type::outbox_event_type;

-- Update comment
COMMENT ON TYPE outbox_event_type IS
    'Valid event types: PULL (pull code and run tests), REVIEW (AI review), NOTIFY (send notifications)';

-- INSERT INTO public.outbox_messages (id, event_type, payload, finished_at, retry_count, error_message, created_at, updated_at, state) VALUES (1, 'PULL', '{"action": "synchronize", "head_ref": "main", "head_sha": "b3f770053fe44b4a0edc722c3a47a83094468cd0", "pr_number": 1, "base_full_name": "javaAndScriptDeveloper/basics_of_python", "fork_clone_url": "https://github.com/raiseAndCall/basics_of_python.git", "fork_full_name": "raiseAndCall/basics_of_python"}', '2026-02-15 21:07:03.849952 +00:00', 0, null, '2026-02-15 21:06:59.649033 +00:00', '2026-02-15 21:07:03.840055 +00:00', 'finished');
