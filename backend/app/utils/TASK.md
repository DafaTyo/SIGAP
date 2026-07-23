# 📌 Module Task Tracker: Utils Package (backend/app/utils)

## 🎯 Core Objective & Responsibility
- Menyediakan utilitas shared yang reusable antar domain: masking PII, validasi geospasial, dan helper format.

## 📋 Development Checklist
- [x] **PII masking** – `pii.py` berisi `mask_nik`, `encrypt_nik`, `decrypt_nik`.
- [ ] **Geospatial helpers** – tambahkan validasi koordinat dan helper PostGIS query.
- [ ] **Ticket generator** – helper pembuatan nomor tiket pengaduan yang idempoten.
- [ ] **EXIF parser** – helper ekstraksi metadata foto untuk tampering detection.

## 🔒 Constraints & Best Practices
- `encrypt_nik`/`decrypt_nik` harus memakai `pgcrypto` via SQLAlchemy text(), bukan cryptography library sendiri.
- Masking pattern NIK: 4 digit awal + 8 bintang + 4 digit akhir.
- Utils tidak boleh mengimpor domain-specific code (hindari circular import).

## 📄 References
- `docs/DATA_GOVERNANCE.md` – §3 PII classification & masking.
- `api-contract.yaml` – schema `VendorNikReveal`.
- `docs/DESIGN.md` – PostGIS usage.
