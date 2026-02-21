-- Create submission_status enum
CREATE TYPE submission_status AS ENUM (
    'pending',
    'cloning',
    'reviewing',
    'completed',
    'failed'
);

-- Create submissions table
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    pr_number INTEGER NOT NULL,
    fork_full_name VARCHAR(255) NOT NULL,
    base_full_name VARCHAR(255) NOT NULL,
    head_ref VARCHAR(255) NOT NULL,
    head_sha VARCHAR(255) NOT NULL,
    github_username VARCHAR(255) NOT NULL,
    repository_path VARCHAR(500),
    status submission_status NOT NULL DEFAULT 'pending',
    test_results JSONB,
    ai_review JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for efficient queries
CREATE INDEX ix_submissions_pr_number ON submissions(pr_number);
CREATE INDEX ix_submissions_github_username ON submissions(github_username);
CREATE INDEX ix_submissions_status ON submissions(status);

-- Create updated_at trigger
CREATE TRIGGER update_submissions_updated_at
    BEFORE UPDATE ON submissions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
