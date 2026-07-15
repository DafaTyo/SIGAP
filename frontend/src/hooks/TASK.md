# 📌 Module Task Tracker: Hooks Package (frontend/src/hooks)

## 🎯 Core Objective & Responsibility
- Menyediakan **custom React hooks** yang meng‑abstraksi logika data fetching, state management, dan integrasi dengan Next.js Server Actions.
- Hooks harus **re‑usable**, **typed** (TypeScript) dan tidak mengandung UI markup.

## 📋 Development Checklist
- [ ] **Package init** – `index.ts` yang men‑export semua hook.
- [ ] **useAuth Hook** – `useAuth.ts`
  - Mengelola token JWT, refresh otomatis, dan expose `user`, `isAuthenticated`, `login`, `logout`.
- [ ] **useVendor Hook** – `useVendor.ts`
  - Functions: `getVendor(id)`, `listVendors(params)`, `createVendor(data)`, `updateVendor(id, data)`.
  - Memanggil server actions di `frontend/src/actions/vendor.ts`.
- [ ] **useDistribution Hook** – `useDistribution.ts`
  - Functions: `submitReport(data)`, `getReport(id)`, `listReportsByVendor(vendorId)`.
- [ ] **useComplaint Hook** – `useComplaint.ts`
  - Functions: `submitComplaint(data)`, `getComplaint(id)`, `trackStatus(id)`.
- [ ] **Write Hooks README** – contoh penggunaan di component, pattern error handling, dan loading state.

## 🔒 Constraints & Best Practices
- **No side‑effects on mount** without explicit call (avoid auto fetch in hook body, use `useEffect` with dependency).
- **Error handling:** return `{data, error, loading}` tuple.
- **Type safety:** define interfaces for payloads (`VendorCreatePayload`, `DistributionCreatePayload`, `ComplaintCreatePayload`).
- **Testing:** use `@testing-library/react` with `jest` to mock server actions.

## 📄 References
- `api-contract.yaml` – request/response schema untuk masing‑endpoint.
- `frontend/src/actions/` – server actions yang akan dipanggil.
- `docs/DESIGN.md` – alur data antara UI, BFF, dan backend.

---

**Instruksi Eksplisit:** Tidak ada kode hook yang boleh ditulis sebelum semua checklist di atas di‑centang selesai.
