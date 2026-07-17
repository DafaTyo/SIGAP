# 📋 SIGAP CONTEXT SUMMARY

## A. Executive Summary (Proof of Context)

### Tujuan Produk
1. **Tujuan Strategis**: Membangun ekosistem tata kelola vendor yang transparan, akuntabel, dan terautomasi untuk memastikan distribusi Program Makan Bergizi Gratis berjalan tepat sasaran, higienis, dan bebas dari anomali/fraud (IDEA.md:3-6, PRD_SIGAP.md:13-14).

2. **Tiga Pilar Solusi**: 
   - **Verifikasi (perizinan digital)**: Mempercepat verifikasi vendor melalui integrasi asinkron dengan sistem pemerintah (IDEA.md:20-26)
   - **Pengawasan (monitoring + vendor scoring real-time)**: Mendeteksi anomali distribusi menggunakan AI berbasis probabilitas (IDEA.md:20-26)
   - **Akuntabilitas (pengaduan publik dengan SLA)**: Menyediakan kanal pengaduan transparan dengan sistem tracking tiket (IDEA.md:20-26)

3. **Lingkup MVP**: Portal Perizinan Vendor, Dashboard Monitoring Distribusi, dan Sistem Pengaduan Publik (IDEA.md:27-31, PRD_SIGAP.md:101-106)

### Batasan Arsitektur Wajib
1. **Arsitektur Modular Monolith**: Next.js sebagai BFF + Backend Python (FastAPI) + PostgreSQL RLS + OPA/CASL (IDEA.md:32-38, DESIGN.md:4-5)

2. **Row-Level Security (RLS)**: PostgreSQL dengan `SET LOCAL app.current_user_id` dan `SET LOCAL app.current_scope` per-request untuk isolasi wilayah (DESIGN.md:19-21, api-contract.yaml:1144-1147)

3. **Open Policy Agent (OPA)**: Mesin kebijakan ABAC terpusat untuk evaluasi izin kompleks (DESIGN.md:23-24)

4. **PII Masking**: NIK di-encrypt di database (pgcrypto AES-256) dan di-mask secara dinamis di level BFF sebelum response dikirim ke klien (PRD_SIGAP.md:47, api-contract.yaml:144-149)

5. **X‑Idempotency‑Key**: Header wajib `X-Idempotency-Key` (UUID v4) untuk semua operasi state-changing (POST/PATCH/DELETE) dengan window 24 jam (api-contract.yaml:903-918)

### Alur Data Kritis NIK
1. **Registraasi → Enkripsi**: NIK mentah diterima di `VendorRegistrationRequest` dan disimpan terenkripsi (pgcrypto AES-256) (api-contract.yaml:144-149)

2. **Response Masked**: Schema `Vendor` hanya berisi `nik_penanggung_jawab_masked` (4 digit awal + 4 digit akhir), NIK mentah TIDAK PERNAH muncul di objek response (api-contract.yaml:1057-1077)

3. **Reveal via OPA**: Hanya endpoint `GET /vendors/{vendorId}/nik` yang mengembalikan NIK mentah, diwajibkan role `admin/verifikator_bgn` dan menghasilkan audit log `action=PII_REVEAL` (api-contract.yaml:284-312)

## B. Audit TASK.md

### 📊 Overview
| Folder | TASK.md ada? | Format valid? | Total item | Selesai | % | Anomali |
|---|---|---|---|---|---|---|---|
| 28 folders total | ✅ Ya (semua) | ❌ TIDAK VALID (semua) | 0 | 0 | 0% | ❌ Missing sections |

### 🔍 Detail Anomali
- **Jumlah TASK.md**: 28 folder dengan file TASK.md yang ada
- **Format issue**: Semua file missing 4 required sections:
  - 🎯 Core Objective & Responsibility
  - 📋 Development Checklist  
  - 🔒 Constraints & Best Practices
  - 📄 References
- **Checklist items**: Total 0 items (semua kosong)
- **Format compliance**: 0% (28/28 invalid)

## C. Cross-Reference Matrix

### Endpoint → Folder TASK.md
- `/vendors/*` → `backend/app/domains/vendor/TASK.md`
- `/distributions/*` → `backend/app/domains/distribution/TASK.md`  
- `/complaints/*` → `backend/app/domains/complaint/TASK.md`
- `/auth/*` → `backend/app/api/TASK.md`

### Domain Entity → Related TASK.md
- **Vendor**: `backend/app/domains/vendor/TASK.md`, `backend/app/api/TASK.md`
- **Distribution**: `backend/app/domains/distribution/TASK.md`, `backend/app/api/TASK.md`
- **Complaint**: `backend/app/domains/complaint/TASK.md`, `backend/app/api/TASK.md`

### Kebijakan Data Governance → Implementing TASK.md
- **NIK Encryption**: `backend/app/utils/TASK.md`, `backend/app/domains/vendor/TASK.md`, `data/migrations/TASK.md`
- **RLS**: `backend/app/middleware/TASK.md`, `data/migrations/TASK.md`
- **OPA Policies**: `backend/app/policies/TASK.md`, `backend/app/middleware/TASK.md`

## D. Inkonsistensi & Gap

### ⚠️ Kritis (menghambat coding)
1. **Format TASK.md**: Semua 28 file TASK.md missing required sections →Tidak ada rencana pengembangan
2. **Indeks API Contract**: Endpoint paths vs TASK.md path naming tidak konsisten

### ⚠️ Minor (dapat ditolerir & diperbaiki saat coding)
1. **Status enum**: Varian status (pending_verification, verified, rejected, suspended) vs status lokal
2. **Role naming**: admin/verifikator_bgn vs verifikator

## E. Gatekeeper Statement

> **BELUM SIAP** mengeksekusi **Layer 1 — Fondasi & Pengamanan** karena:

1. **TASK.md tidak ada**: 28 folder memiliki file TASK.md yang tidak valid, menjelaskan alur kerja pengembangan dan checklist progreso secara memadai.
2. **Implementasi belum dimulai**: Tidak ada checklist progress apapun di semua TASK.md files, meskipun API Contract dan arsitekturnya sudah final.
3. **Documentasi gap**: Kebijakan kritis (RLS, OPA, PII Encryption) tidak punya dokumentasi TASK.md sendiri untuk verifikasi progres.

**Prasyarat yang harus diputuskan Kuma terlebih dahulu**:
1. **Perbaiki TASK.md format**: Audit semua 28 TASK.md files untuk memenuhi format 4-section wajib
2. **Isi Development Checklist**: Populasi checklist untuk semua domain dan API endpoints
3. **Putuskan cross-reference gaps**: Tentukan TASK.md owners untuk semua kebijakan (
   RLS, OPA, PII Encryption, dll.)

Sampai ketiga items di atas selesai, tidak ada Layer 2 (Development) bisa dimulai — semua Task-Driven Development terhenti di gate validasi TASK.md.

---

## 📚 Daftar Dokumen yang Berhasil di‑baca
- `[IDEA.md](C:/SIGAP/docs/IDEA.md)` (89 lines, 4,805 chars)
- `[PRD_SIGAP.md](C:/SIGAP/docs/PRD_SIGAP.md)` (113 lines, 7,896 chars)  
- `[DESIGN.md](C:/SIGAP/docs/DESIGN.md)` (79 lines, 3,917 chars)
- `[DATA_GOVERNANCE.md](C:/SIGAP/docs/DATA_GOVERNANCE.md)` (lihat missing sections)
- `[api-contract.yaml](C:/SIGAP/api-contract.yaml)` (1,597 lines, 47,318 chars)
- `[TASK.md](C:/SIGAP/TASK.md)` (root) (lihat missing sections)

## 🔌 Daftar endpoint API (tabel ringkas)
| Path | Method | Tag | Idempotency |
|---|---|---|---|
| /auth/login | POST | Auth | ❌ |
| /vendors | POST | Vendor | ✅ |
| /vendors | GET | Vendor | ❌ |
| /distributions | POST | Distribution | ✅ |

## 📋 Kebijakan data governance yang mengikat kode
1. **NIK Encryption**: `pgcrypto AES-256` di database, masking di BFF layer
2. **Geospatial Validation**: PostGIS `ST_DWithin` di server, radius field tidak diterima dari klien
3. **Row-Level Security**: `SET LOCAL app.current_user_id/scope` per-request di RLS middleware
4. **Audit Logging**: Global middleware capture semua mutation dengan diff (old/new values)
5. **Idempotency**: 24 jam window, Pencegahan duplicate state changes
6. **PII Reveal**: Audit log khusus `action=PII_REVEAL` untuk endpoint reveal

## 📚 Glossary
- **RLS**: Row-Level Security — isolasi data berdasarkan scope user
- **OPA**: Open Policy Agent — mesin kebijakan ABAC
- **ABAC**: Attribute-Based Access Control — izin berbasis atribut
- **PII_REVEAL**: Audit log action untuk pengungkapan data pribadi sensitif
- **SIO**: Surat Izin Operasional Digital — QR Code unik
- **BFF**: Backend-for-Frontend — Next.js Server Actions layer
- **PostGIS**: Ekstensi geospatial untuk PostgreSQL
- **pgcrypto**: Fungsi crypto PostgreSQL untuk enkripsi data sensitif
- **Task-Driven Development**: Metodologi pengembangan SIGAP — TASK.md sheets per folder