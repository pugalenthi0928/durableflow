# Failure lab 001 — process restart loses state

## Question

What happens to an acknowledged job when the process owning the in-memory repository restarts?

## Prediction — learner must complete before the experiment

```text
I predict:

The user will observe:

The data remaining after restart will be:

This happens because:

The smallest mechanism that could change the result is:
```

## Procedure

1. Run `make run`.
2. Submit a document and copy its job ID.
3. Confirm `GET /v1/jobs/{id}` returns `200`.
4. Stop the server completely.
5. Start `make run` again.
6. Request the same job ID.
7. Capture the response and structured request log.

## Expected observation

The restarted process creates a new empty `InMemoryJobRepository`. The old identifier therefore
returns `404 job_not_found`. The job was acknowledged and then silently lost from the product's
perspective.

## Why

Process memory has the same lifetime and failure boundary as the API. It is neither durable nor
shared between replicas.

## Concept earned

Persistent authoritative state. Stage 3 will introduce PostgreSQL, a schema, constraints,
migrations, transactions, and integration tests only after this failure has been explained.

## Acceptance evidence

- Prediction completed before execution.
- Before/after requests recorded.
- Request IDs captured.
- Actual result explained in the learner's own words.
- No database proposed without a schema and invariant mapping.

