# Jobs

The system processes student submissions through a chain of three job types, all driven by the transactional outbox pattern. A background scheduler polls the `outbox_messages` table every 10 seconds and dispatches each pending message to the appropriate handler.

## How the outbox works

1. An event is written to the `outbox_messages` table (alongside any business data, in the same DB transaction).
2. The scheduler acquires a PostgreSQL advisory lock so only one processor runs at a time across all instances.
3. Pending and retryable messages are fetched in creation order, up to the configured batch size.
4. Each message is dispatched to its handler and awaited — not fire-and-forget — so that any follow-on writes (new outbox messages, updated records) are committed atomically with the original message being marked `finished`.
5. On failure the message is marked `error` and retried on the next cycle, up to `outbox_max_retries`.

---

## PULL

**Trigger:** GitHub webhook (`pull_request` event, actions `opened` or `synchronize`).

**What it does:**

1. Reads the fork repository information from the outbox payload.
2. Shallow-clones the fork branch to `workspace_dir/<fork_owner>/<fork_repo>` on disk. If a clone already exists it is removed first (handles PR updates).
3. Creates or updates a `Submission` record in the database with the clone path and sets its status to `cloning`.
4. Creates a `REVIEW` outbox message carrying only the `submission_id`.

All of steps 3–4 happen inside the processor's open database session, so they commit atomically with the PULL message being marked `finished`.

**Payload fields:**

| Field | Description |
|---|---|
| `pr_number` | GitHub PR number |
| `fork_clone_url` | HTTPS clone URL of the fork |
| `fork_full_name` | e.g. `student/repo-name` |
| `head_ref` | Branch name |
| `head_sha` | Commit SHA |
| `base_full_name` | Assignment parent repo, e.g. `instructor/repo-name` |
| `action` | `opened` or `synchronize` |

---

## REVIEW

**Trigger:** Created automatically by the PULL job.

**What it does (planned):**

1. Fetches the `Submission` record by `submission_id`.
2. Loads source files from the cloned repository path.
3. Sends the code to the AI reviewer.
4. Stores the review result in `submission.ai_review`.
5. Updates the submission status to `reviewing`.
6. Creates a `NOTIFY` outbox message so results are posted back to GitHub.

> **Status:** skeleton — the steps above are stubbed out and not yet implemented.

**Payload fields:**

| Field | Description |
|---|---|
| `submission_id` | Internal `Submission` table PK |

---

## NOTIFY

**Trigger:** Created automatically by the REVIEW job.

**What it does (planned):**

1. Fetches the `Submission` and its results.
2. Formats the AI review (and/or test results) into a human-readable comment.
3. Posts the comment to the GitHub PR.
4. Updates the commit status check on GitHub.
5. Marks the submission as `completed`.

> **Status:** skeleton — not yet implemented.

**Payload fields:**

| Field | Description |
|---|---|
| `submission_id` | Internal `Submission` table PK |
| `result_type` | `"review"` or `"test"` |
