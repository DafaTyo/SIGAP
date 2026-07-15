# 📌 Module Task Tracker: Policies Package (backend/app/policies)

## 🎯 Core Objective & Responsibility
- Menyimpan **OPA/Rego policy files** yang mengatur ABAC (Attribute‑Based Access Control) untuk seluruh modul.
- Memastikan kebijakan dapat **di‑version‑control** bersama kode.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` (optional, hanya untuk import convenience).
- [ ] **Create Rego policy file** – `sgp.rego`
  - Definisikan policy `allow` yang memeriksa `input.user.role`, `input.user.scope`, dan `input.resource.type`.
  - Contoh rule: `allow { input.user.role == "admin" }` atau `allow { input.user.role == "pengawas_dinas"; input.user.province == input.resource.province }`.
- [ ] **Write policy README** – cara menjalankan OPA server (`docker run -p 8181:8181 openpolicyagent/opa eval ...`), dan contoh query dari FastAPI middleware.
- [ ] **Add unit test for policy** – gunakan `opa-test` atau script Python yang meng‑POST ke OPA container.

## 🔒 Constraints & Best Practices
- **Policy granularity:** Setiap resource (vendor, distribution, complaint) memiliki namespace terpisah dalam Rego (`vendor`, `distribution`, `complaint`).
- **Versioning:** Setiap perubahan policy harus diberi *semantic version* dalam commit message (`policy: bump to v1.2`).
- **Performance:** Cache hasil evaluation per request (5 seconds) di middleware.

## 📄 References
- `docs/DESIGN.md` – security architecture (OPA, RLS).
- `api-contract.yaml` – requirement untuk authorization.

---

**Instruksi Eksplisit:** Tidak menulis file Rego atau kode Python sampai semua poin di atas di‑centang selesai.
