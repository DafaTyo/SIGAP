# 📌 Module Task Tracker: API Router Package (backend/app/api)

## 🎯 Core Objective & Responsibility
- Menyediakan **router FastAPI** yang meng‑expose endpoint untuk masing‑masing domain (vendor, distribution, complaint).
- Menjaga *thin* transport layer: hanya delegasi ke service layer di masing‑domain.
- Memastikan **dependency injection** (DB session, JWT user, rate‑limit, audit) melalui `Depends`.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` yang meng‑import semua router (`vendor_router`, `distribution_router`, `complaint_router`).
- [ ] **Vendor Router** – `vendor.py`
  - **Endpoints:** `POST /vendors`, `GET /vendors`, `GET /vendors/{vendor_id}`, `PATCH /vendors/{vendor_id}`, `GET /vendors/{vendor_id}/nik`.
  - **Parameters:** `Depends` pada `db_session`, `current_user`, `idempotency_key`.
  - **Responses:** Menggunakan schema `VendorRead` (masked) dan `VendorNikReveal` (restricted).
- [ ] **Distribution Router** – `distribution.py`
  - **Endpoints:** `POST /distribution`, `GET /distribution/{id}`, `GET /distribution/vendor/{vendor_id}`.
  - **Special:** Header `X‑Idempotency-Key`, streaming status via SSE (`/distribution/{id}/status/stream`).
- [ ] **Complaint Router** – `complaint.py`
  - **Endpoints:** `POST /complaint`, `GET /complaint/{id}`, `PATCH /complaint/{id}/status`, `POST /complaint/{id}/assign`.
  - **Public Access:** `GET /complaint/public/{id}` (tanpa auth, hanya read‑only).
- [ ] **Add OpenAPI Tags** – set `tags` pada setiap router (`Vendor`, `Distribution`, `Complaint`).
- [ ] **Add Security Definitions** – memastikan `security` = `bearerAuth` untuk endpoint yang memerlukan autentikasi.
- [ ] **Write Router README** – menjelaskan konvensi penamaan, dependency injection, dan contoh penggunaan.

## 🔒 Constraints & Best Practices
- **No Business Logic:** Semua keputusan bisnis harus dialihkan ke `backend/app/domains/*/services.py`.
- **Idempotency Middleware:** Pastikan setiap endpoint mutasi meng‑akses header `X‑Idempotency‑Key` sebelum memanggil service.
- **Rate‑limit Decorator:** Gunakan `@rate_limit(limit=... )` pada endpoint yang berpotensi berat.
- **Testing:** Buat integration test di `backend/app/tests/api/` yang mem‑boot FastAPI app dengan in‑memory SQLite.

## 📄 References
- `api-contract.yaml` – sumber definitive endpoint definitions.
- `backend/app/middleware/` – middleware yang di‑apply (audit, rls, opa, idempotency, rate‑limit).
- `backend/app/dependencies/` – DB session, JWT user extraction.

---

**Instruksi Eksplisit:** Kode router (Python) **tidak boleh** ditulis sebelum semua checklist di atas di‑centang sebagai selesai.
