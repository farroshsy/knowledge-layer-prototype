# Local MVP proposal

Deadline for a running prototype: 2026-11-11 08:00 Asia/Jakarta. This file is the design only. It does not implement the app and it does not clone Perkara AI.

Priority order: upload documents, inspect the stored evidence, answer only from that evidence. A missing or non-supporting source ends in abstain or an explicit conflict. It does not end in a guessed fact.

## What is documented, what is inference, what this MVP chooses

Labels used below:

- **Documented.** Public copy or a public post, read on 2026-11-10. Not an audit of Perkara AI's source, database, or production behavior.
- **Inference.** A reading that goes beyond that text.
- **MVP choice.** A decision for this prototype. It is not a claim about Perkara AI.

### Documented product behavior

Marketing HTML at <https://perkara.ai/> describes the service as reading case files and hearing recordings, checking analysis with multiple AI agents, and showing the original source for each answer. The page is a client-rendered site. The strings below come from the public bundle `https://perkara.ai/assets/index-DlM17x7b.js`, not from a product manual.

The same bundle names three different groupings. They are not one list.

| Public label | Names in the bundle | Role on the page |
| --- | --- | --- |
| Five layers | Berkas, Teks, Pengetahuan, Fakta, Sintesa (EN: Files, Text, Knowledge, Facts, Synthesis) | Abstraction stack |
| Eleven strata | Berkas, Segmen, Pindaian, Teks, Klasifikasi, Dokumen, Struktur, Pernyataan, Fakta, Premis, Sintesa (EN: Files, Segments, Scans, Text, Classification, Documents, Structure, Statements, Facts, Premises, Synthesis) | Trace-the-source stack |
| Document-type chips | BAP, Dakwaan, Bukti, Sidang (EN: Statements, Indictment, Exhibits, Hearings) | Kinds of file inside one case |

Other documented copy, same bundle:

- Upload scanned PDFs and hearing audio or video. A person confirms speaker identity and document type after the system guesses. Examples on the page are invented (`Contoh di halaman ini memakai data rekaan`).
- Files are described as read twice and unwrapped into five layers, including who did what, where, when, and how.
- Several agents draft and cross-check an answer. Copy says claims without a source are removed, and each sentence carries a citation to the original page.
- The worked example is attributed, not god's-eye: "Menurut Saksi A, terdakwa hadir", cited to BAP Saksi A, while a hearing line says the witness only heard it from Saksi B.
- Phonetic transcript search is a separate feature. The sample query `rapat` highlights `rapad`. That is sound-alike matching. It is not a claim of semantic understanding.
- Eight feature names are also listed (uraikan berkas, ekstrak pengetahuan, tanya, telusuri sumber, identifikasi rekaman, bedah saksi, cari rekaman, telusuri sumber fakta). Those are features, not the eleven strata.

Ibrahim Arief, <https://x.com/ibamarief/status/2117104412824944848> (2 Nov 2026; read via X, not via the earlier 403 page fetch):

- **Documented.** A semantic model sits between the model and raw case data. For their matters they chose a multi-layered knowledge graph, with some layers on a purpose-built legal-investigation ontology. He gives a scale of about one million entities and links for a matter. He says there are many semantic-model designs, and that ontology must follow the domain.
- **Documented.** A `LIKE '%meeting%'` query treats "Budi tidak bisa ikut meeting" as a hit. He presents that as a false positive because the query misses the negation. Agents then query typed predicates such as `<mengikuti>`, instead of scanning raw text.
- **Documented.** They build an event-driven ETL pipeline, and in some cases PostgreSQL materialized views are enough. He points readers at their own coding agents for implementation. He does not publish the schema.

Later public posts by the same author, text only (screenshots were not inspected):

- Citation inspection should show the original source used for an answer (5 Nov 2026, post `2118380643294023764`).
- Chat council size was described as moving from 3 to 4 agents, with a named final adjudicator model (5 Nov 2026, post `2118379528137613823`). Those screenshots are described by the author as a simulated matter.
- A router can send a simple question to a graph lookup instead of the full council. He contrasts a lookup measured in seconds with a much slower full chat (6 Nov 2026, posts `2118721930106908863` and `2118534284340568303`).
- Retrieval over knowledge-graph nodes is described as a recall stage, with a later rerank over a very large token volume through a third-party reranker (9 Nov 2026, posts `2119826812704539022` and `2119829600578707671`). Treat the numbers as the author's public account, not as measurements of this prototype.

Tirto's interview (<https://tirto.id/perkara-ai-inovasi-ibam-arief-melawan-kriminalisasi-hukum-hEti>, 2 Nov 2026) is journalism, not a spec. It reports upload by the legal team, a human approval step, type-specific handling for witness statements, exhibit lists, and indictments, and a stack of analyst, source-auditor, and judge agents. Useful as context. Not evidence of internal architecture.

### Inference, kept out of the schema

- The five marketing layers and the eleven strata overlap (files, text, facts, synthesis appear in both). **Inference:** the page is a teaching diagram, not a published relational schema. This MVP does not create eleven physical tables just to mirror the diagram.
- **Inference:** "Fakta" on the marketing page is a layer name. The same page answers with "Menurut Saksi A", so a stored proposition is not automatically an established fact. This MVP stores **claims**, with polarity and an epistemic status. It does not have a table named facts.
- **Inference:** one uploaded file yielding many nodes matches "unwrapped into layers" and the author's graph of many entities. The exact cardinality is not published. The MVP **requires** many nodes per document as its own rule.
- Nothing public defines their edge vocabulary, ETL event shape, or how they version a re-run. Those are **MVP choices** below.
- Keyword or regex overlap is not semantic evaluation. The author's meeting example is the counterexample. Phonetic search on the marketing page is a third, narrower thing. This MVP may use exact substring checks only to verify that a stored quote still sits inside its source span.

## MVP

One notebook is one SQLite file. A person uploads many plain-text documents. Ingest stores bytes, a hash, and located sections. A derivation pass then writes statements, claims, premises, and syntheses. Each derived node points at a quote in a section, or at earlier nodes, and records which derivation created it.

The demo corpus is three tiny synthetic documents with a checked derivation. Arbitrary uploads are stored and segmented. They do not grow semantic nodes until a derivation says so. A regex hit is an inspection aid with `method=lexical`. It is never a claim.

### Components

Five pieces, all local. No agent framework, no vector database, no Postgres, no queue, no auth service.

| Piece | Job | Depends on |
| --- | --- | --- |
| `ingest` | Copy `.txt` / `.md` into `documents` and `sections` | Python stdlib |
| `derive` | Insert nodes for one derivation id | Checked JSON fixture for the demo. Optional Grok CLI adapter is off by default |
| `answer` | Read confirmed nodes and return grounded, conflict, or abstain | SQLite only |
| `inspect` | Local page: document text, nodes by layer, citations jump to the span | `http.server` |
| `notebook.sqlite` | The notebook | SQLite |

`answer` never calls a model. If the optional adapter is on, its output is unconfirmed until the citation check passes, and a failed CLI run falls through to `answer`.

### Machine and what "local" means

Checked on this Mac, 2026-11-10: macOS 15.7.9, `x86_64`, Python 3.14.2 at `/usr/local/bin/python3`, SQLite 3.43.2 at `/usr/bin/sqlite3`, Node 20 present but unused, `grok` 1.0.77 at `/Users/farros/.grok/bin/grok`.

Use the Python standard library (`sqlite3`, `http.server`, `hashlib`, `json`, `pathlib`). Do not add packages. Intel Mac: do not require MLX, CUDA, Docker, or a local weight file.

Two different claims:

- **Local app.** The process and the SQLite file run on this Mac. Upload, inspect, and the deterministic answer path are specified to work with network disabled. That offline run has not been executed yet, because this task does not build the app.
- **Offline inference.** Not included. No model weights ship with the MVP. The Grok CLI, if enabled, is a local process that may still reach a model service. Help text shows `login` and `--oauth`. It does not show an offline-weights mode. Whether a prompt succeeds with no API key was **not tested**. Feasibility is unknown. Do not read or copy credentials to find out.

## Category is not an abstraction layer

**Category** is a label on the document: what kind of file it is. For the demo: `minutes`, `witness_note`, `email`. Legal chips from the marketing page (BAP, indictment, exhibit, hearing) can be added as labels later. Category does not place the file on a knowledge layer.

**Layer** is how far a node sits from the source text:

| Layer | Record | Meaning |
| --- | --- | --- |
| 0 | `sections` | Verbatim span. Not a proposition |
| 1 | `statements` | An attributed utterance or a sentence in the file. Still not a fact |
| 2 | `claims` | A proposition with polarity and modality, tied to a statement |
| 3 | `premises` | A claim selected as an input to reasoning, with an epistemic status |
| 4 | `synthesis` | A text that cites premises. It may report a conflict or an abstention. It may not invent a side |

Changing a document's category must not move, delete, or rewrite nodes. One document produces many sections and many nodes. A node belongs to the notebook, not to a folder named after a layer.

## Schema

Identifiers are text. Times are ISO-8601 with offset. Char offsets are UTF-8 byte offsets into `documents.raw_text`, so a quote check is exact.

```text
notebooks
  id, title, created_at

documents
  id, notebook_id, filename, sha256, raw_text, uploaded_at
  category              -- minutes | witness_note | email | unknown | later legal chips
  category_source       -- human | unconfirmed
  category is not a layer

sections
  id, document_id, ordinal, locator     -- e.g. "p1" or "para 2"
  char_start, char_end, text

derivations
  id, notebook_id, parent_derivation_id
  method            -- manual_fixture | lexical_highlight | grok_cli
  method_version    -- fixture name, or CLI version string if one was returned
  created_at, input_hash, notes
  immutable. A re-run inserts a new row. It does not update old nodes.

statements
  id, notebook_id, derivation_id
  text, speaker           -- speaker may be null when the file itself is the speaker
  review_status           -- confirmed | unconfirmed

claims
  id, notebook_id, derivation_id, statement_id
  proposition             -- canonical wording of the proposition
  polarity                -- assert | deny
  modality                -- scheduled | planned | occurred | requested | other
  review_status

premises
  id, notebook_id, derivation_id, claim_id
  epistemic               -- attributed | conflict | insufficient
  uncertainty_note
  review_status

syntheses
  id, notebook_id, derivation_id
  question, status        -- grounded | conflict | abstain
  text, uncertainty_note
  review_status

evidence
  id, node_kind, node_id          -- statement | claim | premise | synthesis
  source_kind, source_id          -- section | statement | claim | premise
  quote, char_start, char_end     -- required when source_kind is section
  A statement or claim that will be shown to a user must have at least one
  evidence row whose quote is a substring of the cited section.

links
  id, derivation_id
  from_kind, from_id, to_kind, to_id
  rel                         -- contradicts | same_event | mentions | derived_from
  note
  A shared keyword does not create a link. Only a derivation does.

entities
  id, notebook_id, name, kind     -- person | event | other

node_entities
  node_kind, node_id, entity_id, role

answers
  id, notebook_id, derivation_id, question
  status                      -- grounded | conflict | abstain
  text, uncertainty_note, created_at
  Answers cite premises or claims. They do not cite a bare lexical hit.
```

`review_status=unconfirmed` nodes are visible in the inspector and invisible to `answer`. The demo fixture inserts `confirmed` rows. Adapter output lands as `unconfirmed`.

Lexical highlights, if implemented, are `derivations.method=lexical_highlight` plus section hits. They are not statements, claims, premises, or syntheses.

## Provenance, versions, uncertainty

Every derived node stores `derivation_id` and at least one `evidence` row. Following evidence ends at a `sections` span. The inspector shows that span inside the document, not a paraphrase alone.

Re-running derivation inserts a new `derivations` row with `parent_derivation_id` set. Old nodes stay. Answers record the derivation they read. Two answers to the same question can differ because they pinned different derivations. The UI names the derivation.

Epistemic status lives on premises and on the answer:

- `attributed` means someone, or some file, said it. Extraction does not promote it.
- `conflict` means two confirmed claims share a proposition and have opposite polarity. The answer shows both and picks none.
- `insufficient` means the related nodes use a different modality or a different proposition. They are listed as non-establishing.
- Answer `abstain` means no confirmed claim supports the asked proposition. Related-but-insufficient nodes may be listed, clearly marked as not supporting it.
- Answer `grounded` is allowed only when every asserted sentence cites a confirmed node, each quote is still a substring of its section, and the cited claims do not conflict and match the asked polarity and modality.

`scheduled` or `planned` does not entail `occurred`. `deny` is not flipped by the presence of the negated words in the source string.

## Cross-document links

Links are rows. They can connect nodes from different documents. The demo needs these links, and no others:

- Rina-attendance claim in the minutes `contradicts` Rina-attendance claim in the witness note. Same proposition (`Rina attended the 2026-03-14 meeting`), opposite polarity.
- All three attendance claims `same_event` the entity `meeting:2026-03-14`.
- The email claim `mentions` person `Budi` with polarity `deny` and modality `occurred`. It does not assert that Budi attended.
- The pilot claim `mentions` a plan date only. It has no `same_event` link to "pilot is running on 2026-11-20", because that event is not in the corpus.

## Sample pipeline

Three synthetic documents. They are dummy data, allowed for this prototype. They are not a real matter.

**doc_a.txt** category `minutes`

```text
Notulen rapat internal 14 Maret 2026.
Pilot direncanakan mulai 15 November 2026.
Rina hadir pada rapat 14 Maret 2026.
```

**doc_b.txt** category `witness_note`

```text
Menurut Saksi Budi, Rina tidak hadir pada rapat 14 Maret 2026.
```

**doc_c.txt** category `email`

```text
Email Sari, 16 Maret 2026: Tolong sampaikan ke Rina, Budi tidak bisa ikut rapat 14 Maret.
```

Ingest writes one document row and one section per non-empty line, with real offsets. The fixture derivation `deriv-demo-1` (`method=manual_fixture`) then writes:

| Node | From | Proposition | Polarity | Modality | Epistemic |
| --- | --- | --- | --- | --- | --- |
| claim A1 | doc_a line 2 | Pilot start is planned for 2026-11-15 | assert | planned | attributed |
| claim A2 | doc_a line 3 | Rina attended meeting 2026-03-14 | assert | occurred | attributed |
| claim B1 | doc_b line 1 | Rina attended meeting 2026-03-14 | deny | occurred | attributed |
| claim C1 | doc_c line 1 | Budi attended meeting 2026-03-14 | deny | occurred | attributed |

Each claim has a statement parent and an evidence quote equal to its source line. Premises point at those claims. Link A2 `contradicts` B1. A2, B1, and C1 share `meeting:2026-03-14`.

Questions the inspector must run against `deriv-demo-1`:

1. **Conflict.** "Apakah Rina hadir pada rapat 14 Maret 2026?" Status `conflict`. Show claim A2 and claim B1 with their quotes. Do not choose a winner. Do not call either an established fact.
2. **Negation.** "Apakah Budi ikut rapat 14 Maret 2026?" The email contains the words "ikut rapat" and "Budi". The stored claim is polarity `deny`. The answer must not say Budi attended. It reports an attributed denial by Sari's email. A lexical highlighter may show the line and must label itself lexical.
3. **Abstain.** "Apakah pilot sudah berjalan pada 20 November 2026?" No claim uses modality `occurred` for the pilot. Claim A1 is a plan for 15 November and does not establish that the pilot was running on 20 November. Status `abstain`. The plan sentence may appear only as related and non-supporting. The answer must not say the pilot ran.

A synthesis row is stored for question 1 with status `conflict`. Questions 2 and 3 do not get a synthesis that asserts a yes.

## Grok CLI adapter versus deterministic inspection

Default path is deterministic and is the one acceptance tests run.

`answer` loads confirmed claims, premises, links, and evidence for the pinned derivation. It matches a question only through stored proposition, polarity, modality, and links. It does not score bag-of-words similarity and then call the result a semantic answer. Unknown wording that hits no confirmed proposition returns `abstain`, even if source text shares keywords.

Optional adapter, off unless a flag is set:

- Spawn `grok` with `-p`, `--output-format json`, `--json-schema` for `{status, text, uncertainty_note, citations[]}`, and `--disable-web-search`.
- Send only the question plus confirmed nodes and their quotes. Do not send instructions to browse.
- Parse JSON. Reject the run unless every citation's quote is a substring of the cited section, every cited node is confirmed, a `grounded` status has at least one citation, and a known conflict is not rewritten as `grounded`.
- Accepted adapter nodes stay `review_status=unconfirmed` until a person confirms them. `answer` ignores them.
- Non-zero exit, timeout, invalid JSON, or a failed check: drop the model text, show the failure in the inspector, run deterministic `answer`. Do not present the dropped text as evidence.

Comparison:

| | Deterministic `answer` | Grok CLI adapter |
| --- | --- | --- |
| Process | Python reading SQLite | Local `grok` process, optional |
| Network | Specified not to need one | Unknown. Help shows login and `--oauth`. No offline model mode was found in `grok help` |
| API key in the repo | None | None. Do not add one. Whether the installed CLI already has a session was not tested |
| Understands negation | Only if a derivation stored `polarity=deny` | Only if a real model call succeeds and the citation check passes. Not tested |
| Keyword overlap | May highlight a span as lexical | Must not be described as the model |
| Abstain on the pilot question | Required | Required of the schema; if the model says the pilot ran, the check drops it |
| Feasibility | Implementable with the installed Python and SQLite. App not built yet | **Unknown.** No prompt was sent |

`grok help` on 1.0.77 shows `-p`, `--json-schema`, `--disable-web-search`, `login`, and `--oauth`. That is the whole basis for the adapter shape. It is not a test of inference.

## Acceptance criteria

The prototype meets the bar when all of the following are true on this Mac, with the adapter flag off:

1. A folder upload of the three files creates three `documents` rows, distinct sha256 values, and at least two sections for doc_a. Raw text round-trips.
2. `deriv-demo-1` creates at least four claims from three documents. doc_a alone produces two claims. Deleting no source file, a second derivation `deriv-demo-2` adds rows and leaves `deriv-demo-1` readable.
3. Document category and node layer are separate columns. Updating doc_c.category does not change claim C1's modality or polarity.
4. The Rina question returns `conflict` with both quotes. The Budi question does not answer yes. The pilot question returns `abstain` and does not say the pilot was running.
5. Every quote shown on those answers is a substring of the cited section. The UI can open that section from the citation.
6. A lexical search for `ikut rapat` may list doc_c and must be labeled lexical. It must not create a claim and must not flip claim C1 to `assert`.
7. Unconfirmed nodes, including any future adapter output, do not appear in the answer payload.
8. With the adapter off, the three questions are answered from SQLite alone.

Adapter criteria, only if someone turns the flag on later:

9. A failed or unchecked CLI result does not change the three answers above.
10. No API key is written into the repo. No paid or external API is called by the default path.

These criteria are the test list. They are not yet executed.

## Defer

- Scanned PDFs, OCR, audio, video, speaker identification, phonetic search.
- The marketing eleven-strata diagram as eleven tables. Segments and scans matter for recordings this MVP does not take.
- Automatic document-type classification. Category is human for the demo. An unconfirmed guess must not feed `answer`.
- Multi-agent council, adjudicator models, rerankers, million-node graphs, Postgres, event buses, materialized views.
- A general legal ontology and a general ontology editor. The demo ontology is the four propositions above.
- Free-form semantic questions over arbitrary uploads. Until a confirmed derivation exists, the honest result is abstain plus the stored text.
- Accounts, encryption, audit logs, multi-user notebooks, data-residency claims.
- Treating a local web page as proof of offline inference.

## Sources

- <https://perkara.ai/> and public bundle `/assets/index-DlM17x7b.js`, fetched 2026-11-10. Vendor marketing copy.
- <https://x.com/ibamarief/status/2117104412824944848>, plus author posts `2118379528137613823`, `2118380643294023764`, `2118721930106908863`, `2119826812704539022`, `2119829600578707671`. Public posts. Screenshots not inspected.
- <https://x.com/PerkaraAI> posts `2113828171959370125` and `2119703235086975273`. Short product claims.
- <https://tirto.id/perkara-ai-inovasi-ibam-arief-melawan-kriminalisasi-hukum-hEti>. Interview, not a spec.
- Local tool check only: `python3 --version`, `sqlite3 -version`, `grok --version`, `grok help`. No model prompt was run.
