# Coordinator handoff

2026-11-10. Safe slice only. No architecture expansion in this file.

## Need

The product retrieves from two distinct sources:

1. Structured business records that exist in the database on their own, not as rows extracted from a document.
2. Unstructured documents dumped separately.

A question uses the database only, the documents only, or both. Classification is one ingest step, not the product goal. One document may have more than one category. Tomorrow's test uses documents that were not in the build. Dummy data remains allowed. No private CTO documents are in this folder.

PostgreSQL, SQLite, a graph store, and embeddings are options for the A/B reports to justify. A suggestion from the CTO is not an order to copy. The current engine is not kept merely because it is already written.

## Current notebook

`klayer/store.py` creates `notebooks`, `documents`, `jobs`, `sections`, `classifications`, `claims`, `fields`, and `relations`. Claims and fields come from uploaded document text. A document can have several sections, and those sections can carry different categories. That is not an independent structured business source, and it is not a tested multi-category model for unseen files.

Do not claim this derived-only SQLite notebook meets the structured-business-data requirement.

## Hold

`council/business-process-a.md` is assigned to terminal `term_f6fae2e5-cfcb-480f-ad7a-247b761d2070`. `council/business-process-b.md` is assigned to terminal `term_a5a7b89e-99eb-40f2-9416-66cee3248fa9`. Both were absent when this handoff was written. They share `council/shared-business-task.md` and must stay blind to each other.

Do not design the hybrid flow here. Review both reports, then apply only the gaps that survive that review.

## Who is not running the build

Terminal `term_8a2c0e4c-6764-4ba0-95e1-a9a8eaae1bb7` is blocked on an approval prompt. Do not treat it as the owner of a live implementation. `research/architecture-challenge.md` is written: a filename-keyed fixture can pass the frozen suite and still fail an unseen upload. Its `worker_done` is not sent. This handoff does not start workers and does not edit application code.

Earlier document-claim rules still stand for extracted text: exact quotes, polarity, plan versus occurrence, and hearsay is not a second witness. They do not fill the missing structured source.
