# 📌 Module Task Tracker: Actions Package (frontend/src/actions)

## 🎯 Core Objective & Responsibility
- Menyimpan **Next.js Server Actions** yang berfungsi sebagai **Backend‑For‑Frontend (BFF)**.
- Setiap action memanggil FastAPI endpoint yang relevan, meng‑handle **idempotency**, **error mapping**, dan **response masking**.
- Actions harus **stateless**; semua state dikelola di client hooks atau UI.

## 📋 Development Checklist
- [ ] **Package init** – `index.ts` yang men‑export semua action (`registerVendor`, `submitDistribution`, `createComplaint`).
- [ ] **Vendor Actions** – `vendor.ts`
  - Functions:
    1. `registerVendor(data: FormData)` – POST `/vendors` dengan header `X‑Idempotency‑Key` (generate UUID).
    2. `updateVendor(id: string, data: Partial<Vendor>)` – PATCH `/vendors/{id}`.
    3. `revealNik(id: string)` – GET `/vendors/{id}/nik` (restricted, returns masked or raw based on role).
- [ ] **Distribution Actions** – `distribution.ts`
  - Functions:
    1. `submitReport(data: FormData)` – POST `/distribution` + enqueue AI task.
    2. `getReport(id: string)` – GET `/distribution/{id}`.
    3. `streamStatus(id: string)` – open SSE `/distribution/{id}/status/stream` (returns AsyncIterable).
- [ ] **Complaint Actions** – `complaint.ts`
  - Functions:
    1. `submitComplaint(data: FormData)` – POST `/complaint`.
    2. `updateStatus(id: string, status: string)` – PATCH `/complaint/{id}/status`.
    3. `assignComplaint(id: string, userId: string)` – POST `/complaint/{id}/assign`.
- [ ] **Error Mapping Utility** – `errorMapper.ts`
  - Convert FastAPI error responses (401, 403, 422, 429) menjadi JavaScript `Error` dengan kode yang dapat di‑catch di UI.
- [ ] **Write Actions README** – contoh pemanggilan dari hook, handling loading & error, dan best practice untuk idempotency.

## 🔒 Constraints & Best Practices
- **No direct DB access:** semua request harus melalui FastAPI.
- **Idempotency:** setiap mutasi meng‑generate UUID via `crypto.randomUUID()` dan men‑set header.
- **Security:** jangan meng‑expose raw JWT di client; gunakan httpOnly cookie (NextAuth) atau token dalam header Authorization.
- **Testing:** mock fetch dengan `msw` (Mock Service Worker) dalam unit test untuk actions.

## 📄 References
- `api-contract.yaml` – endpoint definitions & required headers.
- `frontend/src/hooks/` – contoh pemanggilan actions.
- `docs/DESIGN.md` – alur BFF.

---

**Instruksi Eksplisit:** Kode server actions (TypeScript) **tidak boleh** ditulis sampai semua poin checklist di atas di‑centang selesai.
