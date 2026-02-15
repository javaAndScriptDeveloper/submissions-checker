-- Migration: 001_create_schema_migrations
-- Description: Bootstrap migration tracking table
-- Date: 2026-02-15

CREATE TABLE IF NOT EXISTS schema_migrations (
    id SERIAL PRIMARY KEY,
    migration_name VARCHAR(255) NOT NULL UNIQUE,
    checksum VARCHAR(64) NOT NULL,
    executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    execution_time_ms INTEGER,
    success BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_schema_migrations_name
    ON schema_migrations(migration_name);

CREATE INDEX IF NOT EXISTS idx_schema_migrations_executed_at
    ON schema_migrations(executed_at DESC);

COMMENT ON TABLE schema_migrations IS
    'Tracks executed database migrations for idempotent schema management';
