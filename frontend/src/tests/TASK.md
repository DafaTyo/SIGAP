# 📌 Module Task Tracker: Frontend Tests (frontend/src/tests)

## 🎯 Core Objective & Responsibility
- Menampung **test suite** untuk frontend Next.js menggunakan **Jest** dan **React Testing Library**.
- Menyediakan fixture mock untuk server actions, auth, dan router Next.js.

## 📋 Development Checklist
- [ ] **Package init** – `index.ts` (opsional, hanya untuk re‑export).
- [ ] **Unit Tests per Component** – `components/`
  - Test rendering, user interaction (click, input), and snapshot matching.
- [ ] **Hooks Tests** – `hooks/`
  - Test data fetching, loading state, error handling dengan mock `apiFetch`.
- [ ] **Actions Tests** – `actions/`
  - Mock fetch requests dengan `msw` (Mock Service Worker), assert correct headers (X‑Idempotency‑Key).
- [ ] **Integration Tests** – `integration/`
  - Simulasikan alur registrasi vendor: form submit + mock response + redirect.
- [ ] **Write Tests README** – cara menjalankan `npm test` dan menghasilkan `coverage/lcov-report`.

## 🔒 Constraints & Best Practices
- **Snapshot testing** hanya untuk UI‑only components (no dynamic data).
- **Mock auth** menggunakan `jest.fn()` pada `@/utils/auth.getToken()`.
- **Isolation:** setiap test harus clean state (clear all mocks setelah each test).
- **Coverage target:** ≥ 80 % untuk actions & hooks.

## 📄 References
- `frontend/src/components/`, `frontend/src/hooks/`, `frontend/src/actions/` – source yang harus di‑test.
- `docs/DESIGN.md` – user flow untuk referensi integration test.

---

**Instruksi Eksplisit:** Kode test JavaScript/TypeScript **tidak boleh** ditulis sampai semua checklist di atas di‑centang.