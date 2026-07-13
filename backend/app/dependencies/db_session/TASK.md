# TASK‑BE‑007‑01 – DB Session Dependency

## Goals
- Provide a FastAPI dependency that yields a SQLAlchemy `Session` scoped to the request.
- Ensure the session is properly committed/rolled back and closed after the request finishes.
- Support async and sync SQLAlchemy usage (via `sessionmaker` with `autocommit=False`).

## Verification Criteria
- [] Dependency `get_db()` can be injected into any endpoint (`Depends(get_db)`).
- [] When endpoint succeeds, changes are committed; when it raises an exception, transaction is rolled back.
- [] Unit test `tests/dependencies/test_db_dependency.py` uses a temporary SQLite in‑memory DB to verify commit/rollback behaviour.
- [] CI runs the DB‑dependency test suite and fails on regression.

## Status
- [] Pending