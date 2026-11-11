# Automated Grok council: build/review/evaluate graph

User explicitly authorizes an automatic repeated workflow using best available Grok models, concurrent independent agents, harsh reviews and implementation/evaluation loops. Goal is a working local hybrid knowledge repository by 2026-11-11 08:00 WIB. Do not merely spend tokens for its own sake. Root coordinator operates from Codex app, lacks ORCA_TERMINAL_HANDLE; use local headless Grok processes via an Orca shell command rather than impersonating Orca senders or relying on TUI permission menus. No bypass of rejected UI actions: model calls are tool-less, outputs are data, runner controls an explicit allowlisted change/test workflow.

## Goal context

Read DELIVERY.md, council/shared-business-task.md and council business-process A/B reports. Core is TWO independent source classes: seeded/imported structured business records and unseen documents; DB-only, document-only, combined question answering with source provenance. Initial klayer code is derived-only and incomplete. AI must process new inputs, not fixture-keyed answers. Category != semantic abstraction. Structured query plans compile to parameterized SQL; no direct generated SQL execution. Stable entity IDs or explicit reviewed links, not implicit join by same name. No claims of production readiness. Support actual input format(s) honestly; PDF/DOCX support should be prioritized according to feasibility, no unbounded OCR install. Mandatory observability (operational timings/errors/fallback and separately labeled quality evaluation) is user requested, not optional final paperwork.

## Create a runnable supervisor, not a proposal

Deliver automation/council.py, automation/test_council.py, docs/automation.md and automation/acceptance.json. Standard library Python, no dependencies needed. Do not touch app files during bootstrap. Real generation prompts will include snapshots of allowed source files, while Grok tools are disabled. All changes proposed as structured JSON file manifests, not shell commands. Runner validates and stages; no model code executed merely to parse manifests.

Implementation Interface requirements (also test surface): validate_manifest(project_root, files), evaluate_staging(...), run_council(config) or equivalent documented public functions; tests must cover behavior, not internals. Define machine-readable reports/events and a status command. No arbitrary shell execution, Git writes, skill installs, credential changes, publishing or external communications. Stronger reviews remain independent processes with separate prompts and no access to peer drafts before independent analysis.

## Execution DAG per round

- snapshot + fixed baseline tests
- concurrent proposer A and skeptical proposer B, both grok-4.7, same problem and same source snapshot, blinded until outputs exist
- adjudicator grok-4.7 reads both, chooses ONE bounded next slice with rationale and concrete acceptance criteria (or justified done)
- builder grok-4.7 returns full file contents manifest for that slice, not commands
- deterministic manifest validation + apply only to a TEMP STAGING COPY
- fixed syntax compile and unit test discovery in stage, capture full command/exit/duration, with timeout; no model-selected commands
- concurrent independent review(s) of the actual staged diff, grok-4.7 for data-integrity/security/spec gaps and build-fast for contract/test gaps
- only publish staged changes to project when fixed gates and independent review pass and source hashes still match snapshot. Otherwise keep failed candidate as artifact and feed actual issues back to next round. Never declare done because a model says so. Need acceptance status and evidence; no hiding failing tests.

Persist state after every node. Stop on STOP file, cancellation, budget max calls, time budget, deadline, repeated provider failure, stale concurrent source edit or no progress. Do not poll Orca inbox or create fake worker_done. SIGTERM handler should checkpoint and stop children safely. One supervisor at a time via lock. No task graph that starts dependency work early. At most 2 model calls in parallel by default; the model provider uses cloud inference, not local GPU.

## Hard limits

Default max 8 rounds, max 64 provider calls, max 4 wall-clock hours, absolute deadline 2026-11-11 06:30 Asia/Jakarta (reserve demo time). Config may lower these. Provider timeout 240s, tests timeout 120s. Do not claim quota percentage known; grok usage --json currently returned unavailable. Record actual token usage only if CLI supplies fields; missing usage/cost is null/unavailable, not zero. No arbitrary cost estimates. No promise of constant inference speed.

## Safe file scope

Only klayer/, tests/, fixtures/, docs/ plus README.md and CONTEXT.md are allowed proposed targets with text extensions .py/.html/.css/.js/.json/.md/.txt. Never automation/, .git/, .ssh/, .env, data/, symlinks, traversal/absolute paths, binaries, model weights, source outside prototype, secret filenames. Deny duplicate paths and oversized manifest (e.g. 12 files / 500KB per round). All code changes remain small. Don't introduce arbitrary frameworks/dependencies as an automatic edit. Staging copy uses only allowlisted project source, not credentials/private datasets/real database. Test command paths are fixed under staged root. Snapshot fingerprint checked again before publish; don't overwrite external changes.

Publishing full manifests is a reversible local action: keep before/after backups and evidence. Avoid partial publication: validate first, stage all files then publish with rollback on write error. No git reset/rebase/clean. A failed candidate remains stored but not live. Do not stop or modify unrelated processes.

## Grok calls (based on successful existing providers.py)

Use subprocess argument lists, shell=False, --model explicit, -p prompt or --prompt-file, --verbatim, --output-format json, --json-schema with actual schema, --system-prompt-override, --max-turns 1, --no-subagents, --disable-web-search, --permission-mode dontAsk, --no-alt-screen, --tools '' (no native tools). Model works from supplied source context only. If flags unsupported fail explicitly, don't silently enable tools or permission bypass. CLI JSON may return structuredOutput or text containing JSON: strictly parse a single object and validate shape/types. Never accept eval/pickle/markdown executable output. Resolve executable with shutil.which. Capture stderr bounded/sanitized. Don't print auth tokens or raw credentials in events.

## Instrumentation and visible metrics

Every node/round: role, model, start/end, monotonic duration, status, attempt, call count, prompt/output size, usage if supplied, test failures, file hashes, accepted/rejected finding IDs, reason for decision. JSONL events + latest status JSON + human-readable round report, and a simple standalone HTML report that can be opened without a server. Missing metrics clearly unavailable. Evaluation quality is separate from code tests; no fabricated semantic F1/citation accuracy, no copied Perkara benchmarks. Cost null unless measured. Report denominators/dataset versions for quality results. Final manifest of actual acceptance checks with pass/fail/not_measured. One can view status even while loop runs.

## Completion conditions

A working pipeline is required, not just passing existing tests. Builder should add genuine acceptance tests for independent business data and combined queries, new uploads, unknown/multi-category, negative/plan vs occurred, ambiguity, unsupported evidence, invalid/stale citations, retries and persistence. Deterministic tests with fakes and real provider spot checks must be distinct. Runtime provider inference is online through Grok subscription unless separately demonstrated local; no remote paid API or private uploads. Loop should stop with remaining blockers rather than mark unmet acceptance green.

## Bootstrap test requirements

Use fake model call adapter or dry-run so no external Grok calls for supervisor unit tests. Cover path traversal, symlink escape, forbidden files, duplicate targets, budget/cancellation/deadline, invalid JSON response, failed tests not published, stale source not overwritten, valid passing stage publication and rollback/backup behavior. No tests asserting constants just to inflate counts. Document one dry-run command, live start command, status and stop-file operation. Don't run the full loop from import or from unit tests.
