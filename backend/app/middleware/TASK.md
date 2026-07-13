# TASK‑BE‑006 – Middleware Package Master List

## Goals
- Assemble a **modular middleware stack** for the FastAPI backend where each concern lives in its own module.
- Provide a single helper `register_middlewares(app)` that imports and registers each middleware based on environment toggles.
- Ensure **full test coverage** (≥ 90 %) for every sub‑module and for the registration helper itself.
- Keep the stack **lightweight**: only enable what the deployment needs (e.g., rate‑limit can stay disabled in dev).

## Verification Criteria
- [] `register_middlewares(app)` calls the `add_*` functions for every middleware that is enabled via env vars.
- [] All sub‑module `TASK‑BE‑006‑0x` items are marked **[x]** when their unit tests pass.
- [] End‑to‑end test `tests/middleware/test_full_stack.py` spins up a FastAPI `TestClient` with the full registration and verifies that:
  - CORS headers appear when enabled.
  - GZip compresses large responses.
  - Security headers are present.
  - Request‑ID propagates.
  - OPA policy blocks/allows correctly.
  - Audit log entry is created.
  - (optional) Rate‑limit throttles after the defined threshold.
- [] CI pipeline runs the full‑stack middleware test suite and fails if any criteria are not satisfied.

## Status
- [] Pending