# Statuses

## Submission status

Tracks the lifecycle of a single student submission (one PR).

| Status | Set by | Meaning |
|---|---|---|
| `pending` | Default on record creation | Submission row created, waiting for the PULL job to start cloning. |
| `cloning` | PULL job | Repository is being (or has been) cloned to the local workspace. A REVIEW outbox message has been queued. |
| `reviewing` | REVIEW job (planned) | AI code review is in progress. |
| `completed` | NOTIFY job (planned) | All processing finished; results have been posted to GitHub. |
| `failed` | Any job on unrecoverable error | Processing stopped. The associated outbox message will have an `error` state with a description. |

The happy-path flow is:

```
pending → cloning → reviewing → completed
```

---

## Outbox message state

Tracks the processing state of a single entry in the `outbox_messages` table.

| State | Meaning |
|---|---|
| `pending` | Message created, not yet picked up by the processor. |
| `finished` | Handler completed successfully. The message will not be processed again. |
| `error` | Handler threw an exception. The message will be retried on the next processor cycle, up to `outbox_max_retries` times. The `error_message` column holds the last exception string and `retry_count` tracks how many attempts have been made. |

---

## Outbox event types

| Event type | Handler | Description |
|---|---|---|
| `PULL` | `execute_pull_task` | Clone the student fork and create a Submission record. |
| `REVIEW` | `execute_review_task` | Run AI code review on the cloned repository. |
| `NOTIFY` | `execute_notify_task` | Post review results as a GitHub PR comment. |
