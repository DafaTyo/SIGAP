# 📌 Module Task Tracker: Core Package (backend/app/core)

## 🎯 Core Objective & Responsibility
- Menyediakan fondasi shared untuk seluruh aplikasi FastAPI: konfigurasi environment, logging terstruktur, dan error classes yang konsisten.

## 📋 Development Checklist
- [x] **Config** – `config.py` memuat env via `pydantic-settings`, mencakup DB/Redis/JWT/OPA/RateLimit/Idempotency.
- [x] **Logger** – `logger.py` mengembalikan JSON logger berbasis `structlog` dengan `request_id`.
- [ ] **Validasi startup** – pastikan FastAPI startup memanggil `configure_logging()`.
- [ ] **Secret rotation docs** – tambahkan prosedur rotasi `JWT_SECRET_KEY` dan `NIK_ENCRYPTION_KEY`.

## 🔒 Constraints & Best Practices
- Jangan hardcode secret di kode; semua lewat `.env`.
- Logger hanya menulis metadata, bukan PII mentah.
- Gunakan exception classes khusus domain, bukan `Exception` generik.

## 📄 References
- `api-contract.yaml` – security schemes, error format.
- `docs/DESIGN.md` – layer architecture.
- `docs/DATA_GOVERNANCE.md` – audit & logging.
