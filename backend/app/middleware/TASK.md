# 📌 Module Task Tracker: Middleware Package (backend/app/middleware)

## 🎯 Core Objective & Responsibility
- Menyediakan **FastAPI middleware** yang menangani cross‑cutting concerns:
  - Audit logging
  - Row‑Level Security (RLS) context setter
  - OPA policy evaluation
  - Idempotency handling
  - Rate limiting
- Middleware bersifat **stateless** dan dapat dipasang di urutan yang konsisten pada aplikasi utama.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` yang meng‑export semua middleware class.
- [ ] **Audit Log Middleware** – `audit_log.py`
  - **Functionality:** Capture `request.method`, `path`, `user.id`, `old_value`, `new_value`; insert ke tabel `audit_logs`.
  - **Input:** `request`, `response` objects.
  - **Output:** Tidak mengubah response, hanya men‑insert log.
- [ ] **RLS Setter Middleware** – `rls_setter.py`
  - **Functionality:** Pada setiap request, jalankan `SET LOCAL app.current_user_id = <user_id>; SET LOCAL app.current_scope = <province>` pada DB connection (via SQLAlchemy event).
- [ ] **OPA Policy Middleware** – `opa_policy.py`
  - **Functionality:** Memanggil OPA server (`http://opa:8181/v1/data/sigap/auth/allow`) dengan payload `{user, action, resource}`; menolak dengan `HTTPException(403)` bila tidak diizinkan.
- [ ] **Idempotency Middleware** – `idempotency.py`
  - **Functionality:** Simpan `idempotency_key` di Redis; jika key sudah ada, kembalikan response yang tersimpan.
- [ ] **Rate Limit Middleware** – `rate_limit.py`
  - **Functionality:** Batas request per IP/ per user (configurable via env `RATE_LIMIT_*`).
- [ ] **Write Middleware README** – menjelaskan urutan pemasangan, konfigurasi env, dan contoh penggunaan dalam `backend/app/main.py`.

## 🔒 Constraints & Best Practices
- **Order matters:** AuditLog → Idempotency → RateLimit → OPA → RLS (set before DB queries).
- **No DB commit** dalam middleware kecuali `audit_log` (gunakan separate connection/transaction).
- **Performance:** Cache OPA decisions per request for 5 seconds to reduce remote calls.
- **Testing:** Mock OPA server & Redis in `backend/app/tests/middleware/`.

## 📄 References
- `docs/DESIGN.md` – bagian *Security Architecture* (RLS, OPA, masking).
- `api-contract.yaml` – header requirements (idempotency, rate‑limit).
- `backend/app/policies/sgp.rego` – contoh policy yang akan dipanggil.

---

**Instruksi Eksplisit:** Tidak ada kode middleware yang boleh ditulis sebelum semua poin di atas ditandai selesai.
