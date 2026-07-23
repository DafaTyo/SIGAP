# 📌 Module Task Tracker: Frontend (frontend/src)

## 🎯 Core Objective & Responsibility
- Next.js BFF (Backend-for-Frontend) yang mengatur request ke FastAPI, SSR, dan PII masking layer.

## 📋 Development Checklist
- [ ] **Package init** – `package.json`, `next.config.js` dengan proxy ke `/api`.
- [ ] **BFF layer** – Server Actions untuk setiap domain (vendor, distribution, complaint).
- [ ] **PII masking** – Middleware yang mem‑mask NIK sebelum response ke client.
- [ ] **CASL integration** – Permission toggling berdasarkan role/scope.
- [ ] **UI components** – Halaman utama: Dashboard, Vendor List, Distribution Map, Complaint Tracker.

## 🔒 Constraints & Best Practices
- PII masking wajib di BFF layer (DESIGN.md §2.3).
- RBAC diperiksa di Server Component/Route Handler, bukan hanya middleware.ts (CVE-2025-29927).
- Semua request ke FastAPI harus melalui BFF, tidak ada direct API call dari client.

## 📄 References
- `api-contract.yaml` – endpoint tujuan dari BFF.
- `docs/DESIGN.md` – BFF layer dan PII masking.
- `docs/DATA_GOVERNANCE.md` §3 – masking rules.
