# Isolation Strategy

## Options considered

1. Docker only
   Good baseline isolation and reproducibility.
2. Docker + separate service containers
   Better fault boundaries between backend, vector DB, and LLM runtime.
3. VM
   Stronger isolation, but too heavy for this scope.
4. Sandbox runtime inside containers
   Useful later if agents get code execution tools.

## Chosen setup

- `backend` container
- `ollama` container
- `chroma` container
- `prometheus` container
- `grafana` container

## Why this is the best fit

- simple to explain
- reproducible on another machine
- clear service boundaries
- enough isolation for a read-classify-store pipeline

## Weaknesses

- Docker is not a full security boundary
- Ollama inside a container still shares host kernel
- JS-heavy scraping can require browser tooling later

## Upgrade path

- add gVisor or Firecracker if agents later execute arbitrary code
- move to `vLLM` on dedicated GPU host if throughput matters
