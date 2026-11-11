# Research handoff

2026-11-10, corrected the same day. The current handoff is `council/coordinator-handoff.md`. Terminal `term_8a2c0e4c-6764-4ba0-95e1-a9a8eaae1bb7` is blocked on an approval prompt. It does not own a live implementation. This file is not `docs/delivery-decision.md`.

## Read, and do not rewrite

Read `research/perkara-research.md`, `research/council-decision.md`, and `research/public-behavior-map.md` as reconciled on this date. Also read the worker files as they stand: `research/mvp-proposal.md`, `research/risk-and-acceptance.md`, `research/public-behavior-counterexamples.md`. Do not rewrite those three. `research/architecture-challenge.md` is now written. Its `worker_done` is blocked on an Orca command approval. No further Orca message was sent from this session. Mail on run `run_b5b3a36b42da`, if any arrives later, belongs to the delivery terminal.

## Contract the six cases do not cover

The reviewer file stays the attack. The behavior map now forbids the outputs that attack still lets through:

- A derived premise or synthesis may not flip polarity or modality of a live claim. A valid span is not enough. The relation is `meniadakan`. An answer that uses the flipped node fails.
- A plan does not `mendukung` an occurrence in another document, even when the date matches. The report stays an attributed claim.
- "Hanya mendengar" weakens direct testimony. It is not a second witness. "Hadir, dua sumber" fails. There is no fact that the defendant attended.

Cases 2 and 5 do not contain those three inputs. Do not mark them passed because the older cases passed.

## What was actually shown

`provider-smoke.json` records one online Grok CLI extraction: method `grok`, category `notulen`, `nonce_quote_exact` true, four grok quotes, no warnings, `provider_error` null, `offline_model` false. The file does not store the nonce. The session log names the passing nonce `KLAYER-SMOKE-4420`. An earlier nonce, `KLAYER-SMOKE-4419`, classified `notulen` and missed the exact nonce sentence. Exact copy of every sentence was required before the quote check passed. One pass is not semantic accuracy. The JSON query planner was not smoked. No API key was stored. App local is not model offline.

A prior session reported `python3 -m unittest tests.test_flow` as 10 tests OK. This close did not re-run them and does not certify the tree.

## Process left running

`python3 -m klayer serve --db data/demo.sqlite --provider auto --port 8765` was still running on `127.0.0.1:8765` at research close. This session did not stop it. A new upload through that process can call Grok CLI online. Seeded rows were classified with local rules before that restart. Do not treat those rows as model output.

## Left out on purpose

Azure, Docling, a distributed queue, a runtime agent council, recordings, phonetic search, and a million-node graph. Five animation labels, eleven strata, and the BAP/dakwaan/bukti/sidang chips are three public lists. Do not nest them as a spec. Marketing badge TERVERIFIKASI is not a truth bit. Lexical output must stay labeled `local-rules` and `semantic: false`.

## Hybrid requirement this notebook does not meet

The CTO task is retrieval over two sources: independent structured business records in a database, and separately dumped unstructured documents. A question may use the database only, documents only, or both. Classification is one step, not the product. One document may have more than one category. Unseen documents will be tested tomorrow. PostgreSQL was a suggestion, not an order.

`klayer/store.py` has notebooks, documents, jobs, sections, classifications, claims, fields, and relations. Claims and fields are derived from uploaded document text. There is no independent structured business record. Do not describe this notebook as meeting that requirement. Architecture stays on hold until `council/business-process-a.md` and `council/business-process-b.md` are reviewed. See `council/coordinator-handoff.md`.
