# 📌 Module Task Tracker: Data Seeds (data/seeds)

## 🎯 Core Objective & Responsibility
- Menyimpan **seed data** JSON yang berisi contoh entitas awal (vendors, users, roles) untuk populasi database pada environment development atau CI.
- Data harus **idempotent** – bila seed dijalankan lebih dari satu kali tidak menambah duplikat.

## 📋 Development Checklist
- [ ] **Add placeholder JSON** – `vendors_initial.json`
  - Contoh 3 vendor dengan NIK terenkripsi (hex string placeholder), status `verified`.
- [ ] **Add users JSON** – `users_initial.json`
  - Daftar user (admin, verifikator, pengawas) dengan hashed password (bcrypt placeholder).
- [ ] **Write Seeds README** – cara menjalankan seed via `infra/scripts/seed.sh` atau FastAPI admin endpoint.
- [ ] **Add .gitkeep** (optional) to keep folder tracked when empty.

## 🔒 Constraints & Best Practices
- **Never store real secrets** – gunakan dummy values, hash placeholder.
- **Version control:** setiap perubahan seed berpotensi memengaruhi migration test, beri tag versi.
- **Validation:** schema validation dengan Pydantic (`seed_schema.py`) – not required for now but mention.

## 📄 References
- `docs/DATA_GOVERNANCE.md` – aturan data pribadi.
- `backend/app/domains/vendor/models.py` – field list untuk menyesuaikan seed.

---

**Instruksi Eksplisit:** Tidak menambahkan file JSON seed sampai semua checklist di atas selesai.
