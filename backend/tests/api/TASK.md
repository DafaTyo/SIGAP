# TASK.md – Backend/tests/api

## Goals
- Unit‑test semua endpoint FastAPI (CRUD, auth, audit) dengan **TestClient**.
- Pastikan **security** (JWT, OPA) bekerja: request tanpa token → 401, request dengan role tidak cukup → 403.
- Gunakan **fixtures** untuk DB isolation (transaction rollback per test).

## Verification Criteria
- [] Semua endpoint memiliki setidaknya satu test case yang berhasil (`200/201/204`).
- [] Test coverage pada `api/` ≥ 90 %.
- [] CI pipeline (`ci.yml`) menjalankan `pytest backend/tests/api` dan gagal bila coverage < 90 %.

## Status
- [ ] Pending
