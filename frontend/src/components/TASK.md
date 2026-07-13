# TASK.md – Frontend/components

## Goals
- Bangun komponen UI reusable yang mengikuti design‑system SIGAP (Tailwind, CSS‑variables).
- Setiap komponen harus mempunyai **Storybook** story, **unit‑test**, dan **type‑definitions** (TypeScript).

## Verification Criteria
- [] Komponen `Button`, `Card`, `Table`, `Modal`, `Dropdown` tersedia di folder `components/`.
- [] Storybook (`npm run storybook`) menampilkan semua story tanpa error.
- [] Jest snapshot tests untuk setiap komponen dengan coverage ≥ 90 % pada folder `components`.
- [] Komponen mematuhi **ARIA** attributes (aksesibilitas).
- [] CI men‑run `npm run test:components` dan gagal bila ada regression.

## Status
- [ ] Pending
