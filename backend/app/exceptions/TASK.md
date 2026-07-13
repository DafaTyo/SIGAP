# TASK‑BE‑008‑01 – Exception Base Classes

## Goals
- Define a hierarchy of custom exception classes that inherit from `fastapi.HTTPException`.
- Provide a base `AppError` with fields `status_code`, `detail`, and optional `extra` dict for additional context.
- Derive specific exceptions (e.g., `NotFoundError`, `ConflictError`, `ValidationError`) that set appropriate HTTP status codes.
- Ensure each exception can be raised from services or routers and will be automatically converted to JSON error responses by FastAPI.

## Verification Criteria
- [] `AppError` can be instantiated with custom `status_code` and `detail` and when raised returns a JSON response matching FastAPI's default error format.
- [] Sub‑classes (`NotFoundError`, `ConflictError`, `ValidationError`) set correct status codes (404, 409, 422 respectively).
- [] Unit test `tests/exceptions/test_app_error.py` verifies that raising each exception yields the expected status code and JSON payload.
- [] CI pipeline runs the exception tests and fails on regression.

## Status
- [] Pending