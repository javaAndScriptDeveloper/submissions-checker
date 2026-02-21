# Junior Dev Handover Checklist

Topics to walk through when handing this project over. Work through them roughly in order — each section builds on the previous one.

---

## 1. Project purpose
- [ ] What the system does: automated code review of student GitHub pull requests
- [ ] Who the actors are: students, instructors, GitHub, the AI provider
- [ ] High-level flow: student opens PR → webhook → clone → AI review → comment back on PR

---

## 2. Local setup
- [ ] Python version and virtual environment (`.venv`, `uv` or `pip`)
- [ ] Copy `.env.example` → `.env` and fill in required values
- [ ] Required env vars: `DATABASE_URL`, `GITHUB_WEBHOOK_SECRET`, `SECRET_KEY`, `OPENAI_API_KEY`
- [ ] Start PostgreSQL locally (or via Docker)
- [ ] Run the app: `uvicorn submissions_checker.main:app --reload`
- [ ] Verify health check: `GET /health`
- [ ] Swagger UI at `/docs`

---

## 3. Tech stack
- [ ] **FastAPI** — async HTTP framework, lifespan context manager pattern
- [ ] **SQLAlchemy** (async) — ORM for DB models; `AsyncSession` everywhere
- [ ] **PostgreSQL** — primary datastore; also used for advisory locks
- [ ] **pydantic-settings** — typed config loaded from `.env` (`core/config.py`)
- [ ] **APScheduler** — in-process background job scheduler (10-second poll loop)
- [ ] **structlog / logging** — structured logging (`get_logger(__name__)`)

---

## 4. Configuration system
- [ ] `core/config.py`: `Settings` class backed by pydantic-settings; reads from `.env`
- [ ] `get_settings()` is cached with `@lru_cache` — call it anywhere, no DI needed
- [ ] Key knobs: `SCHEDULER_ENABLED`, `OUTBOX_BATCH_SIZE`, `OUTBOX_MAX_RETRIES`, `WORKSPACE_DIR`
- [ ] `SCHEDULER_ENABLED=false` runs an API-only instance (no background worker)

---

## 5. Application startup sequence (`main.py`)
- [ ] `lifespan()` context manager: runs on startup and shutdown
- [ ] Startup order: run migrations → init DB pool → start scheduler
- [ ] Shutdown order: stop scheduler (waits for in-flight jobs) → close DB
- [ ] Why migrations run on startup: keeps schema in sync without a separate deploy step

---

## 6. Database migrations
- [ ] Custom raw-SQL migration system in `core/migrations.py` (not Alembic)
- [ ] Migration files live in `migrations/sql/` — numbered, ordered, run once
- [ ] `schema_migrations` table tracks which files have already run
- [ ] To add a migration: create `NNN_description.sql` in `migrations/sql/`
- [ ] Walk through existing migrations 001–007 to understand schema history

---

## 7. Database models
- [ ] `db/models/base.py` — `TimestampMixin` (created_at, updated_at) on all models
- [ ] `db/models/outbox.py` — `OutboxMessage`: the message queue table
- [ ] `db/models/submission.py` — `Submission`: one row per student PR
- [ ] `db/models/enums.py` — all enums: `SubmissionStatus`, `OutboxState`, `OutboxEventType`
- [ ] `db/session.py` — `get_db_session()` async context manager for background tasks
- [ ] `core/database.py` — `init_db()` / `close_db()` manage the connection pool

---

## 8. Transactional outbox pattern
- [ ] Why it exists: reliably decouple "write business data" from "trigger async work"
- [ ] Inserting an `OutboxMessage` in the same transaction as business data = atomicity guarantee
- [ ] The processor picks up `pending` messages and runs their handlers
- [ ] On success: message state → `finished`; on failure: state → `error`, increments `retry_count`
- [ ] Max retries controlled by `OUTBOX_MAX_RETRIES`; after that it stays `error` and needs manual intervention
- [ ] Read `docs/statuses.md` for the full state reference

---

## 9. GitHub webhook entry point (`api/routes/webhooks.py`)
- [ ] `POST /webhooks/github` receives all GitHub webhook payloads
- [ ] `core/security.py` — HMAC-SHA256 signature validation against `GITHUB_WEBHOOK_SECRET`
- [ ] Only `pull_request` events with action `opened` or `synchronize` are handled; everything else returns 200 and is ignored
- [ ] Handler extracts fork URL, branch, commit SHA, repo names → writes a `PULL` `OutboxMessage`
- [ ] Returns immediately; all real work is async

---

## 10. Background processor (`workers/scheduled/outbox_processor.py`)
- [ ] Called every 10 seconds by APScheduler
- [ ] Acquires a PostgreSQL advisory lock before doing anything — prevents concurrent runs across multiple app instances
- [ ] Fetches a batch of `pending` / retryable `error` messages (ordered by `created_at`)
- [ ] Dispatches each to the correct handler function based on `event_type`
- [ ] Each handler runs inside the same DB session → commits atomically with the message state update
- [ ] `core/scheduler.py` — `init_scheduler()`, `start_scheduler()`, `shutdown_scheduler()`

---

## 11. Job pipeline: PULL → REVIEW → NOTIFY
- [ ] Read `docs/jobs.md` for the definitive reference
- [ ] **PULL** (`workers/tasks/pull_tasks.py`) — fully implemented:
  - Shallow-clones the student fork into `WORKSPACE_DIR/<owner>/<repo>`
  - Creates/updates a `Submission` record, sets status to `cloning`
  - Writes a `REVIEW` outbox message (same DB transaction)
- [ ] **REVIEW** (`workers/tasks/review_tasks.py`) — skeleton only, not implemented:
  - Will load source files, call AI client, store result, create `NOTIFY` message
- [ ] **NOTIFY** (`workers/tasks/notify_tasks.py`) — skeleton only, not implemented:
  - Will post PR comment and commit status back to GitHub via the GitHub API

---

## 12. Services layer
- [ ] `services/github/client.py` — GitHub REST API client (post comments, update commit status)
- [ ] `services/github/webhook_validator.py` — webhook HMAC validation logic
- [ ] `services/github/pr_handler.py` — parses raw webhook payload into structured data
- [ ] `services/ai/client.py` — wraps OpenAI (or compatible) API
- [ ] `services/ai/code_reviewer.py` — builds prompts and parses AI responses
- [ ] `utils/git.py` — `clone_repository()`, `remove_repository()` shell helpers

---

## 13. API routes (other than webhooks)
- [ ] `api/routes/health.py` — `GET /health` liveness check
- [ ] `api/routes/users.py` — user management (CRUD)
- [ ] `api/dependencies.py` — FastAPI dependency injection helpers (DB session, settings)

---

## 14. What is NOT yet implemented
- [ ] REVIEW task — AI code review logic is a stub
- [ ] NOTIFY task — GitHub comment/status posting is a stub
- [ ] Tests — skeleton files exist in `tests/` but are mostly empty
- [ ] GitHub App authentication — only webhook secret auth is in place; App-based token auth is stubbed in config but not wired up

---

## 15. Key operational concerns
- [ ] `WORKSPACE_DIR` needs adequate disk space and must be writable; old clones are deleted before re-cloning on PR update
- [ ] Outbox messages in `error` state after max retries need manual review/reset
- [ ] Running multiple app instances: set `SCHEDULER_ENABLED=false` on API instances and `SCHEDULER_ENABLED=true` only on dedicated worker instances — the advisory lock provides safety but a single worker instance is simpler
- [ ] Logs are structured (JSON-friendly) — use `event` key to search

---

## 16. Suggested reading order for the code
1. `docs/statuses.md` + `docs/jobs.md`
2. `core/config.py`
3. `main.py`
4. `db/models/outbox.py` + `db/models/submission.py`
5. `api/routes/webhooks.py`
6. `workers/scheduled/outbox_processor.py`
7. `workers/tasks/pull_tasks.py`
8. `workers/tasks/review_tasks.py` (skeleton — your next work)
9. `workers/tasks/notify_tasks.py` (skeleton — your next work)
