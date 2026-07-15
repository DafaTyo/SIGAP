# 📌 Module Task Tracker: Utils Package (frontend/src/utils)

## 🎯 Core Objective & Responsibility
- Menyediakan **utility functions** untuk frontend yang bersifat general‑purpose (API wrapper, token handling, date formatting, masking).
- Semua utilitas harus **type‑safe** (TypeScript) dan tidak mengakses DOM secara langsung (kecuali helper untuk `window`/`document`).

## 📋 Development Checklist
- [ ] **Package init** – `index.ts` men‑export semua util.
- [ ] **API Wrapper** – `api.ts`
  - Function: `apiFetch<T>(url: string, options?: RequestInit) -> Promise<T>`
  - Handles automatic inclusion of CSRF token, refresh token flow, and error mapping.
- [ ] **Token Storage** – `auth.ts`
  - Functions: `saveToken(token: string)`, `getToken()`, `clearToken()` (uses httpOnly cookie via Next.js middleware).
- [ ] **Date Formatter** – `date.ts`
  - Functions: `formatDate(date: Date, format: string = "dd/MM/yyyy")`.
- [ ] **Masking Helper** – `mask.ts`
  - Functions: `maskNIK(nik: string) -> string`, `maskEmail(email: string) -> string`.
- [ ] **Write Utils README** – contoh import dan penggunaan di hooks/components.

## 🔒 Constraints & Best Practices
- **No network side‑effects** inside utils (network only in `api.ts`).
- **Pure functions** for formatting/masking – no external state.
- **Testing:** unit tests in `frontend/src/tests/utils/` with jest.

## 📄 References
- `docs/DATA_GOVERNANCE.md` – aturan masking NIK & email.
- `frontend/src/actions/` – API wrapper konsistensi.

---

**Instruksi Eksplisit:** Kode utility TypeScript **tidak boleh** ditulis sebelum semua checklist di atas di‑centang selesai.
