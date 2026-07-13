# TASK.md – Backend/utils

## Goals
- Kumpulan **utility functions** yang pure dan reusable across the codebase.
- Fokus pada: pagination helpers, datetime helpers, UUID generator, error‑wrapper, response‑model factory.

## Verification Criteria
- [] `utils.pagination.paginate(query, limit, offset)` meng‑return `items`, `total`, `limit`, `offset`.
- [] `utils.datetime.now_utc()` returns timezone‑aware UTC datetime.
- [] `utils.errors.AppError` wrapper (shared dengan folder `exceptions`).
- [] Unit‑test untuk setiap helper (`pytest backend/tests/utils`).
- [] Coverage ≥ 90 % pada folder `utils`.

## Status
- [ ] Pending
