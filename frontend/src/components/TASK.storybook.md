# TASK‑FE‑005 – Storybook Setup (optional)

## Goals
- Install and configure Storybook for the Next.js UI component library.
- Enable isolated component development, visual regression testing, and documentation.
- Integrate Storybook with the existing design system (Tailwind CSS, custom tokens).

## Verification Criteria
- [] `storybook` script added to `package.json` (`npm run storybook`).
- [] At least one example story for each core component (Button, Card, Table) exists under `src/components/**/*.stories.tsx`.
- [] Storybook launches without runtime errors and displays components correctly.
- [] Visual regression test (e.g., `chromatic` or `storyshots`) runs in CI and fails on unintended UI changes.
- [] CI workflow includes a step that runs `npm run test:storybook` (or `chromatic` upload) and fails on regression.

## Status
- [] Pending