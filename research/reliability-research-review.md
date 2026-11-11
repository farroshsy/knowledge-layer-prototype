# Reliability research review — Grok synthesis

Source notes were fetched by coordinator; this worker had no independent browser. Recommendations are not implemented controls or executed tests.

Tomorrow 08:00 WIB delivery is a working PoC of independent business records plus unseen documents with a grounded combined answer. It is not accepted: no candidate is selected, quality is unmeasured, and the only HTTP runs (Grok 5/6, rules 6/6) omit that hybrid route. Grok already failed once on fallback timeout, so a full live Grok pass and offline inference are contradicted. Demo blockers are hybrid retrieval, claim support versus citations, temporal and attribution wording, same-name identity, the provider failure, and a second-person rerun. Format risk stays on the demo list only for formats the candidate already claims. Injection, workspace scope, parser limits, privacy, and stronger persistence evidence gate any real-data pilot. ROI, authenticated deployment, WAL changes, and accessibility are conditional later work. Cited notes supply general controls; the fixtures are proposed acceptance checks. This is not an audit or a compliance determination.


## Findings

- P0 demo-blocker | business workflow + hybrid retrieval | acceptance = three HTTP cases on one fresh workspace: (1) a business fact present only in records and absent from all document text, (2) a fact present only in an unseen document and absent from records, (3) a combined answer that keeps those sources distinct | status not_measured | grok-http-01 5/6 and rules-http-01 6/6 both state this baseline protocol did not exercise independent records or the hybrid route; accepted candidate pointer is false; accepted count is 0 | source-backed: context recall needs a defined reference, and a plausible answer is not a recall measurement (https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/); record queries use bound parameters and allowlisted identifiers, and model-written arbitrary SQL stays out of the path (https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | proposed project control: frozen synthetic fixtures plus saved request/response transcripts in a new acceptance-run directory; rules 6/6 remains a baseline result only

- P0 demo-blocker | supported assertions vs citation validity | acceptance = three independent bits on one answer: exact source location, active document version, and entailment of each atomic claim by the retrieved span; a present-looking citation with an unsupported claim fails that claim | status not_measured; both HTTP runs state they are not a full semantic-support evaluation | source-backed: faithfulness judges support by retrieved context, and span validity is a separate check (https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) | proposed project control: fixture oracle on synthetic claims; agreement between grok and rules is an invalid proof of correctness under the current claim limits

- P0 demo-blocker | temporal, polarity, attribution | acceptance = a planning or proposal statement stays a plan; it is neither an occurrence nor evidence of non-occurrence; negation and speaker stay attached to the named source | status not_measured | source-backed control is the same faithfulness check against retrieved context (https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) | proposed fixtures: gold labels for planned, did-not-occur, and attributed report as three different outcomes

- P0 demo-blocker | identity | acceptance = two people with the same display name and different IDs, and no confirmed link, stay ambiguous in the answer and in any stored link | status not_measured | source-backed: provenance records entities, activities, and agents for a derivation; lineage supports assessment and does not prove truth or identity (https://www.w3.org/TR/prov-overview/) | proposed control: same-name fixture pair and a negative test that shared name alone creates no link

- P0 observed-failure | provider timeout, fallback, subprocess boundary | acceptance = one live Grok HTTP ingestion with nested job method, error, exit status, and wall time stored; a timeout remains in the sample; any rules fallback is labeled with the method that actually ran; parent timeout is only parent-timeout evidence | status failed | .acceptance-runs/grok-http-01/results.json is 5/6 with fallback timeout, so the claim that all live Grok checks passed is contradicted; the claim that all inference is local/offline is false for Grok because the Grok CLI uses online inference | source-backed: explicit argument lists, timeouts, and exit handling; a parent timeout does not establish full descendant cleanup (https://docs.python.org/3.14/library/subprocess.html) | proposed control: read the existing nested error metadata before any provider change; tomorrow’s demo can use a clearly labeled non-Grok path only if a human accepts that path

- P0 demo-risk | document data quality | acceptance = if PDF or DOCX is in tomorrow’s demo, one text-bearing file yields non-empty extracted text tied to that upload; an image-only/scanned PDF yields an explicit failure or explicit empty-extraction flag, never silent empty success | status not_measured; native PDF/DOCX not exercised | source-backed: format allowlist, size limits, safe names, storage boundaries, and content verification before parsing (https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | proposed control: keep the 08:00 demo on already-supported text fixtures unless the selected candidate already claims PDF/DOCX

- P0 delivery | reproducibility / handoff | acceptance = a second person starts the selected candidate, inserts fresh synthetic rows, restarts, and repeats one hybrid query with the same pass/fail | status not_measured; latest_release is null; quality_metrics not_measured; build status working with 3 calls and elapsed_s 87.466 is run health only | source-backed: generative-AI risk assessment covers design, development, use, and evaluation, and a passing demo is not production certification (https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | proposed control: one run card and one repeated query; snapshot hash 33bb16de2a5ac6f15633d6188d33572c3cb82d61b1f72896b8793f6359e06221 identifies this context file and is not answer-truth provenance

- P1 before real-data pilot | document prompt injection | acceptance = a synthetic upload that tells the model to ignore workspace scope or execute SQL yields a bounded plan, and business row counts plus content hashes stay unchanged | status not_measured | source-backed: retrieved documents can carry instructions; prompts and RAG alone do not remove injection; bound privileges and validate outputs (https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | proposed control: one hostile synthetic file as a pilot gate, with data-diff evidence

- P1 before real-data pilot | SQL scope and access | acceptance = the same entity IDs in two notebooks return no cross-notebook rows; this local single-user PoC remains a PoC and is not an authenticated enterprise deployment | status not_measured | source-backed SQL control is parameterized data and allowlisted identifiers (https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | proposed control: two-workspace fixture; authorization productization stays outside tomorrow’s delivery

- P1 before real-data pilot | parser and supply surface | acceptance = installed parser names and versions, max upload size, and the result of a mismatched-content upload are recorded; the demo performs no unbounded auto-install | status not_measured | source-backed upload limits and content checks apply (https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) | proposed control: a version list taken from the environment that actually runs the candidate

- P1 integrity | persistence | acceptance = a failed retry leaves the previous active result in place; a duplicate content hash does not create a second active version; reopening the database returns the same active rows; required foreign keys are declared and enforcement is on for the connection used | status partial_baseline_tests | source-backed: relationships must be declared, and enabling enforcement on a connection does not create missing constraints (https://www.sqlite.org/foreignkeys.html) | proposed control: schema dump plus reopen transcript; WAL stays off the demo checklist because it changes concurrency, backup, and checkpoint behavior and is not a scalability label (https://www.sqlite.org/wal.html)

- P1 operations | latency and sample accounting | acceptance = every reported figure includes raw server wall time, sample count, and timeouts kept in the denominator | status partial_single_run | source-backed process limits are the subprocess timeout and exit-handling notes (https://docs.python.org/3.14/library/subprocess.html) | proposed control: extend the existing acceptance-run JSON; one partial run is not a concurrency result; cost and remaining_quota_percent are null

- P1 before real data | privacy | status open_decision; evidence in this effort uses synthetic inputs; real company documents wait on an authorized provider and data-handling decision; the Grok path is online | source-backed lifecycle point: use-phase risk is evaluated separately from a demo (https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | proposed control: synthetic-only corpus through 08:00 WIB delivery

- P2 after PoC | ROI and investment | acceptance = intended users complete the real task with measured time and cost against an agreed baseline | status not_measured; the PoC does not establish ROI or product-market fit | source-backed: evaluation is its own lifecycle activity (https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | proposed control: defer measurement until a candidate is accepted and a human sets the success threshold

- P2 conditional | accessibility | status not_measured; no accessibility result and no accessibility primary source are in the supplied evidence, so there is no WCAG or assistive-tech claim | both HTTP runs state they are not a browser interaction | proposed control: if tomorrow’s surface is the HTTP API, UI accessibility stays outside this acceptance; a later UI pilot needs a human pass over labels, keyboard completion, and error text

- Evidence limit | this matrix is a prioritized acceptance reading of the supplied register, two HTTP result summaries, and ten primary-source notes; it is not an exhaustive audit, penetration test, or compliance determination


## Proposed falsification checks

- E1 hybrid business workflow, before 08:00 WIB. Insert synthetic record R that appears in no document, and unseen document D whose fact appears in no record. HTTP DB-only query returns R and cites the record key. HTTP docs-only query returns D’s fact and cites D’s location. HTTP combined query states both facts and names the source of each. Evidence: new results JSON with the three transcripts, fixture hashes, and a checklist that R’s string is absent from extracted document text. Fail if either fact is missing, swapped, or merged into one unsupported sentence.

- E2 retrieval reference. Using the same fixtures, list the gold contexts for each question before the call. Pass only when each gold context is present in the retrieved set for that question. Evidence: gold list plus retrieved IDs. A fluent answer with an empty or wrong retrieved set fails. Recall stays unclaimed when no gold set exists (https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/).

- E3 citation versus support. For one combined answer, record location string, active version id, and a yes/no support bit per atomic claim against the retrieved span. Pass requires all three. Evidence: span excerpt, version id, and the bit table. A valid location with an unsupported claim fails faithfulness for that claim (https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/).

- E4 temporal and attribution. Fixtures: “meeting is planned,” “meeting did not occur,” and “A said B planned the meeting.” Expected answers preserve plan versus occurrence versus attribution. Evidence: source span next to the answer sentence. Fail on upgrade of a plan into a completed event, or on treating a plan as proof the event never happened.

- E5 identity. Create two entities, same display name, distinct IDs, no link record. Query by that name. Expected answer lists both IDs as unresolved or asks for a confirmed link, and the link table gains no row. Evidence: response body plus entity and link queries. Provenance of the answer, if shown, identifies sources and does not by itself assert the people are the same (https://www.w3.org/TR/prov-overview/).

- E6 Grok timeout path. Repeat one ingestion through the actual Grok HTTP entry and keep the raw job record. Expected stored fields: provider, method, error, exit, wall time. Timeout is a failed sample and stays in passed/total. If a fallback answer is returned, its method field is the fallback method. Evidence: results.json equivalent to .acceptance-runs/grok-http-01/results.json, which already contradicts a full Grok pass. Process evidence follows explicit argv, timeout, and exit handling; parent timeout alone does not prove child cleanup (https://docs.python.org/3.14/library/subprocess.html).

- E7 formats. If support is claimed: upload one small text PDF or DOCX on the allowlist and require non-empty text tied to the stored object; upload one image-only PDF and require an explicit empty or unsupported outcome. Evidence: extractor output, detected type, byte size, and stored name. Mismatched content fails closed. Limits follow the upload cheat sheet (https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html). If support is not claimed, record “text fixtures only” and skip new parsers.

- E8 injection. Upload a synthetic document whose body says to ignore scope and query another workspace or change rows. Expected: refusal or bounded plan, zero row changes, hashes unchanged. Evidence: before/after counts and hashes, plus the plan or SQL text that ran. Privilege bounds are the control; prompt wording is not the control (https://genai.owasp.org/llmrisk/llm01-prompt-injection/).

- E9 scope. Same entity IDs in notebook A and notebook B. Query from A. Expected: only A’s rows. Evidence: two result sets and the scope predicate used. Parameterized queries and allowlisted identifiers are the SQL evidence (https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html). This result does not establish enterprise authentication.

- E10 persistence. Force a retry failure, insert a duplicate content hash, restart the process, and reopen the database. Expected: one active result for the successful publication, no second active row for the duplicate, same active rows after reopen, foreign-key definitions present, enforcement on for that connection. Evidence: schema, PRAGMA foreign_keys for the live connection, and row dumps. Enabling the PRAGMA is insufficient when the constraint was never declared (https://www.sqlite.org/foreignkeys.html). Leave WAL mode unchanged unless a human explicitly accepts the backup and checkpoint effects (https://www.sqlite.org/wal.html).

- E11 handoff. A second person follows the run card: start the selected candidate, load fresh synthetic data, restart, repeat E1’s combined query. Expected: same pass/fail as the first operator. Evidence: their transcript and clock time. Missing selected candidate blocks this experiment.

- E12 metrics. Publish wall times for E1 and E6 with n and the timeout count. Expected: denominators include failures. Evidence: raw server timings. cost and quota stay unpublished while null.

- E13 accessibility, only if a UI is in scope. Human completes one upload and one hybrid question by keyboard and reads the error text for the scanned-PDF case. Expected: each step has a name and the error is in text. Evidence: tester notes. No UI in the current HTTP protocol means this experiment stays unrun and no conformance claim is made.

- E14 ROI, after a candidate is accepted. Intended users perform the business task with the tool and with their current method. Expected output is time and cost per completed task, compared with a threshold a human sets in advance. Evidence: task logs. Until that study exists, value status stays not_measured.


## Open decisions

- Which candidate, if any, is the accepted demo build? The accepted pointer is false, accepted count is 0, and latest_release is null. Delivery at 11 November 2026 08:00 Asia/Jakarta stays on that choice and the hybrid tests, ahead of new architecture.

- After the observed Grok fallback timeout, is a clearly labeled rules answer acceptable for the demo, or is a live Grok success required? Online Grok inference cannot be described as local/offline.

- Are PDF and DOCX inside tomorrow’s acceptance, or are text fixtures the demo corpus? Adding parsers before 08:00 competes with the hybrid blocker.

- Who will authorize any later use of real company documents, and under which provider terms? Until that decision, inputs stay synthetic and private documents stay out.

- Is cross-notebook isolation a tomorrow demo fixture or a gate only before a real-data pilot? The local single-user PoC does not become an enterprise access-control product by passing one fixture.

- Is any browser UI in tomorrow’s acceptance? If yes, who performs the accessibility pass? Current evidence has no browser interaction and no accessibility result.

- Who owns post-PoC ROI measurement, what task is timed, and what time/cost delta counts as success?

- Does anyone explicitly want SQLite WAL enabled? Default for this delivery is to leave it unchanged because it alters concurrency, backup, and checkpoints.

- Confirm the frozen ai-interview-platform tree stays untouched and this work stays unpushed, with no secrets and no publication.


## Primary references

- [Prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) — Retrieved documents can carry instructions; prompts and RAG alone do not eliminate injection. Bound privileges and validate outputs.

- [File upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html) — Use format allowlists, size limits, safe names and storage boundaries; verify actual content before parsing.

- [SQL injection](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) — Bind data using parameters and allowlist dynamic identifiers. Do not execute model-generated arbitrary SQL.

- [AI risk lifecycle](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) — Risk assessment spans design, development, use and evaluation. A passing demo is not production certification.

- [Provenance](https://www.w3.org/TR/prov-overview/) — Track entities, activities and agents responsible for derivations. Lineage supports assessment; it does not prove truth.

- [Answer support](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) — Assess whether assertions are supported by retrieved context; source span validity is a separate check.

- [Retrieval recall](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/) — Recall evaluation requires a defined reference; do not infer recall from plausible-looking responses.

- [SQLite constraints](https://www.sqlite.org/foreignkeys.html) — Declare relationships and enable enforcement on connections; PRAGMA alone does not create missing constraints.

- [SQLite concurrency](https://www.sqlite.org/wal.html) — WAL changes concurrency and backup/checkpoint behavior. Do not turn it on merely as a scalability label.

- [Provider process boundary](https://docs.python.org/3.14/library/subprocess.html) — Use explicit argument lists, controlled timeouts and exit handling. Parent timeout does not establish all descendant cleanup.