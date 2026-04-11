# Observability

## Stack

- `Loguru` for structured app logs
- `Prometheus` for metrics
- `Grafana` for dashboards

## Key metrics

- `agent_latency_seconds{agent=...}`
- `classification_total{mode=...}`
- `fallback_total{target=...}`

## What to alert on

- parser failures spike
- topic creator rate jumps unexpectedly
- validator rejection rate grows
- p95 latency exceeds threshold
