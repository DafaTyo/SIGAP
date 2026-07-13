# TASK.md – Backend/tests/utils

## Goals
- Unit‑test semua helper di `backend/app/utils` (pagination, datetime, uuid, error wrapper).
- Pastikan helper **type‑safe** dan tidak menimbulkan side‑effects.

## Verification Criteria
- [] `utils.pagination.paginate` menghasilkan `items` slice yang benar sesuai `limit`/`offset`.
- [] `utils.datetime.now_utc` mengembalikan timezone‑aware datetime dengan tzinfo UTC.
- [] `utils.errors` meng‑wrap exception menjadi `AppError` dengan kode dan status yang tepat.
- [] Coverage ≥ 95 % pada folder `utils`.

## Status
- [ ] Pending
