# TASK‑BE‑006‑05 – OPA Policy Middleware

## Goals
- For each request, build a JSON input payload containing `user_id`, `method`, `path`, `query_params`, and (optionally) request body.
- Send the payload to OPA (or CASL) via HTTP `POST` to `OPA_URL/v1/data/sigap/allow`.
- If OPA returns `{"result": false}` respond with **403 Forbidden** and stop request processing.
- If OPA returns `{"result": true}` allow request to continue.
- Cache positive decisions for the same `(user_id, method, path)` tuple for 60 seconds to reduce OPA latency.

## Verification Criteria
- [] Successful request (policy true) proceeds to endpoint and returns the original status code.
- [] Denied request (policy false) returns **403** with JSON body `{ "detail": "Forbidden by policy" }`.
- [] Cache layer is hit on a second identical request (verify via log message or mock OPA call count).
- [] Unit test `tests/middleware/test_opa_policy.py` covers true, false, and cache scenarios using a mock OPA server (e.g., `responses` library).
- [] CI pipeline runs the OPA policy tests and fails if any scenario is broken.

## Status
- [] Pending