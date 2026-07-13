# TASK.md – Infra/prometheus

## Goals
- Set up Prometheus to **scrape** metrics from `frontend`, `backend`, `postgres`, and `opa`.
- Define alert rules for **error rate > 1 %**, **latency > 300 ms**, and **container restarts**.
- Export metrics in **Prometheus exposition format** (`/metrics`).

## Verification Criteria
- [] `prometheus.yml` includes job configs for each service, using Docker service DNS.
- [] `docker compose up` brings up Prometheus and it successfully scrapes all targets (no `scrape_error`).
- [] Alert rule `HighErrorRate` fires when simulated error rate > 1 % (use `curl` to generate errors).
- [] Grafana dashboard (imported via `grafana/dashboard.json`) visualizes request latency, error rate, DB connection pool.
- [] CI runs `promtool check config` and fails on syntax errors.

## Status
- [ ] Pending
