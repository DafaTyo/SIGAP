# TASK‑BE‑007‑04 – Settings Dependency

## Goals
- Load application configuration from environment variables using Pydantic `BaseSettings`.
- Provide a FastAPI dependency `get_settings()` that returns a singleton settings instance.
- Support validation of critical variables (e.g., `DATABASE_URL`, `JWT_PUBLIC_KEY`, `OPA_URL`).
- Allow hot‑reload in development mode when environment variables change.

## Verification Criteria
- [] `Settings` model raises `ValidationError` if required env vars are missing or malformed.
- [] `get_settings()` returns the same instance across multiple endpoint calls (singleton).
- [] Unit test `tests/dependencies/test_settings.py` mocks environment variables and verifies successful load and validation errors.
- [] CI pipeline runs the settings‑dependency tests.

## Status
- [] Pending