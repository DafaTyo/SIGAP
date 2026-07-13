# TASK.md – Backend/core

## Goals
- Centralize konfigurasi aplikasi: **settings** (pydantic BaseSettings), **logger** (structlog/JSON), dan **dependency injection container**.
- Implementasikan **CORS**, **GZip**, **Security‑Headers**, **Request‑ID**, serta **OPA policy middleware** pada level FastAPI (diletakkan di `main.py`).
- Pastikan semua konfigurasi dapat di‑override via environment variables (`.env.example`).

## Verification Criteria
- [] Settings dapat dimuat (`Settings()`), memvalidasi required vars (`DB_URL`, `OPA_URL`, `JWT_SECRET`).
- [] Logger mengoutput JSON ke stdout, termasuk `request_id`.
- [] Middleware stack ter‑registrasi di `app/main.py` (FastAPI `add_middleware`).
- [] Unit‑test (`pytest backend/tests/core`) memverifikasi bahwa `Settings` meng‑raise error bila var penting hilang.
- [] Coverage ≥ 85 % pada folder `core`.

## Status
- [ ] Pending
