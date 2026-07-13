# TASK.md – Backend/tests/services

## Goals
- Unit‑test semua service class/function secara **isolated** (mock DB session, mock OPA client).
- Pastikan service menangani error dengan **AppError** yang tepat.
- Validasi **business rules** (mis. vendor cannot be deleted if active contracts exist).

## Verification Criteria
- [] Setiap service memiliki minimal 3 test case (happy path, validation error, business rule violation).
- [] Coverage pada `services/` ≥ 90 %.
- [] CI men‑run `pytest backend/tests/services` dan gagal bila coverage < 90 %.

## Status
- [ ] Pending
