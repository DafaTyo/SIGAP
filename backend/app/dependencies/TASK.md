# TASK.md – Backend/dependencies

## Goals
- Provide **dependency‑injection** helpers for:
  - Database session (`Depends(get_db)`).
  - Redis cache client (optional, for rate‑limiting / caching).
  - JWT token verifier / current user extractor.
- Semua dependency harus **lazy‑loaded** dan dapat **di‑override** untuk testing.

## Verification Criteria
- [] `get_db` meng‑return SQLAlchemy `Session` yang otomatis `commit/rollback` pada request selesai.
- [] `get_current_user` mem‑decode JWT, mem‑validasi `sub` dan `role`, dan men‑inject `User` model ke route.
- [] Unit‑test (`pytest backend/tests/dependencies`) mem‑mock DB dan JWT, memastikan error handling (401, 403).
- [] Coverage ≥ 85 % pada folder `dependencies`.
- [] CI menjalankan test suite dan gagal bila dependency tidak tersedia (mis. env var `DB_URL` hilang).

## Status
- [ ] Pending
