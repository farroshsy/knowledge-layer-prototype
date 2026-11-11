# Delivery contract — local knowledge-layer prototype

Deadline: 2026-11-11 08:00 Asia/Jakarta. User wants a usable local product and strong backend foundations, not a fixture viewer marketed as automatic AI. Dummy corpus approved; no private CTO docs yet. New project only, never modify frozen Rakamin submission. No push, publish, or external messages.

## Product process

1. User creates/selects a knowledge notebook and sees its document categories/definitions.
2. User uploads one or multiple supported documents (or pastes content). Originals and versions retained with stable source location.
3. Backend records an ingest job and exposes queued/running/completed/failed status; errors are understandable and retry does not duplicate active results.
4. Parser extracts text/structure with locators. Classification suggests a type or unknown/mixed, with reasons/evidence and method metadata. User can correct type.
5. Extractor uses category/schema to produce structured information and attributed claims; validation checks source pointers, bounds, negation/modality representation and referential consistency before publication.
6. User inspects category, extracted fields, layers and exact sources. Category changes trigger relevant reprocessing or explicit stale status, not silently incompatible data.
7. User can explore cross-document information and ask grounded questions if that vertical slice is supported; conflict and insufficient evidence are explicit. Any derived answer points back through claims to source text.
8. A restart preserves the notebook and does not expose stale or half-published data as current. User can repeat demo using supplied instructions.

## Non-negotiable foundation

Simple modular application with explicit interfaces for parsing, classification/extraction provider, validation, storage and query. One durable database with versioned schema/migrations; relational nodes/edges are acceptable, a graph DB is not mandatory. No microservices/distributed queue unless a measured need justifies them. Stable IDs, source hashes/version, transactionally published derivations, no generated SQL/shell execution from user or document text. Safe file handling and loopback binding. Configuration without committed secrets. No claim of production/multiuser security.

## A working product must not be a disguised fixture

Initial reviewer/design proposals conservatively suggested manual oracle fixture derivations only. That is valuable for evaluation but insufficient as the sole delivered product for this user's request. At least one real automatic classification/extraction path for newly uploaded synthetic text should be implemented and exercised, with explicit method/provenance. It must not return canned answers keyed to filenames. Demo fixtures are independent expected-output material, not the implementation.

Evaluate using Grok CLI through the authenticated local subscription as a bounded provider adapter if feasible; first test a tiny structured request with no secret inspection and record command/result. App local != model offline. Do not call paid API endpoints or install large model weights without a deliberate, authorized decision. If CLI cannot support the function, report the exact blocker immediately; don't pretend rules-only matching is semantic extraction. A deterministic rule-based classification fallback may be transparent and useful, but its limitations must be labeled. Never let provider subprocess execute free-form model commands; prompt input as stdin/structured argument with safe subprocess invocation, timeout, concurrency limit, output schema validation.

## Build and review sequence

Research is now sufficient to begin the bounded decision. Coordinator should collect both independent worker reports, complete ONE adversarial response loop, write concise council decision and begin implementation without asking user for permission on routine reversible local edits. User has authorized building the local product. Preserve a reviewer independent of implementation. Divide file ownership between backend builder and minimal frontend/fixtures if parallelizing. Keep tests tied to user behavior/data invariants, not test-count inflation. Stop expanding reference research.

Mandatory acceptance: upload new synthetic text not known at build time; dynamic classification/extraction results with sources; unknown category; category correction/reprocessing; conflicting/negated statements; no evidence answer; invalid citation rejected; reingest idempotency; job failure retry; persistence across restart; no source prompt injection instructions executed. Only claim what actually passes; distinguish automated assertions vs model quality spot checks.

## Delivery before deadline

Local app actually started with URL, reproducible start/setup commands, seeded dummy corpus, a 3-minute demo walkthrough, API/schema explanation, recorded test commands/results and known limitations. UI should reveal backend capabilities, not consume the night on decorative fidelity to PerkaraAI. Complete a usable end-to-end slice first, then expand breadth within time. Development foundations and production readiness are different claims.
