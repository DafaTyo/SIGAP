# 📌 Module Task Tracker: Workers Package (backend/workers/validate_documents)

## 🎯 Core Objective & Responsibility
- Mengimplementasikan **worker** yang memproses validasi dokumen legal vendor secara asynchronous.
- Menggunakan **Redis queue** (Celery/ARQ) untuk men‑enqueue job ketika vendor meng‑upload dokumen.
- Mengirimkan status via **Server‑Sent Events (SSE)** atau **WebSocket** ke frontend.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` (expose worker entrypoint).
- [ ] **Worker entrypoint** – `worker.py`
  - **Function:** `process_document(vendor_id: UUID, document_type: str, file_path: str)`
  - **Steps:**
    1. Download file dari storage (local atau S3).
    2. Call external API OSS/BPOM (mockable).
    3. Update `DocumentValidationStatus` di DB (`pending`, `valid`, `invalid`).
    4. Publish status to SSE channel `/vendors/{id}/documents/{doc_id}/status/stream`.
- [ ] **Task Scheduler** – `tasks.py`
  - Register worker with Celery/ARQ (`@celery.task` atau `@arq_job`).
- [ ] **Error handling** – retry dengan backoff exponential, cap maksimal 3 retries.
- [ ] **Write Worker README** – cara menjalankan worker container, environment vars (`REDIS_URL`, `EXTERNAL_API_KEY`).

## 🔒 Constraints & Best Practices
- **Idempotent processing:** Jika dokumen sudah `valid` atau `invalid`, skip re‑processing.
- **Timeout:** set maksimal 5 menit per dokumen; kirim `status = "failed"` bila timeout.
- **Security:** Jangan log isi file mentah; hanya log hash SHA256.
- **Testing:** Mock external API via `responses` library; unit‑test worker logic in `backend/tests/workers/`.

## 📄 References
- `api-contract.yaml` – endpoint `/vendors/{vendorId}/documents/{documentId}/status` & `/status/stream`.
- `docs/DATA_GOVERNANCE.md` – kebijakan penyimpanan dokumen & audit.
- `backend/app/middleware/audit_log.py` – pastikan setiap status update tercatat.

---

**Instruksi Eksplisit:** Kode worker (Python) **tidak boleh** ditulis sampai semua item checklist di atas di‑centang selesai.
