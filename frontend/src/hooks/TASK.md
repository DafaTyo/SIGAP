# TASK.md – Frontend/hooks

## Goals
- Buat custom React hooks untuk **auth**, **data fetching**, **pagination**, dan **form handling**.
- Hooks harus tipe‑safe (TypeScript) dan dapat dipakai ulang di seluruh halaman.

## Verification Criteria
- [] Hook `useAuth` meng‑expose `login`, `logout`, `currentUser`, dan secara otomatis refresh token.
- [] Hook `useFetch` men‑handle loading/error states, abort controller, dan caching (SWR pattern).
- [] Hook `usePagination` menyediakan data slice, total count, dan navigasi halaman.
- [] Unit‑test untuk setiap hook dengan **React Testing Library** (`@testing-library/react-hooks`).
- [] Coverage ≥ 85 % pada folder `hooks`.

## Status
- [ ] Pending
