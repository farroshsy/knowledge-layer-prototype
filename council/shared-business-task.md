# Shared task: independent business process and retrieval architecture challenge

User explicitly requests MULTIPLE actual Grok agent sessions on the SAME task, blind independent proposal then cross-review, evidence-based resolution. Deadline local demo 2026-11-11 08:00 WIB. This is a bounded design challenge (aim ~10 minutes), not another literature review or instruction to delay the build all night. No forced disagreement: independently identical conclusions are acceptable, but all must justify assumptions and tradeoffs.

## Authoritative user need from CTO conversation

Company knowledge repository on local/internal system. TWO source classes: (1) dummy structured business data in a database, PostgreSQL or another justified foundation; (2) separately dumped unstructured documents. A simple chat/UI accepts a question that may require combining structured records with evidence inside those documents. The CTO will test with previously unseen documents tomorrow morning. One document can have multiple classifications. Layers such as structure, claims/facts, premises and synthesis are optional design inspiration, not a mandate to copy legal PerkaraAI internals. Classification is not the sole product goal. No actual CTO documents supplied yet; user explicitly authorized dummy data. User wants robust backend/business process and a working product, not canned fixture answers.

CTO suggestions are guidance, not orders to copy technical decisions. Infer exact business process and error behavior before choosing tools. We do NOT know actual incoming document domain or formats; list assumptions, target a useful initial support set, and explain unsupported inputs clearly. Only use existing prototype directory. Do not touch sibling submitted ai-interview-platform.

## Same question for both agents

What is the smallest COMPLETE product flow that credibly answers this need and has sound foundations for development? Specify actors, business objects, source ownership, ingest/review/query/update/error flow. Make it clear WHEN database only, documents only, or combined retrieval is required. Define data-layer vs semantic-layer vs document-category. Propose a semantic query interface that safely compiles to parameterized relational queries, not free raw model-generated SQL. Address joins by stable business identifiers, ambiguous entities and conflicting structured/doc evidence; a matching word/name alone is not a reliable join.

Compare relational semantic model vs graph-backed design vs embedding-heavy retrieval on use-case fit, correctness, setup/maintenance cost, latency and deadline. Do not manufacture numeric scores. Don't choose Postgres simply because suggested, or SQLite simply because easiest: justify based on actual scope. Unseen-doc ingestion and genuine model classification/extraction must be part of deliverable; deterministic test oracle is evaluation only.

Supply one worked synthetic business example with independent structured business records + documents; 3 questions (DB-only, doc-only, combined) with expected sources/results, including negation/plan vs fact and conflict. Include at least one unanswerable and one ambiguous entity case. Propose a small set of invariants and verifiable acceptance conditions. Don't falsely promise general zero-hallucination or copy external benchmark results.

For relevant design vocabulary read /Users/farros/.agents/skills/codebase-design/SKILL.md and /Users/farros/.agents/skills/domain-modeling/SKILL.md. No skill install/setup rituals or issue tracker changes. If defining glossary, propose it inside your report rather than editing shared CONTEXT until coordinator resolves terms. No remote publication or project/code edits.

Read DELIVERY.md and research/perkara-research.md only for needed background. You may inspect current klayer sources to identify mismatches; do not endorse existing implementation by default and do not edit it. Do not read peer business-process-{a,b}.md until coordinator explicitly starts cross-review. Do not run shells or delegate more agents; your task is reasoning from sources and writing one report via file tools.

## Output

Only write your assigned file council/business-process-a.md OR council/business-process-b.md, as stated in the launch prompt. Sections: brief interpretation; actors/flow (include concise Mermaid); worked example; architecture options/tradeoffs; proposed decision; current-code gaps; acceptance cases; uncertainties that materially change design. Finish with a concise actual outcome in Bahasa Indonesia. Source public claims, label inference. No code, installs, secrets, hooks, credentials, paid APIs, permissions changes or messages to others. Use native Read/Write tools for these files. Both agents have the same brief and no privileged answer key.
