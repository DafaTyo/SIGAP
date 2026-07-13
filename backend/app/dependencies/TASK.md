# TASK‑BE‑007‑05 – Dependency Package Master List

## Goals
- Centralize all FastAPI dependencies (DB session, Redis cache, JWT auth, Settings) in a single package.
- Provide a helper `register_dependencies(app)` that can optionally inject dependencies globally (e.g., via `app.dependency_overrides`).
- Ensure each sub‑dependency has **≥ 90 %** test coverage and passes CI.
- Make the package easy to import: `from .dependencies import get_db, get_redis, get_current_user, get_settings`.

## Verification Criteria
- [] All sub‑dependency `TASK‑BE‑007‑0x` items are marked **[x]** when their unit tests succeed.
- [] `register_dependencies(app)` can be called from `app/main.py` to set global overrides for testing environments.
- [] End‑to‑end test `tests/dependencies/test_full_package.py` creates a FastAPI `TestClient` with all dependencies wired and verifies that:
  - DB session works (INSERT & SELECT).
  - Redis cache can store/retrieve a value.
  - JWT auth correctly extracts `user_id`.
  - Settings are accessible inside a sample endpoint.
- [] CI runs the full‑package dependency tests and fails on any regression.

## Status
- [] Pending