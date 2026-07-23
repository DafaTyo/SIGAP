# 📌 Module Task Tracker: Frontend Actions (frontend/src/actions)

## 🎯 Core Objective & Responsibility
- Server Actions Next.js (App Router) yang menjadi gateway utama frontend menuju API backend.
- Setiap action wajib mencantumkan inkimentiditas kunci (X-Idempotency-Key) dan masking PII sebelum dikirim ke client.

## 📋 Development Checklist
- [ ] **auth/login** – Login JWT untuk vendor, verifikator BGN, pengawas dinas, admin.
- [ ] **auth/logout** – Blacklist token.
- [ ] **vendor/submit-registration** – Submit form registrasi sesuai `VendorRegistrationRequest`.
- [ ] **vendor/upload-document** – Upload dokumen legal (NIK, NIB, PIRT, dll.) dengan progress status via SSE/websocket.
- [ ] **vendor/list** – Ambil list vendor sesuai scope role.
- [ ] **distribution/submit-report** – Submit laporan distribusi dengan foto dan koordinat GPS.
- [ ] **distribution/list** – List laporan distribusi yang bisa diakses berdasarkan scope.
- [ ] **complaint/submit** – Submit pengaduan masyarakat (publik) tanpa login.
- [ ] **complaint/track** – Public tracking per tiket dan status pengaduan.
- [ ] **public/vendor-verify** – Verify keabsahan vendor via kode SIO.
- [ ] **public/dashboard/summary** – Data agregat publik (total vendor, pengaduan, distribusi).

## 🔒 Constraints & Best Practices
- Semua mutation (POST, PATCH, DELETE) wajib set `X-Idempotency-Key` header.
- PII masking diterapkan setelah response didapat dari FastAPI (DESIGN.md §2.3).
- Semua routes dilindungi oleh CASL berdasarkan role/scope user.
- Error handling menampilkan pesan dalam Bahasa Indonesia.

## 📄 References
- `api-contract.yaml` – endpoint target.
- `docs/DESIGN.md` – BFF + CASL architecture.
- `docs/DATA_GOVERNANCE.md` §3 – PII masking di BFF.
