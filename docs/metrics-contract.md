# Metrics contract — measured values, not decorative scores

Date: 10 Nov 2026 WIB. User requires metrics to be inspectable. This contract separates workflow operations from application quality. A metric has value or null, unit, scope, denominator/sample count, dataset/version, timestamp and measurement method. `null / not_measured` is not zero and is not pass.

## Workflow operations (supervisor must collect)

- Per node/agent/model: start/end, monotonic elapsed seconds, status, timeout/error, attempt.
- Per run: completed/failed calls, accepted/rejected candidate, test command/exit/duration, source snapshot hashes, revision outputs, stop reason.
- Per model call: prompt/output size in characters or bytes (state unit). Actual token fields only if CLI reports them. Do not relabel character estimate as tokens.
- Cost: unavailable unless actual provider accounting exists. The subscription's remaining percentage is currently not programmatically available via `grok usage --json`; max calls/time are real controls instead.
- Independent views: original blinded proposals, later reviews, unresolved disagreements and adjudication rationale remain visible. Do not mark simulated personas as independent agents.

## Application operations (add instrumentation to actual execution path)

- End-to-end ingest/query duration using server monotonic clock, with per-stage parse/classify/extract/retrieve/plan/compose/validate timing where those stages actually exist.
- Success/failure/retry counts, pending/stale counts, current provider/method, fallback and invalid-citation rejection counts, source version and query route.
- DB-only / document-only / combined / unsupported route counters only from real executed routes.
- Latency p50/p95 with exact sample count and aggregation convention. With very small N show raw durations and don't advertise stable SLOs. Provider cold start and warm samples separate when measurable.
- Retain trace IDs that join source/job/query/run without logging secrets or unnecessary document text. User must be able to open the trace/report that explains the metric.

## Quality evaluation (requires independent labeled data and actual runs)

- Classification multi-label precision/recall/F1: specify label set, micro/macro averaging, unknown handling, sample count.
- Extraction/relations: field correctness, negation/modality/attribution, entity-link ambiguity handling, exact span validity versus semantic support separately.
- Retrieval: Recall@K only where gold evidence is labeled; MRR/NDCG only when ranking labels fit. Report DB evidence and document evidence coverage separately for combined tasks.
- Answer support: supported/unsupported assertions with an independently specified labeling method; citation coverage is not truth. Conflict and abstention cases must have expected outcomes.
- Integrity: idempotent retry, no stale publication, safe cross-source links, active citation resolution and restart persistence as pass/fail checks, not invented accuracy scores.

## Display and gate rules

Machine-readable JSON/JSONL plus readable HTML/Markdown report. Every performance comparison uses same case set/model/config or explicitly states differences. A measurement can be failed; do not hide it when aggregating. External PerkaraAI benchmark screenshots stay references, never become local measurement rows. Demo deadline and six-month roadmap are separate; no dashboard can establish production readiness.
