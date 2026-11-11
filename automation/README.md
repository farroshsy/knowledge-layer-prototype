# Automatic Grok council

Started in Orca on 10 November 2026 at 21:12 WIB. The supervisor is a local process, not a hosted service: the Mac and Orca must remain running. No automatic push, submission, secret access or changes to the frozen AI Interview repository.

## Actual graph

Baseline → two independent parallel proposals → adjudicator → builder → two parallel adversarial reviews of the exact diff → fixed local tests → versioned accepted candidate → next round with previous findings.

Grok 4.7 handles proposals, adjudication, implementation and integrity review. Grok 4.7 Build Fast provides a second contract/test review. These are separate calls, not different model families or proof of statistical independence. Agreement alone never certifies correctness.

Default bounds are 8 rounds, 64 calls, 4 hours, two simultaneous calls, 480 seconds per call, and an absolute 11 November 06:30 WIB deadline. Two consecutive rounds without progress stop the run. Budgets are ceilings, not targets for wasting quota. Provider errors and failed tests are recorded rather than counted as success.

## Inspect or stop

Run from this project directory:

```sh
python3 automation/council.py status
python3 automation/council.py stop
```

Open `.council-runs/last-run.json` to locate the current run. Its `report.html`, `status.json`, `events.jsonl` and per-round JSON contain progress, model names, durations, proposals, decisions, review findings, exact diffs and test outputs. Reload the HTML for updates. Real provider usage is retained when returned; cost and remaining quota are unavailable, not estimated.

The report separates workflow activity from application quality. A running council does not imply semantic quality has been measured. See `docs/metrics-contract.md` for the application evaluation contract.

## Accepted candidate

`.council-runs/latest-approved.json` points to the most recently reviewed and tested candidate. It does not overwrite the original source. After inspecting the evidence, run:

```sh
python3 automation/council.py serve-latest
```

This verifies the accepted source hash and starts the candidate with a separate dummy database. Stop another server already using port 8765 first. Acceptance still requires testing real new documents, hybrid queries, citation support and appropriate abstention; legacy tests alone do not establish those claims.

## Verification of the controller

`python3 -m unittest automation.test_council` passed 13 tests on 10 November. A real tool-less Grok probe returned `{"ok": true}`. The live run was observed executing two proposals concurrently. No completed candidate was claimed at launch.

Model calls have no tools and receive bounded supplied text. The controller restricts file paths and runs fixed test commands. Candidate Python tests execute locally; this is not an operating-system security sandbox. Use only synthetic documents in this development loop. Remote Windows authentication is not established, and this run does not use the PC GPU.

## Restart deliberately

Do not start a second supervisor concurrently. A lock prevents overlapping runs. Inspect the last status and STOP file first; remove STOP only when deliberately starting another run. Each invocation starts a fresh baseline from the original project source; accepted candidates remain separately available for inspection. No calendar scheduler or automatic reboot recovery is installed.
