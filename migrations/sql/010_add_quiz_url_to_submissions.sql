-- Migration: 010_add_quiz_url_to_submissions
-- Description: Add quiz_url column to store the generated Google Form link
ALTER TABLE submissions ADD COLUMN IF NOT EXISTS quiz_url VARCHAR(1000);
