# 📌 Module Task Tracker: Utils Package (backend/app/utils)

## 🎯 Core Objective & Responsibility
- Provide reusable utility functions for handling personally identifiable information (PII), notably NIK masking and encryption placeholders.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` re‑exports helpers.
- [x] **PII utilities** – `pii.py` with `mask_nik`, `encrypt_nik`, `decrypt_nik` stubs.

## 🔒 Constraints & Best Practices
- `mask_nik` must never expose the full NIK; short strings are masked by half‑length.
- Encryption/decryption functions are **stubs** that raise `NotImplementedError` until integrated with a DB session.
- Utilities must be pure functions without side‑effects.

## 📄 References
- `api-contract.yaml` – masking rules for `nik_penanggung_jawab_masked`.
- `docs/DATA_GOVERNANCE.md` – PII classification and encryption requirements.
