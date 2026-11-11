"""Parsing, category schemas, and labeled lexical extraction.

Lexical rules are not semantic inference. Callers must keep the method label.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

CATEGORIES = ("sop", "notulen", "proposal", "laporan_progres", "other")

CATEGORY_FIELDS = {
    "sop": ("langkah", "penanggung_jawab"),
    "notulen": ("peserta", "keputusan", "tindakan"),
    "proposal": ("tujuan", "anggaran"),
    "laporan_progres": ("capaian", "hambatan"),
    "other": (),
}

KEYWORDS = {
    "notulen": ("notulen", "peserta", "keputusan", "rapat"),
    "sop": ("sop", "prosedur", "langkah", "penanggung jawab"),
    "proposal": ("proposal", "latar belakang", "anggaran"),
    "laporan_progres": ("laporan progres", "capaian", "hambatan"),
}

FIELD_PATTERNS = {
    "peserta": re.compile(r"(?im)^peserta\s*:\s*(.+)$"),
    "keputusan": re.compile(r"(?im)^keputusan\s*:\s*(.+)$"),
    "tindakan": re.compile(r"(?im)^tindakan\s*:\s*(.+)$"),
    "langkah": re.compile(r"(?im)^langkah(?:\s*\d+)?\s*:\s*(.+)$"),
    "penanggung_jawab": re.compile(r"(?im)^penanggung jawab\s*:\s*(.+)$"),
    "tujuan": re.compile(r"(?im)^tujuan\s*:\s*(.+)$"),
    "anggaran": re.compile(r"(?im)^anggaran\s*:\s*(.+)$"),
    "capaian": re.compile(r"(?im)^capaian\s*:\s*(.+)$"),
    "hambatan": re.compile(r"(?im)^hambatan\s*:\s*(.+)$"),
}

DATE_RE = re.compile(
    r"\b\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|"
    r"September|Oktober|November|Desember)\b"
)
NAME_RE = re.compile(r"\b[A-Z][a-z]{2,}\b")


@dataclass
class ClaimDraft:
    quote: str
    polarity: str
    modality: str
    attribution: str
    predicate: str
    method: str
    provider_label: str


@dataclass
class FieldDraft:
    name: str
    value: str
    quote: str
    method: str
    provider_label: str


@dataclass
class SectionDraft:
    ordinal: int
    category: str
    reason: str
    evidence_quote: str
    method: str
    provider_label: str
    claims: list[ClaimDraft] = field(default_factory=list)
    fields: list[FieldDraft] = field(default_factory=list)


def parse_sections(body: str) -> list[dict]:
    """Split a document on blank lines. Offsets refer to the original body."""
    sections: list[dict] = []
    lines = body.splitlines(keepends=True)
    buf: list[str] = []
    buf_start = 0
    pos = 0

    def flush() -> None:
        nonlocal buf
        raw = "".join(buf)
        buf = []
        if not raw.strip():
            return
        lead = len(raw) - len(raw.lstrip("\n"))
        text = raw.strip()
        start = buf_start + lead
        end = start + len(text)
        if body[start:end] != text:
            start = body.find(text, buf_start)
            end = start + len(text)
        sections.append(
            {"ordinal": len(sections), "start": start, "end": end, "text": text}
        )

    for line in lines:
        if line.strip() == "":
            if buf:
                flush()
            pos += len(line)
            buf_start = pos
        else:
            if not buf:
                buf_start = pos
            buf.append(line)
            pos += len(line)
    if buf:
        flush()
    for section in sections:
        if body[section["start"] : section["end"]] != section["text"]:
            raise ValueError("section offset does not match source text")
    return sections


def _keyword_hits(text: str, category: str) -> list[str]:
    low = text.lower()
    return [word for word in KEYWORDS[category] if word in low]


def classify_lexical(text: str) -> tuple[str, str, str]:
    scores = {name: _keyword_hits(text, name) for name in KEYWORDS}
    best = max(len(hits) for hits in scores.values())
    if best == 0:
        return "other", "tidak ada kata kunci kategori", ""
    winners = [name for name, hits in scores.items() if len(hits) == best]
    if len(winners) != 1:
        return "other", "kata kunci dua kategori sama kuat", ""
    category = winners[0]
    hits = scores[category]
    evidence = hits[0]
    idx = text.lower().find(evidence)
    quote = text[idx : idx + len(evidence)]
    reason = "kecocokan leksikal: " + ", ".join(hits)
    return category, reason, quote


def _sentences(text: str) -> list[tuple[int, str]]:
    found = []
    for match in re.finditer(r"[^.!?\n]+(?:[.!?]|$)", text):
        raw = match.group(0)
        stripped = raw.strip()
        if len(stripped) < 8:
            continue
        lead = len(raw) - len(raw.lstrip())
        start = match.start() + lead
        if text[start : start + len(stripped)] != stripped:
            continue
        found.append((start, stripped))
    return found


def _claim_from_sentence(sentence: str, method: str, label: str) -> ClaimDraft:
    polarity = "negated" if re.search(r"\b(tidak|bukan|belum)\b", sentence, re.I) else "affirmed"
    modality = (
        "plan"
        if re.search(r"\b(direncanakan|rencana|dijadwalkan)\b", sentence, re.I)
        else "asserted"
    )
    attribution = ""
    who = re.search(r"\bMenurut\s+([^,.]{1,40})", sentence)
    if who:
        attribution = who.group(1).strip()
    predicate = ""
    if re.search(r"hadir|ikut meeting|mengikuti", sentence, re.I):
        predicate = "attendance"
    elif re.search(r"\bpilot\b", sentence, re.I):
        predicate = "pilot"
    return ClaimDraft(
        quote=sentence,
        polarity=polarity,
        modality=modality,
        attribution=attribution,
        predicate=predicate,
        method=method,
        provider_label=label,
    )


def lexical_draft(sections: list[dict], forced_category: str | None = None) -> list[SectionDraft]:
    drafts = []
    for section in sections:
        text = section["text"]
        if forced_category:
            if forced_category not in CATEGORIES:
                raise ValueError(f"unknown category: {forced_category}")
            category = forced_category
            reason = "koreksi pengguna"
            evidence = ""
            method = "user"
        else:
            category, reason, evidence = classify_lexical(text)
            method = "rules"
        claims = [
            _claim_from_sentence(sentence, "rules", "local-rules")
            for _, sentence in _sentences(text)
        ]
        fields = []
        for name in CATEGORY_FIELDS[category]:
            for match in FIELD_PATTERNS[name].finditer(text):
                line = match.group(0).strip()
                if line not in text:
                    continue
                fields.append(
                    FieldDraft(
                        name=name,
                        value=match.group(1).strip(),
                        quote=line,
                        method="rules",
                        provider_label="local-rules",
                    )
                )
        drafts.append(
            SectionDraft(
                ordinal=section["ordinal"],
                category=category,
                reason=reason,
                evidence_quote=evidence,
                method=method,
                provider_label="local-rules",
                claims=claims,
                fields=fields,
            )
        )
    return drafts


def locate(section: dict, quote: str) -> tuple[int, int] | None:
    if not quote or quote not in section["text"]:
        return None
    idx = section["text"].find(quote)
    start = section["start"] + idx
    end = start + len(quote)
    return start, end


def rollup(categories: list[str]) -> str:
    active = {item for item in categories if item}
    if len(active) == 1:
        return next(iter(active))
    if not active:
        return "other"
    return "mixed"


def conflicting_pairs(claims: list[dict]) -> list[tuple[str, str, str]]:
    """Return (left_id, right_id, kind) for active claims that disagree."""
    pairs = []
    seen = set()
    dated = []
    for claim in claims:
        dates = DATE_RE.findall(claim["quote"])
        if claim["predicate"] == "pilot" and claim["modality"] == "plan" and dates:
            dated.append((claim, dates[0]))
    for i, (left, left_date) in enumerate(dated):
        for right, right_date in dated[i + 1 :]:
            if left_date != right_date:
                key = tuple(sorted((left["id"], right["id"])))
                if key not in seen:
                    seen.add(key)
                    pairs.append((left["id"], right["id"], "conflict"))
    attendance = [claim for claim in claims if claim["predicate"] == "attendance"]
    for i, left in enumerate(attendance):
        left_names = set(NAME_RE.findall(left["quote"]))
        for right in attendance[i + 1 :]:
            if left["polarity"] == right["polarity"]:
                continue
            if left_names.isdisjoint(NAME_RE.findall(right["quote"])):
                continue
            key = tuple(sorted((left["id"], right["id"])))
            if key in seen:
                continue
            seen.add(key)
            pairs.append((left["id"], right["id"], "conflict"))
    return pairs
