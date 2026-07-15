# 📌 Module Task Tracker: Vendor Domain (backend/app/domains/vendor)

## 🎯 Core Objective & Responsibility
- Mengelola entitas **Vendor**: model, schema, service, repository, dan policy.
- Menjamin **PII masking**, **enkripsi NIK**, dan **ABAC** via OPA.
- Menyediakan endpoint CRUD yang sesuai dengan `api‑contract.yaml`.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` (expose nama modul).
- [ ] **Model** – `models.py`
  - **Class:** `Vendor`
  - **Fields:** `id (UUID)`, `name`, `nik_encrypted (BYTEA)`, `nik_masked (VARCHAR)`, `status`, `created_at`, `updated_at`.
  - **Constraints:** `unique(name)`, `check (status in ('pending','verified','rejected'))`.
- [ ] **Schema (Pydantic)** – `schemas.py`
  - **Classes:** `VendorCreate`, `VendorUpdate`, `VendorRead` (masking `nik_masked`).
- [ ] **Repository** – `repositories.py`
  - **Functions:** `get_vendor`, `list_vendors`, `create_vendor`, `update_vendor`, `delete_vendor`.
  - **All queries** harus men‑set `app.current_user_id` & `app.current_scope` (RLS).
- [ ] **Service** – `services.py`
  - **Functions:** `register_vendor`, `verify_document`, `reveal_nik` (restricted). 
  - **Input:** DTOs dari `schemas.py`.
  - **Output:** `VendorRead` atau error `HTTPException`.
- [ ] **Policy** – `policies.py`
  - **Function:** `can_view_nik(user, vendor)` → pemanggilan OPA policy `sgp.rego`.
- [ ] **Task Documentation** – `README.md` di folder menjelaskan alur data flow (controller → service → repo → model).

## 🔒 Constraints & Best Practices
- **Idempotency:** Semua operasi mutasi harus memeriksa header `X‑Idempotency‑Key` (middleware di `backend/app/middleware/idempotency`).
- **Encryption:** Gunakan `pgcrypto` (`crypt` extension) untuk `nik_encrypted`; masking hasil di `utils.mask_pii`.
- **ABAC:** Policy OPA harus dipanggil sebelum mengembalikan NIK mentah; hanya `admin` atau `verifikator_bgn` yang boleh.
- **Testing:** Unit‑test untuk setiap fungsi di `backend/app/tests/vendor/` (fixtures DB transaksi, mock OPA). 

## 📄 References
- `api-contract.yaml` → endpoint `/vendors` & `/vendors/{vendorId}/nik`.
- `docs/DATA_GOVERNANCE.md` → aturan PII & enkripsi.
- `docs/DESIGN.md` → diagram alur RLS & OPA.

---

**Instruksi Eksplisit:** Kode Python **tidak boleh** ditulis sampai semua item checklist di atas di‑ceklist sebagai selesai.
