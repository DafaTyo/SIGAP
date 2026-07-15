# 📌 Module Task Tracker: Complaint Domain (backend/app/domains/complaint)

## 🎯 Core Objective & Responsibility
- Menangani entitas **Complaint** (pengaduan publik) beserta alur tiket, prioritas, dan status penyelesaian.
- Memastikan **privacy** dan **audit‑log** pada setiap perubahan status.
- Menyediakan endpoint yang dapat diakses baik oleh user anonim maupun pengguna ter‑autentikasi.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` (expose modul).
- [ ] **Model** – `models.py`
  - **Class:** `Complaint`
  - **Fields:** `id (UUID)`, `reporter_name`, `reporter_email`, `photo_path`, `description`, `severity (enum)`, `status (enum)`, `assigned_to (FK to user)`, `created_at`, `updated_at`.
  - **Constraints:** `check (severity in ('low','medium','high','critical'))`, `check (status in ('open','in_progress','resolved','closed'))`.
- [ ] **Schema** – `schemas.py`
  - **Classes:** `ComplaintCreate`, `ComplaintRead`, `ComplaintUpdate`.
- [ ] **Repository** – `repositories.py`
  - **Functions:** `create_complaint`, `get_complaint`, `list_complaints`, `update_status`, `assign_complaint`.
- [ ] **Service** – `services.py`
  - **Functions:** `submit_complaint`, `change_status`, `assign_to_user`, `add_note` (optional).
- [ ] **Policy** – `policies.py`
  - **Function:** `can_view_complaint(user, complaint)` → OPA check berdasarkan scope wilayah dan role.
- [ ] **Task Documentation** – `README.md` menjelaskan alur: Public Form → API → Service → Repo → Audit.

## 🔒 Constraints & Best Practices
- **Anonimity:** Jika user tidak login, hanya field non‑identifying yang disimpan (`reporter_name` opsional, `reporter_email` optional).
- **PII Masking:** Semua field PII (email) harus disimpan dengan hashing jika anonim, atau dienkripsi bila diperlukan.
- **Audit Log:** Middleware `audit_log` wajib men‑log setiap `PATCH /complaint/{id}` dengan `old_value`/`new_value`.
- **Idempotency:** `POST /complaint` harus menerima `X‑Idempotency‑Key` untuk menghindari duplikat laporan.
- **Rate‑limit:** 5 pengaduan per menit per IP (middleware `rate_limit`).
- **Testing:** Unit‑test di `backend/app/tests/complaint/` meliputi validasi schema, policy check, dan audit record.

## 📄 References
- `api-contract.yaml` → endpoint `/complaint` dan `/complaint/{id}`.
- `docs/DESIGN.md` – bagian *Public Complaint Module*.
- `docs/DATA_GOVERNANCE.md` – kebijakan penyimpanan foto & data pribadi.

---

**Instruksi Eksplisit:** Tidak ada file kode yang boleh ditulis sampai semua poin checklist di atas ditandai selesai (`[x]`).
