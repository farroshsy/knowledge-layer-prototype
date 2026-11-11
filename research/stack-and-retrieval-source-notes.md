# Stack and retrieval decisions — evidence notes

10 November 2026. Selected primary-source review, not exhaustive literature survey. Advice is conditional; it does not authorize a rewrite or prove local speedups. Attached GPT reports are secondary conceptual proposals, not verified Perkara implementation details.

## Verified project/company evidence

The supplied ai-interview-platform README lines 10–11 describes Rails/PostgreSQL/Redis/Sidekiq and React18/TypeScript/Vite/Tailwind. This verifies the provided case-study repository, not every Rakamin product or the intended architecture of this new task. The user-provided intern curriculum mentions JavaScript/TypeScript and React/Next examples. No verified CTO requirement to reuse one language/framework has been received. A secondary job-search result mentions Rails/Express/React but is not treated as an authoritative company-wide specification.

Our actual new prototype is Python/SQLite/plain HTML. Original baseline tests passed 10; a store-only candidate has now passed its two-review/test gate. A separate parallel candidate is being built. Neither establishes complete PoC acceptance.

One actual Grok HTTP ingest timed out after75s and published explicit rules fallback. Two later query requests used Grok and took about21.45s and17.21s. This is a small observed sample, not a latency SLO. It suggests external inference waiting must be profiled before asserting a language rewrite will solve response latency. CPU time, cost per token and team maintenance cost have not been measured.

## Technology primary sources

- [Rust ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html). Compiler-checked ownership provides memory-management constraints; it does not validate retrieval semantics, source support, business rules or generated SQL. Runtime performance benefit in this app is unmeasured. Candidate use: a measured CPU-heavy parser/indexer module with stable boundary, not an automatic whole-app rewrite.
- [Python asyncio](https://docs.python.org/3.14/library/asyncio.html). Supports asynchronous network/subprocess/concurrency orchestration. Async syntax alone does not provide durable jobs, safe retries or CPU acceleration.
- [PostgreSQL overview](https://www.postgresql.org/docs/current/intro-whatis.html). Supports transactional relational data, constraints and MVCC, relevant to a multiuser pilot. Migration/setup/driver/backup and operational costs remain tradeoffs for a next-morning demo.
- [SQLite WAL](https://www.sqlite.org/wal.html). Readers and writers can overlap but there remains one writer at a time; shared-memory restrictions affect network storage. An existing local durable DB is useful for this demo, not a claim of enterprise scale.
- [Python DAG scheduling](https://docs.python.org/3/library/graphlib.html). Ready tasks can be executed concurrently when predecessor constraints are satisfied. This is the relevant abstraction for parallel implementation, not simply increasing agent count.

## Algorithm candidates and actual reading depth

The following are algorithm-family candidates. Abstracts/documentation were read; no implementation comparison has been executed locally. Dates and reported benefits belong to their sources. Do not import author benchmark gains into our results.

- [Microsoft GraphRAG query overview](https://microsoft.github.io/graphrag/query/overview/): entity-oriented local search, corpus-oriented global search, DRIFT and basic vector search serve different question types. Global search adds substantial work. Evaluate question coverage and indexing/query costs before adopting.
- [LightRAG](https://arxiv.org/abs/2410.05779), initial2024/revised2025: graph/vector combination, low/high-level retrieval and incremental updates. Candidate when relation-heavy query coverage and update behavior beat a baseline on our corpus. No benchmark reproduced.
- [Late Chunking](https://arxiv.org/abs/2409.04701), initial2024/revised2025: embedding token sequences before chunk pooling to retain context. Requires an appropriate embedding pipeline; not the same as stuffing more text into the answer model. Does not fix identity or negation by itself.
- [EAGR](https://arxiv.org/abs/2611.01910), submitted1Nov2026: evidence-conditioned expansion over semantic metadata without a dedicated explicit graph DB. New preprint and author-reported benchmark; no local reproduction or production maturity assessment. Potential bounded experiment, not a mandate.

## Selection criteria before choosing stack/plugin

Business workflow fit; expected corpus/format and update frequency; exactness/negation/identity needs; permissions/privacy/provider policy; measured bottleneck; deadline and reversible setup; existing team skills/code standards; reviewer/oncall availability; library maintenance/license/dependency provenance; integration and observability; migration/rollback/export; total operating and handoff cost. Do not assign invented numerical scores when inputs are unknown.

Stack compatibility can reduce handoff burden, but first confirm which Rakamin team and codebase will own this component. A stable HTTP/schema/provider boundary can preserve that option without a rewrite tonight.

Plugins/tools are candidates, not automatic improvements. Require a needed capability, maintained primary repo/docs, license, bounded permissions, data destinations, version pinning, reproducibility and measurable gain. No installation is approved merely because a marketplace ranks it.

## Decision levels

- CTO/business perspective: sponsor/user job, value hypothesis, opportunity cost, risk acceptance and continue/pause/pivot gate. Real decision authority stays with humans.
- Staff engineering perspective: domain boundaries, invariants, data lifecycle, team fit, security/operations and migration triggers.
- Delivery/implementer perspective: smallest complete behavior, file ownership, acceptance criteria, test results and explicit blockers.

Proposed economic evaluation: compare volume × human task time before/after, including verification and correction time, against provider, infrastructure, implementation, review and maintenance costs. Inputs are unknown; no claim of x-times uplift or ROI is established.

## Immediate provisional decision

Complete and exercise the current small local PoC while documenting alternatives. Reconsider a broader stack change after actual domain/owner/integration constraints or measured local bottleneck emerges. Escalate bugs that affect correctness immediately; do not postpone a blocker merely because this is a PoC. Audio, legal-case billing and witness workflows from attached reconstructions are not automatically requirements for Rakamin.

## Addendum — user-supplied X analysis

The 261-line GPT analysis was read and normalized with original line references at `.context-hub/input-packets/x-analysis-review.txt`; source hash/trust notes are adjacent. Rendered Mermaid CSS was omitted from the context packet, not substantive prose. The linked Kevin/Azka X posts could not be fetched directly in this pass, so their attributed accounts remain secondary reports.

Source-backed concepts: [OWL primer](https://www.w3.org/TR/owl2-primer/) distinguishes classes/properties/individuals, useful when separating ontology definitions from instances; [Postgres materialized views](https://www.postgresql.org/docs/current/rules-materializedviews.html) persist query results and require refresh for changed data. Neither establishes that these technologies are mandatory here.

Practical decisions: preserve explicit domain contracts and stable identities, review semantic-rule changes with potentially broad impact, separate compute coverage from evidence recall, and choose metrics by stage. Ontology editor and unrestricted SQL are not introduced into the next-morning PoC. Read-only validated SQL can be a legitimate alternative under an appropriate threat model; our current implementation continues using bounded operations and parameterized storage methods.

Concrete implementation evidence takes precedence over architectural inspiration: independent review rejected mislabeled docs-only routes, unrelated sibling evidence expansion, and substring-based person identity matching. Macro HTTP journeys also failed combined queries. A bounded Grok repair has been dispatched against those defects, not against a hypothetical need for a large ontology engine. Its outputs must still pass tests and review; dispatch is not completion.
