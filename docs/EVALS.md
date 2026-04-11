# Evaluation Plan

## LLM eval

Measure:
- classification accuracy
- JSON validity rate
- consistency across repeated runs
- hallucination rate on out-of-domain articles

Candidate models to benchmark:
- `qwen2.5:7b-instruct`
- `llama3.1:8b-instruct`
- `mistral:7b-instruct`

Recommended default winner: `qwen2.5:7b-instruct`

## System eval

Measure:
- end-to-end accuracy
- false-new-topic rate
- average latency
- parser failure rate
- validator rescue rate

## Minimal dataset design

Create a local gold set with 40-100 URLs:
- 10-25 programming
- 10-25 english learning
- 10-25 cooking
- 10-25 out-of-domain

Store fields:
- `url`
- `expected_topic`
- `should_create_new_topic`

## Suggested success criteria

- `>= 0.85` accuracy on in-domain topics
- `< 0.15` false-new-topic rate
- `< 8s` p95 latency on local machine
