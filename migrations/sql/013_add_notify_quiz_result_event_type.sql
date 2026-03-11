-- Migration: 013_add_notify_quiz_result_event_type
-- Description: Add NOTIFY_QUIZ_RESULT value to outbox_event_type enum
ALTER TYPE outbox_event_type ADD VALUE IF NOT EXISTS 'NOTIFY_QUIZ_RESULT';
