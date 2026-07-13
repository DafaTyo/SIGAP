# TASK‑BE‑007‑03 – JWT Auth Dependency

## Goals
- Parse and validate JWT access tokens from the `Authorization: Bearer <token>` header.
- Verify signature using the public key (`JWT_PUBLIC_KEY`) and check standard claims (`exp`, `nbf`, `aud`).
- Extract `user_id` and optional `role` claim, expose them via a Pydantic `UserContext` model.
- Raise `HTTPException(status_code=401, detail="Invalid token")` when validation fails.

## Verification Criteria
- [] Valid token yields a `UserContext` with correct `user_id` and `role`.
- [] Expired, malformed, or signature‑invalid token returns **401**.
- [] Unit test `tests/dependencies/test_jwt_dependency.py` creates a signed JWT (using test private key) and checks both success and failure paths.
- [] CI runs the JWT dependency test suite and fails on any mismatch.

## Status
- [] Pending