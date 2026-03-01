-- Migration: 008_add_generate_quiz_event_type
-- Description: Add GENERATE_QUIZ value to outbox_event_type enum
ALTER TYPE outbox_event_type ADD VALUE IF NOT EXISTS 'GENERATE_QUIZ';
