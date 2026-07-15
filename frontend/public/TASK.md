# 📌 Module Task Tracker: Public Assets (frontend/public)

## 🎯 Core Objective & Responsibility
- Menyimpan **static assets** yang akan dilayani oleh Next.js secara langsung (favicon, logo, gambar ilustrasi, robots.txt).
- Tidak mengandung kode eksekusi, hanya file‑binary atau teks.

## 📋 Development Checklist
- [ ] **Create placeholder assets** – `favicon.ico`, `logo.svg`, `robots.txt` (dummy content).
- [ ] **Add README.md** – menjelaskan konvensi penamaan (`*.png` untuk UI icons, `*.svg` untuk vector, `*.ico` untuk favicon) dan cara men‑add asset ke repo.
- [ ] **Add .gitkeep** (optional) jika folder akan tetap kosong pada awal commit.

## 🔒 Constraints & Best Practices
- **Size limit:** tidak ada file > 150 KB untuk menjaga bundle size.
- **Naming:** gunakan lower‑kebab‑case (`my-logo.svg`).
- **Performance:** compress PNG/JPEG dengan lossless tools sebelum commit.

## 📄 References
- `docs/DESIGN.md` – bagian *UI/UX Assets*.

---

**Instruksi Eksplisit:** Tidak ada file kode yang boleh dibuat di dalam `frontend/public` sampai semua checklist di atas selesai.
