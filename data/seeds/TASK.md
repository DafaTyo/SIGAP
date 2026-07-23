# 📌 Module Task Tracker: Seeds Folder (data/seeds)

## 🎯 Core Objective & Responsibility
- Menyediakan seed data untuk development dan testing: vendor dummy, user test, sample complaints, distribusi sample.
- Seed data harus aman (tidak mengandung PII asli) dan siap dipakai untuk demo MVP.

## 📋 Development Checklist
- [ ] **Vendor seeds** – 3 vendor sample (verified, pending, rejected).
- [ ] **User seeds** – 5 user sample (admin, verifikator_bgn, pengawas_dinas, vendor, masyarakat).
- [ ] **Distribution seeds** – 10 sample laporan distribusi dengan berbagai status.
- [ ] **Complaint seeds** – 5 sample pengaduan dengan severity berbeda.
- [ ] **Shell script** – `seed.sh` yang menjalankan seeding via psql.

## 🔒 Constraints & Best Practices
- Semua NIK di seed data adalah dummy (sesuai format NIK tapi tidak asli).
- Koordinat geografis menggunakan titik real di wilayah Indonesia.
- Password user dummy: `password123` (hashing dengan bcrypt).

## 📄 References
- `api-contract.yaml` – schema data untuk validasi format.
- `data/migrations/0001_enable_pgcrypto_and_rls.sql` – struktur tabel tujuan.
