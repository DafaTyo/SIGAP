# TASK.md – Backend/tests/dependencies

## Goals
- Test semua dependency injector (`get_db`, `get_current_user`, `redis_client`).
- Pastikan dependency meng‑raise **HTTPException** yang tepat bila env var tidak ada atau token tidak valid.

## Verification Criteria
- [] `get_db` menghasilkan session yang dapat dipakai untuk operasi CRUD dalam test.
- [] `get_current_user` meng‑decode JWT dengan benar; meng‑raise 401 bila token missing/invalid.
- [] Mock Redis client dapat di‑inject dan dipanggil tanpa error.
- [] Coverage ≥ 85 % pada folder `dependencies`.

## Status
- [ ] Pending
