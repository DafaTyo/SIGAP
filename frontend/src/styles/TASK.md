# TASK‑FE‑006 – Styles / Design Tokens

## Goals
- Store Tailwind CSS configuration and any design‑token JSON/YAML files used across the UI.
- Ensure the design system is versioned and can be imported by Storybook and component libraries.
- Provide a helper that loads tokens (e.g., colors, spacing) for use in component props.

## Verification Criteria
- [] `tailwind.config.js` exists at project root and references `./src/styles/design.tokens.json`.
- [] `design.tokens.json` (or `.yaml`) contains at least color palette, font sizes, and spacing scale.
- [] Component library imports tokens via a small utility (`importTokens()`).
- [] Unit test `src/styles/__tests__/tokens.test.ts` verifies that the token file can be parsed and returns expected values.
- [] CI runs the style token test and fails on parsing errors or missing required keys.

## Status
- [] Pending