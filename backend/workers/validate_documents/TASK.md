# TASK‑BE‑011‑04 – Background Worker for OSS/BPOM Validation

## Goals
- Implement **Redis‑based worker** (using **ARQ** atau **Celery**) yang meng‑konsumsi job `validate_external_documents`.
- Job mengambil payload dokumen (NIB, PIRT, Sertifikat Halal) dan memanggil API eksternal OSS/BPOM.
- Hasil validasi (status `valid`/`invalid` + detail) disimpan di tabel `legal_documents`.
- Worker dijalankan secara **asynchronous**, tidak memblokir request BFF.
- Pastikan worker dapat di‑scale (multiple workers) dan memiliki retry/back‑off.

## Verification Criteria
- [] Worker dapat dijalankan dengan perintah `python -m workers.validate_documents` (script starter).
- [] Unit test `tests/workers/test_validate_documents.py` menggunakan mock HTTP ke OSS/BPOM dan memverifikasi penyimpanan hasil di DB.
- [] CI pipeline men‑run worker test dalam environment dengan Redis mock (e.g., `fakeredis`).
- [] Dokumentasi `README.md` di folder `workers/` menjelaskan cara menjalankan worker di dev & prod.

## Status
- [] Pending