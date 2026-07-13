# TASK‑BE‑006‑06 – Audit Log Middleware

## Goals
- Record every inbound request and its outcome (allowed/denied, status code, processing time).
- Store logs in PostgreSQL table `audit_log` with columns:
  - `id` (serial primary key)
  - `request_id` (UUID from Request‑ID middleware)
  - `user_id` (extracted from JWT or `anonymous`)
  - `method`
  - `path`
  - `query_params`
  - `status_code`
  - `decision` ("allow" / "deny")
  - `timestamp`
  - `processing_ms`
- Ensure the logging operation does **not** block the response (use async `await` insertion).

## Verification Criteria
- [] Every request creates exactly one row in `audit_log`.
- [] Row contains the same `request_id` as response header `X‑Request‑ID`.
- [] Denied requests have `decision = 'deny'`; allowed requests have `decision = 'allow'`.
- [] Unit test `tests/middleware/test_audit_log.py` inserts a request through `TestClient` and then queries the test DB to verify the row.
- [] CI pipeline runs audit‑log tests and fails if row count mismatches.

## Status
- [] Pending