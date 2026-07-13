# TASK‑FE‑004 – Custom React Hooks

## Goals
- Create reusable hooks for common UI logic (e.g., `useAuth`, `useVendorData`, `useDebounce`).
- Each hook must be typed with TypeScript and include JSDoc comments.
- Provide unit tests using React Testing Library and Jest.

## Verification Criteria
- [] Hook files live under `src/hooks/` with `.ts` extension.
- [] Each hook returns a stable API (e.g., `useAuth(): {user, login, logout}`).
- [] All hooks have accompanying test file `*.test.tsx` that achieves ≥ 90 % coverage.
- [] CI pipeline runs the hook test suite and fails on coverage drop.

## Status
- [] Pending