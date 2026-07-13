# TASK.md – Infra/grafana

## Goals
- Create Grafana dashboards that visualise **SIGAP** key metrics: request latency, error rate, RLS‑blocked queries, DB connection pool usage.
- Export dashboard as JSON so it can be version‑controlled and imported automatically via Grafana API.
- (Optional) Set up **alert notifications** (Slack webhook) for critical thresholds.

## Verification Criteria
- [] Dashboard JSON (`dashboard.json`) can be imported without errors (`POST /api/dashboards/db`).
- [] Panels display correct Prometheus queries and update in real‑time.
- [] Alert rule `LatencyCritical` triggers when 95th‑pct latency > 500 ms for 5‑minute window.
- [] CI validates dashboard JSON schema with `grafana-cli plugins ls` (or lint tool).

## Status
- [ ] Pending
