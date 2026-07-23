# 📌 Module Task Tracker: Frontend Utils (frontend/src/utils)

## 🎯 Core Objective & Responsibility
- Utilitas TypeScript reusable: formatters, validators, PII mask, koordinat helper, dll.

## 📋 Development Checklist
- [ ] **pii.ts** – mask NIK, mask email, mask phone (mirror dari backend rules).
- [ ] **format.ts** – format tanggal Indonesia, format currency (Rupiah).
- [ ] **validate.ts** – validator untuk NIK, nib, koordinat GPS.
- [ ] **map.ts** – bounding box, radius calculation untuk peta.
- [ ] **api.ts** – typed fetch wrapper dengan idempotency key injection.
- [ ] **date.ts** – date helpers dengan locale id-ID.

## 🔒 Constraints & Best Practices
- Pure functions, no side effects.
- Full TypeScript types dan JSDoc comments.
- Unit test coverage wajib untuk setiap utilitas.
- Tidak boleh menyimpan secret di frontend (XSS risk).

## 📄 References
- `api-contract.yaml` – field type dan validation rules.
- `docs/DATA_GOVERNANCE.md` §3 – masking patterns.
- `frontend/src/hooks/` – hook yang menggunakan utilitas ini.