# 📌 Module Task Tracker: Policies Package (backend/app/policies)

## 🎯 Core Objective & Responsibility
- Menyimpan kebijakan OPA/ABAC yang dievaluasi untuk menentukan akses user terhadap resource.

## 📋 Development Checklist
- [ ] **OPA policy file** – buat `policies/sigap.rego` minimal untuk Vendor/Distribution/Complaint.
- [ ] **Unit test policy** – verifikasi decision untuk tiap role (vendor, verifikator_bgn, pengawas_dinas, admin).
- [ ] **Sync CASL** – endpoint `/auth/me/permissions` harus cocok dengan policy OPA untuk UI.
- [ ] **Fallback mode** – implementasi fallback policy bila OPA unreachable untuk dev/testing.

## 🔒 Constraints & Best Practices
- Fail-closed: jika OPA gagal, tolak akses (403).
- Policy hanya memakai atribusi, bukan hardcode role-check di Python.
- Jangan kembalikan `result: true` untuk operasi sensitif tanpa validasi scope.

## 📄 References
- `docs/DESIGN.md` – §2.2 OPA & CASL.
- `docs/DATA_GOVERNANCE.md` – §7 Access Control.
- `api-contract.yaml` – endpoint yang butuh bearerAuth.
