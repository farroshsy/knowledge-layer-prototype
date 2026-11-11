# Macro validation and value — decision instrument

10 November 2026. All commercial proposals below are hypotheses; no paying customer, willingness-to-pay, ROI or universal scenario coverage has been established.

## Actual macro evidence

Runner: `automation/macro_business_eval.py`.
Dataset: synthetic-macro-v1. Candidate: `.parallel-builds/20261110-214747-9bf46f/candidate-1`, exact hash in protocol. Provider: rules, not real-model quality evaluation. Disposable SQLite and actual loopback HTTP endpoints.

| Representative user job | Independent DB query | Combined new document + DB | Cross-notebook check |
|---|---|---|---|
| HR checks onboarding status and latest memo | pass | fail | pass |
| PIC checks class launch and preparation minutes | pass | fail | pass |
| Operations checks laptop purchase and meeting notes | pass | fail | pass |

Result: 6/9 automatic checks. Three domains use one shared record/memo workflow, so they are not three independent proofs of broad market fit. No usability/time-savings test with a real user has run. No semantic benchmark or confidence interval is implied.

The combined question asked “Apa status item dengan ID … dan bukti dari dokumennya?”; response stayed db_only with zero document claims. This may involve intent morphology and extraction/retrieval coverage. Root cause must be isolated before changing code. Keep failed evidence; do not rewrite questions simply to obtain a green dashboard.

## What macro proof should establish

The unit is a completed user job: create/import independent records, upload new source, inspect processing failures, ask a meaningful mixed-source question, open both source types, understand ambiguity/conflict, then reopen and repeat. Microtests validate mechanisms; integration checks validate contracts; full workflow tests validate task completion; real-user comparison validates utility. These are separate evidence layers.

Define each scenario BEFORE executing it: persona/job, data formats/size, independent DB facts, documents, identities/time/authority, question paraphrases, gold evidence, expected answer/abstention, exception path, and observable success condition. Record actual provider, method/fallback, source hash, model/config and raw timings. Same-name collision, newer proposal versus approved record, missing/partially processed source and unsupported cost-saving question should be separate negative cases.

Coverage should grow across question type, document format, ambiguity, source disagreement, corpus length, update/restart, failure/retry and user permissions. Do not claim “all real-life scenarios” from any finite benchmark. For tomorrow, demonstrate a bounded tested surface and disclose failures. Customer-specific domain validation follows with permission.

## Potential value / revenue paths

| Hypothesis | Buyer / user job | Possible charging unit | Capabilities required | Evidence before prioritizing |
|---|---|---|---|---|
| Internal operational knowledge | Internal sponsor; locate and reconcile records/documents | Internal budget/cost savings, NOT external revenue | Hybrid retrieval, source evidence, access scope, repeatability | Task-time baseline, correction/review time, real usage frequency |
| Team knowledge workspace | Business team with repeated document questions | Workspace or seats, possibly bounded usage | Multiuser access, lifecycle, onboarding, support, privacy | Buyer interviews and paid pilot or credible purchase commitment |
| Document-processing/API service | Teams integrating extraction/retrieval into their products | Document/page/job or API usage | Measured extraction quality, idempotency, API contracts, limits and cost visibility | Customer integration need, usage volume, unit cost and acceptance benchmark |
| Private deployment license + support | Organization requiring controlled deployment | Deployment/license plus maintenance/support | Provider/data policy, installation, backup/restore, monitoring, upgrades | Actual security requirements, support effort and approved contract scope |
| Domain solution / paid pilot | A specific vertical with measurable repetitive work | Pilot, domain package or ongoing service | Domain ontology, gold cases, tailored workflow and reviewer | Identified buyer/problem, domain validation, evidence that generic search is inadequate |
| Integration/onboarding services | Teams with fragmented systems | Scoped implementation fee | Connectors, import validation, mapping, documentation and ownership | Real data-source inventory and delivery estimate; avoid pretending service income is recurring SaaS margin |

Do not monetize customers' private documents, assume redistribution rights or treat data retention as automatically permitted. Product ownership and commercial authority belong to the company. Pricing units are options, not prices or validated demand.

## Feature prioritization mechanism

For every proposed feature, capture the user job, scenario evidence, failure/risk addressed, demand evidence, candidate revenue/value path, implementation/dependency cost, recurring provider/support cost, measurable acceptance and decision owner.

Apply gates in order:
1. Correctness/privacy/security/reproducibility blocker? Address it even if not directly billable.
2. Does the feature enable completion of an important currently failing workflow?
3. Is there an identified user/buyer and evidence of frequency/pain/willingness to adopt?
4. Can its outcome and total cost be measured in a bounded experiment?
5. Compare alternatives and reversibility. Choose build, experiment, defer or reject with rationale.

Do not create weighted ICE/RICE scores from invented demand or effort values. A feature can be a prerequisite for several revenue paths while producing no immediate revenue itself. Audit/provenance and safe permissions are examples; security is not optional because it does not sell separately.

Current macro failures strengthen the priority for genuine combined retrieval and varied question handling. Audio, billing automation, generic graph engine or a language rewrite remain separate proposals; none fixes that failed workflow by its mere presence.

## Value measurement

Measure manual time per completed task against assisted search + evidence review + correction time, with the same tasks and success rubric. Track task completion and unsupported assertions alongside time: a faster wrong answer is not a gain.

Potential net operating value = completed task volume × validated labor-time difference × relevant labor cost, minus inference/storage/support/maintenance and implementation cost over a stated horizon. All those business inputs are currently unknown. Revenue requires separate buyer/payment evidence and is not equal to theoretical labor savings.

Stage gates: technical PoC → feasibility on held-out/new documents → customer/problem and willingness-to-pay validation → scoped pilot → appropriate security/operational hardening → expansion. Continue/pause/pivot decisions remain human decisions with source-linked evidence.

## Primary references and reading limits

- [Strategyzer Value Proposition Canvas](https://www.strategyzer.com/library/the-value-proposition-canvas): starts from customer jobs, pains and desired gains; fit must be checked with customer evidence. Our candidate revenue paths are proposals, not claims endorsed by this source.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework): risk considerations belong across design, development, use and evaluation. This is guidance, not a certification of our system.
- [ALCE primary repository](https://github.com/princeton-nlp/ALCE): citation quality and correctness need explicit evaluation, rather than assuming the presence of a citation proves support.
- [ARES paper](https://aclanthology.org/2024.naacl-long.20/): separates context relevance, answer faithfulness and answer relevance. We have not reproduced ARES or trained a judge.
