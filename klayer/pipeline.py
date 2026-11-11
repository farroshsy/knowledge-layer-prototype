"""Ingest, publication, correction, and grounded lookup."""

from __future__ import annotations

import re

from klayer.domain import conflicting_pairs, lexical_draft, locate, rollup
from klayer.providers import ProviderError, ProviderOutcome, lexical_outcome
from klayer.store import Store, new_id

MAX_BODY = 200_000


class PipelineError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _sections_for_provider(rows: list[dict]) -> list[dict]:
    return [
        {
            "ordinal": row["ordinal"],
            "start": row["start_offset"],
            "end": row["end_offset"],
            "text": row["text"],
            "id": row["id"],
        }
        for row in rows
    ]


def _run_provider(provider, sections: list[dict], forced_category: str | None) -> ProviderOutcome:
    if provider == "rules" or provider is None:
        return lexical_outcome(sections, forced_category)
    try:
        return provider.extract(sections, forced_category)
    except ProviderError as exc:
        fallback = lexical_outcome(sections, forced_category)
        fallback.provider_error = str(exc)
        fallback.warnings.append("online provider failed; published local-rules output")
        fallback.method = "rules"
        fallback.label = "local-rules"
        return fallback


def _publication(store: Store, document: dict, sections: list[dict], outcome: ProviderOutcome) -> dict:
    generation = store.next_generation(document["id"])
    classifications = []
    claims = []
    fields = []
    body = document["body"]
    by_ordinal = {item.ordinal: item for item in outcome.sections}
    for section in sections:
        draft = by_ordinal[section["ordinal"]]
        evidence_span = locate(section, draft.evidence_quote) if draft.evidence_quote else None
        classifications.append(
            {
                "id": new_id(),
                "section_id": section["id"],
                "category": draft.category,
                "reason": draft.reason,
                "evidence_quote": draft.evidence_quote,
                "evidence_start": evidence_span[0] if evidence_span else None,
                "evidence_end": evidence_span[1] if evidence_span else None,
                "method": draft.method,
                "provider_label": draft.provider_label,
            }
        )
        for claim in draft.claims:
            span = locate(section, claim.quote)
            if not span or body[span[0] : span[1]] != claim.quote:
                outcome.warnings.append("rejected claim whose span is not the source text")
                continue
            claims.append(
                {
                    "id": new_id(),
                    "section_id": section["id"],
                    "quote": claim.quote,
                    "start_offset": span[0],
                    "end_offset": span[1],
                    "polarity": claim.polarity,
                    "modality": claim.modality,
                    "attribution": claim.attribution,
                    "predicate": claim.predicate,
                    "method": claim.method,
                    "provider_label": claim.provider_label,
                }
            )
        for item in draft.fields:
            span = locate(section, item.quote)
            if not span or body[span[0] : span[1]] != item.quote:
                outcome.warnings.append("rejected field whose span is not the source text")
                continue
            fields.append(
                {
                    "id": new_id(),
                    "section_id": section["id"],
                    "name": item.name,
                    "value": item.value,
                    "quote": item.quote,
                    "start_offset": span[0],
                    "end_offset": span[1],
                    "method": item.method,
                    "provider_label": item.provider_label,
                }
            )
    return {
        "document_id": document["id"],
        "notebook_id": document["notebook_id"],
        "generation": generation,
        "section_ids": [section["id"] for section in sections],
        "classifications": classifications,
        "claims": claims,
        "fields": fields,
        "relations": [],
        "warnings": outcome.warnings,
        "provider_method": outcome.method,
        "provider_label": outcome.label,
        "provider_error": outcome.provider_error,
    }


def _guard_evidence(sections: list[dict], outcome: ProviderOutcome, forced_category: str | None) -> None:
    """A non-other category must cite text in the section, unless the user set it."""
    lexical = {item.ordinal: item for item in lexical_draft(sections, forced_category)}
    kept = []
    for section in sections:
        draft = next(item for item in outcome.sections if item.ordinal == section["ordinal"])
        needs_evidence = draft.method != "user" and draft.category != "other"
        if needs_evidence and (not draft.evidence_quote or draft.evidence_quote not in section["text"]):
            outcome.warnings.append(
                f"section {section['ordinal']}: rejected category without an in-source evidence quote"
            )
            kept.append(lexical[section["ordinal"]])
            continue
        kept.append(draft)
    outcome.sections = kept


def _replace_relations(store: Store, notebook_id: str, pairs: list[tuple[str, str, str]]) -> None:
    with store._lock:
        try:
            store._conn.execute("BEGIN")
            store._conn.execute(
                "UPDATE relations SET state='stale' WHERE notebook_id=? AND state='active'",
                (notebook_id,),
            )
            for left, right, kind in pairs:
                store._conn.execute(
                    "INSERT INTO relations(id, notebook_id, left_claim_id, right_claim_id, kind, state) "
                    "VALUES (?, ?, ?, ?, ?, 'active')",
                    (new_id(), notebook_id, left, right, kind),
                )
            store._conn.execute("COMMIT")
        except Exception:
            store._conn.execute("ROLLBACK")
            raise


def process_job(store: Store, job_id: str, provider) -> dict | None:
    running = store.mark_running(job_id)
    if running is None:
        return store.get_job(job_id)
    context = store.document_context(running["document_id"])
    if context is None:
        store.mark_failed(job_id, "document missing")
        return store.get_job(job_id)
    sections = _sections_for_provider(context["sections"])
    try:
        outcome = _run_provider(provider, sections, None)
        _guard_evidence(sections, outcome, None)
        publication = _publication(store, context["document"], sections, outcome)
        publication["job_id"] = job_id
        store.publish(job_id, publication)
        pairs = conflicting_pairs(store.active_claims(context["document"]["notebook_id"]))
        _replace_relations(store, context["document"]["notebook_id"], pairs)
    except Exception as exc:
        store.mark_failed(job_id, str(exc)[:800])
    return store.get_job(job_id)


def upload(store: Store, notebook_id: str, filename: str, body: str, provider) -> dict:
    if store.get_notebook(notebook_id) is None:
        raise PipelineError("not_found", "notebook not found")
    if not isinstance(body, str) or not body.strip():
        raise PipelineError("validation", "document text is empty")
    if len(body) > MAX_BODY:
        raise PipelineError("validation", "document is larger than 200000 characters")
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise PipelineError("validation", "filename must be a plain label, not a path")
    from klayer.domain import parse_sections

    parsed = parse_sections(body)
    if not parsed:
        raise PipelineError("validation", "document has no text")
    created = store.insert_upload(notebook_id, filename, body, parsed)
    if not created["created"]:
        return created
    process_job(store, created["job"]["id"], provider)
    created["job"] = store.get_job(created["job"]["id"])
    return created


def retry_job(store: Store, job_id: str, provider) -> dict:
    job = store.queue_retry(job_id)
    if job is None:
        raise PipelineError("not_found", "job not found")
    if job["status"] == "queued":
        process_job(store, job_id, provider)
        return store.get_job(job_id)
    return job


def correct_category(store: Store, section_id: str, category: str, provider) -> dict:
    from klayer.domain import CATEGORIES

    if category not in CATEGORIES or category == "mixed":
        raise PipelineError("validation", "category is not one of the notebook definitions")
    row = store.section_row(section_id)
    if row is None:
        raise PipelineError("not_found", "section not found")
    context = store.document_context(row["document_id"])
    section = _sections_for_provider([row])[0]
    outcome = _run_provider(provider, [section], category)
    for draft in outcome.sections:
        draft.method = "user"
        draft.reason = "koreksi pengguna"
        draft.category = category
    _guard_evidence([section], outcome, category)
    publication = _publication(store, context["document"], [section], outcome)
    job = store.latest_job(context["document"]["id"])
    publication["job_id"] = job["id"]
    store.publish(job["id"], publication)
    _replace_relations(store, context["document"]["notebook_id"], conflicting_pairs(
        store.active_claims(context["document"]["notebook_id"])
    ))
    return store.document_view(context["document"]["id"])


def document_category(view: dict) -> str:
    categories = []
    for section in view["sections"]:
        classification = section.get("classification")
        if classification and classification["state"] == "active":
            categories.append(classification["category"])
    return rollup(categories)


def structured_query(store: Store, notebook_id: str, intent: dict) -> dict:
    if store.get_notebook(notebook_id) is None:
        raise PipelineError("not_found", "notebook not found")
    action = intent.get("intent")
    if action == "compare_claims":
        relations = store.active_relations(notebook_id)
        claims = {claim["id"]: claim for claim in store.active_claims(notebook_id)}
        rows = []
        for relation in relations:
            rows.append(
                {
                    "kind": relation["kind"],
                    "left": claims.get(relation["left_claim_id"]),
                    "right": claims.get(relation["right_claim_id"]),
                }
            )
        return {
            "inference": "stored-relations",
            "semantic": False,
            "answer": "conflicts" if rows else "abstain",
            "reason": "no active conflict" if not rows else "both claims remain",
            "relations": rows,
        }
    if action != "list_claims":
        raise PipelineError("validation", "intent must be list_claims or compare_claims")
    polarity = intent.get("polarity") or None
    modality = intent.get("modality") or None
    predicate = intent.get("predicate") or None
    contains = intent.get("quote_contains") or None
    for value, allowed in (
        (polarity, {"affirmed", "negated", None}),
        (modality, {"asserted", "plan", None}),
        (predicate, {"attendance", "pilot", None}),
    ):
        if value not in allowed:
            raise PipelineError("validation", "query filter is not in the allow list")
    if contains is not None and (not isinstance(contains, str) or len(contains) > 80):
        raise PipelineError("validation", "quote_contains must be a short string")
    claims = store.search_claims(notebook_id, polarity, modality, predicate, contains)
    if not claims:
        return {
            "inference": "structured-lookup",
            "semantic": False,
            "answer": "abstain",
            "reason": "no active claim matches the filters",
            "claims": [],
        }
    return {
        "inference": "structured-lookup",
        "semantic": False,
        "answer": "claims",
        "reason": "filters matched stored claims",
        "claims": claims,
    }


def lexical_question(store: Store, notebook_id: str, question: str) -> dict:
    """Labeled lexical lookup over stored claims. This is not semantic parsing."""
    text = question.strip()
    if re.search(r"hadir|ikut", text, re.I):
        result = structured_query(
            store,
            notebook_id,
            {"intent": "list_claims", "polarity": "affirmed", "predicate": "attendance"},
        )
    elif re.search(r"pilot", text, re.I) and re.search(r"berjalan|sudah|terjadi", text, re.I):
        result = structured_query(
            store,
            notebook_id,
            {"intent": "list_claims", "modality": "plan", "predicate": "pilot"},
        )
        result["answer"] = "plan_not_occurrence" if result["claims"] else "abstain"
        result["reason"] = (
            "only planned statements are stored"
            if result["claims"]
            else "no active claim matches the filters"
        )
    else:
        result = {
            "inference": "local-lexical",
            "semantic": False,
            "answer": "abstain",
            "reason": "no lexical pattern matched and no semantic planner ran",
            "claims": [],
        }
        return result
    result["inference"] = "local-lexical"
    result["semantic"] = False
    return result


def ask(store: Store, notebook_id: str, question: str, provider) -> dict:
    if not isinstance(question, str) or not question.strip():
        raise PipelineError("validation", "question is empty")
    planner = getattr(provider, "plan", None)
    if not callable(planner):
        return lexical_question(store, notebook_id, question)
    try:
        intent = planner(question)
    except ProviderError as exc:
        result = lexical_question(store, notebook_id, question)
        result["provider_error"] = str(exc)
        return result
    if not isinstance(intent, dict):
        raise PipelineError("validation", "invalid plan")
    if intent.get("intent") == "abstain":
        return {
            "inference": "online-grok-cli",
            "semantic": False,
            "offline_model": False,
            "answer": "abstain",
            "reason": "planner abstained",
            "claims": [],
        }
    cleaned = {"intent": intent.get("intent")}
    for key in ("polarity", "modality", "predicate", "quote_contains"):
        value = intent.get(key) or None
        cleaned[key] = value or None
    try:
        result = structured_query(store, notebook_id, cleaned)
    except PipelineError as exc:
        raise PipelineError("validation", "invalid plan: " + exc.message) from exc
    result["inference"] = "online-grok-cli"
    result["semantic"] = False
    result["offline_model"] = False
    return result
