# TASK.md – Backend/services

## Goals
- Implement **business‑logic layer** yang pure‑Python (tidak bergantung pada FastAPI). Contoh: `VendorService`, `ContractService`.
- Pastikan service dapat dipanggil secara terpisah dalam unit‑test (mock DB session).
- Integrasikan **OPA policy evaluation** di level service (opsional, bila perlu validasi domain).

## Verification Criteria
- [] Service `create_vendor`, `update_vendor`, `delete_vendor` mengembalikan DTO yang sudah divalidasi.
- [] Semua service memiliki **unit‑test** yang mem‑mock DB dan OPA (`pytest backend/tests/services`).
- [] Coverage ≥ 90 % pada folder `services`.
- [] Service tidak men‑raise generic `Exception`; gunakan custom `AppError` (lihat folder `exceptions`).

## Status
- [ ] Pending
