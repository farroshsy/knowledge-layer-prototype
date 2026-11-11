"""SQLite notebook store. One connection, one lock, one publication transaction."""

from __future__ import annotations

import hashlib
import sqlite3
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS notebooks (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS documents (
  id TEXT PRIMARY KEY,
  notebook_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  content_hash TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL,
  UNIQUE (notebook_id, content_hash)
);
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL,
  status TEXT NOT NULL,
  error TEXT,
  warnings TEXT NOT NULL DEFAULT '',
  provider_method TEXT,
  provider_label TEXT,
  provider_error TEXT,
  attempt INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sections (
  id TEXT PRIMARY KEY,
  document_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL,
  start_offset INTEGER NOT NULL,
  end_offset INTEGER NOT NULL,
  text TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS classifications (
  id TEXT PRIMARY KEY,
  section_id TEXT NOT NULL,
  document_id TEXT NOT NULL,
  category TEXT NOT NULL,
  reason TEXT NOT NULL,
  evidence_quote TEXT NOT NULL,
  evidence_start INTEGER,
  evidence_end INTEGER,
  method TEXT NOT NULL,
  provider_label TEXT NOT NULL,
  state TEXT NOT NULL,
  generation INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS claims (
  id TEXT PRIMARY KEY,
  section_id TEXT NOT NULL,
  document_id TEXT NOT NULL,
  notebook_id TEXT NOT NULL,
  quote TEXT NOT NULL,
  start_offset INTEGER NOT NULL,
  end_offset INTEGER NOT NULL,
  polarity TEXT NOT NULL,
  modality TEXT NOT NULL,
  attribution TEXT NOT NULL,
  predicate TEXT NOT NULL,
  method TEXT NOT NULL,
  provider_label TEXT NOT NULL,
  state TEXT NOT NULL,
  generation INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS fields (
  id TEXT PRIMARY KEY,
  section_id TEXT NOT NULL,
  document_id TEXT NOT NULL,
  name TEXT NOT NULL,
  value TEXT NOT NULL,
  quote TEXT NOT NULL,
  start_offset INTEGER NOT NULL,
  end_offset INTEGER NOT NULL,
  method TEXT NOT NULL,
  provider_label TEXT NOT NULL,
  state TEXT NOT NULL,
  generation INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS relations (
  id TEXT PRIMARY KEY,
  notebook_id TEXT NOT NULL,
  left_claim_id TEXT NOT NULL,
  right_claim_id TEXT NOT NULL,
  kind TEXT NOT NULL,
  state TEXT NOT NULL
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return uuid.uuid4().hex


def content_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


class Store:
    def __init__(self, path: str | Path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(SCHEMA)
        self._conn.execute("INSERT OR IGNORE INTO schema_migrations(version) VALUES (1)")
        self._conn.execute(
            "UPDATE jobs SET status='failed', error='interrupted before publish', updated_at=? "
            "WHERE status='running'",
            (now(),),
        )
        self._conn.commit()

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def reopen(self) -> Store:
        path = self.path
        self.close()
        return Store(path)

    def _one(self, sql: str, args: tuple = ()) -> dict | None:
        row = self._conn.execute(sql, args).fetchone()
        return dict(row) if row else None

    def _all(self, sql: str, args: tuple = ()) -> list[dict]:
        return [dict(row) for row in self._conn.execute(sql, args).fetchall()]

    def create_notebook(self, name: str) -> dict:
        with self._lock:
            row = {
                "id": new_id(),
                "name": name.strip() or "Notebook",
                "created_at": now(),
            }
            self._conn.execute(
                "INSERT INTO notebooks(id, name, created_at) VALUES (:id, :name, :created_at)",
                row,
            )
            self._conn.commit()
            return row

    def list_notebooks(self) -> list[dict]:
        with self._lock:
            return self._all("SELECT * FROM notebooks ORDER BY created_at")

    def get_notebook(self, notebook_id: str) -> dict | None:
        with self._lock:
            return self._one("SELECT * FROM notebooks WHERE id=?", (notebook_id,))

    def find_document(self, notebook_id: str, digest: str) -> dict | None:
        with self._lock:
            return self._one(
                "SELECT * FROM documents WHERE notebook_id=? AND content_hash=?",
                (notebook_id, digest),
            )

    def latest_job(self, document_id: str) -> dict | None:
        with self._lock:
            return self._one(
                "SELECT * FROM jobs WHERE document_id=? ORDER BY created_at DESC LIMIT 1",
                (document_id,),
            )

    def insert_upload(self, notebook_id: str, filename: str, body: str, sections: list[dict]) -> dict:
        with self._lock:
            digest = content_hash(body)
            existing = self._one(
                "SELECT * FROM documents WHERE notebook_id=? AND content_hash=?",
                (notebook_id, digest),
            )
            if existing:
                job = self._one(
                    "SELECT * FROM jobs WHERE document_id=? ORDER BY created_at DESC LIMIT 1",
                    (existing["id"],),
                )
                return {"document": existing, "job": job, "created": False, "sections": []}
            document = {
                "id": new_id(),
                "notebook_id": notebook_id,
                "filename": filename or "untitled.txt",
                "content_hash": digest,
                "body": body,
                "created_at": now(),
            }
            self._conn.execute(
                "INSERT INTO documents(id, notebook_id, filename, content_hash, body, created_at) "
                "VALUES (:id, :notebook_id, :filename, :content_hash, :body, :created_at)",
                document,
            )
            stored_sections = []
            for section in sections:
                row = {
                    "id": new_id(),
                    "document_id": document["id"],
                    "ordinal": section["ordinal"],
                    "start_offset": section["start"],
                    "end_offset": section["end"],
                    "text": section["text"],
                }
                self._conn.execute(
                    "INSERT INTO sections(id, document_id, ordinal, start_offset, end_offset, text) "
                    "VALUES (:id, :document_id, :ordinal, :start_offset, :end_offset, :text)",
                    row,
                )
                stored_sections.append(row)
            job = {
                "id": new_id(),
                "document_id": document["id"],
                "status": "queued",
                "error": None,
                "warnings": "",
                "provider_method": None,
                "provider_label": None,
                "provider_error": None,
                "attempt": 1,
                "created_at": now(),
                "updated_at": now(),
            }
            self._conn.execute(
                "INSERT INTO jobs(id, document_id, status, error, warnings, provider_method, "
                "provider_label, provider_error, attempt, created_at, updated_at) "
                "VALUES (:id, :document_id, :status, :error, :warnings, :provider_method, "
                ":provider_label, :provider_error, :attempt, :created_at, :updated_at)",
                job,
            )
            self._conn.commit()
            return {
                "document": document,
                "job": job,
                "created": True,
                "sections": stored_sections,
            }

    def mark_running(self, job_id: str) -> dict | None:
        with self._lock:
            job = self._one("SELECT * FROM jobs WHERE id=?", (job_id,))
            if not job or job["status"] in ("running", "completed"):
                return None
            self._conn.execute(
                "UPDATE jobs SET status='running', error=NULL, updated_at=? WHERE id=?",
                (now(), job_id),
            )
            self._conn.commit()
            return self._one("SELECT * FROM jobs WHERE id=?", (job_id,))

    def mark_failed(self, job_id: str, error: str) -> None:
        with self._lock:
            self._conn.execute(
                "UPDATE jobs SET status='failed', error=?, updated_at=? WHERE id=? AND status!='completed'",
                (error[:800], now(), job_id),
            )
            self._conn.commit()

    def queue_retry(self, job_id: str) -> dict | None:
        with self._lock:
            job = self._one("SELECT * FROM jobs WHERE id=?", (job_id,))
            if not job:
                return None
            if job["status"] in ("running", "completed", "queued"):
                return job
            self._conn.execute(
                "UPDATE jobs SET status='queued', error=NULL, attempt=attempt+1, updated_at=? WHERE id=?",
                (now(), job_id),
            )
            self._conn.commit()
            return self._one("SELECT * FROM jobs WHERE id=?", (job_id,))

    def document_context(self, document_id: str) -> dict | None:
        with self._lock:
            document = self._one("SELECT * FROM documents WHERE id=?", (document_id,))
            if not document:
                return None
            sections = self._all(
                "SELECT * FROM sections WHERE document_id=? ORDER BY ordinal",
                (document_id,),
            )
            return {"document": document, "sections": sections}

    def section_row(self, section_id: str) -> dict | None:
        with self._lock:
            return self._one("SELECT * FROM sections WHERE id=?", (section_id,))

    def publish(self, job_id: str, publication: dict) -> None:
        """Replace active derivations inside one transaction."""
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                self._write_publication(publication)
                self._conn.execute(
                    "UPDATE jobs SET status='completed', error=NULL, warnings=?, "
                    "provider_method=?, provider_label=?, provider_error=?, updated_at=? WHERE id=?",
                    (
                        "\n".join(publication.get("warnings") or []),
                        publication["provider_method"],
                        publication["provider_label"],
                        publication.get("provider_error"),
                        now(),
                        job_id,
                    ),
                )
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    def _write_publication(self, publication: dict) -> None:
        document_id = publication["document_id"]
        notebook_id = publication["notebook_id"]
        generation = publication["generation"]
        section_ids = publication["section_ids"]
        marks = ",".join("?" for _ in section_ids)
        if section_ids:
            self._conn.execute(
                f"UPDATE classifications SET state='stale' WHERE section_id IN ({marks}) AND state='active'",
                section_ids,
            )
            self._conn.execute(
                f"UPDATE claims SET state='stale' WHERE section_id IN ({marks}) AND state='active'",
                section_ids,
            )
            self._conn.execute(
                f"UPDATE fields SET state='stale' WHERE section_id IN ({marks}) AND state='active'",
                section_ids,
            )
        for item in publication["classifications"]:
            self._conn.execute(
                "INSERT INTO classifications(id, section_id, document_id, category, reason, "
                "evidence_quote, evidence_start, evidence_end, method, provider_label, state, generation) "
                "VALUES (:id, :section_id, :document_id, :category, :reason, :evidence_quote, "
                ":evidence_start, :evidence_end, :method, :provider_label, 'active', :generation)",
                {**item, "document_id": document_id, "generation": generation},
            )
        claim_ids = []
        for item in publication["claims"]:
            claim_ids.append(item["id"])
            self._conn.execute(
                "INSERT INTO claims(id, section_id, document_id, notebook_id, quote, start_offset, "
                "end_offset, polarity, modality, attribution, predicate, method, provider_label, "
                "state, generation) VALUES (:id, :section_id, :document_id, :notebook_id, :quote, "
                ":start_offset, :end_offset, :polarity, :modality, :attribution, :predicate, :method, "
                ":provider_label, 'active', :generation)",
                {**item, "document_id": document_id, "notebook_id": notebook_id, "generation": generation},
            )
        for item in publication["fields"]:
            self._conn.execute(
                "INSERT INTO fields(id, section_id, document_id, name, value, quote, start_offset, "
                "end_offset, method, provider_label, state, generation) "
                "VALUES (:id, :section_id, :document_id, :name, :value, :quote, :start_offset, "
                ":end_offset, :method, :provider_label, 'active', :generation)",
                {**item, "document_id": document_id, "generation": generation},
            )
        self._conn.execute(
            "UPDATE relations SET state='stale' WHERE notebook_id=? AND state='active'",
            (notebook_id,),
        )
        for left, right, kind in publication["relations"]:
            self._conn.execute(
                "INSERT INTO relations(id, notebook_id, left_claim_id, right_claim_id, kind, state) "
                "VALUES (?, ?, ?, ?, ?, 'active')",
                (new_id(), notebook_id, left, right, kind),
            )

    def next_generation(self, document_id: str) -> int:
        with self._lock:
            row = self._one(
                "SELECT COALESCE(MAX(generation), 0) AS generation FROM classifications WHERE document_id=?",
                (document_id,),
            )
            return int(row["generation"]) + 1

    def get_job(self, job_id: str) -> dict | None:
        with self._lock:
            return self._one("SELECT * FROM jobs WHERE id=?", (job_id,))

    def active_claims(self, notebook_id: str) -> list[dict]:
        with self._lock:
            return self._all(
                "SELECT claims.*, documents.filename FROM claims "
                "JOIN documents ON documents.id=claims.document_id "
                "WHERE claims.notebook_id=? AND claims.state='active' ORDER BY claims.start_offset",
                (notebook_id,),
            )

    def search_claims(
        self,
        notebook_id: str,
        polarity: str | None = None,
        modality: str | None = None,
        predicate: str | None = None,
        quote_contains: str | None = None,
    ) -> list[dict]:
        clauses = ["notebook_id=?", "state='active'"]
        args: list = [notebook_id]
        if polarity:
            clauses.append("polarity=?")
            args.append(polarity)
        if modality:
            clauses.append("modality=?")
            args.append(modality)
        if predicate:
            clauses.append("predicate=?")
            args.append(predicate)
        if quote_contains:
            escaped = quote_contains.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            clauses.append("quote LIKE ? ESCAPE '\\'")
            args.append(f"%{escaped}%")
        sql = "SELECT * FROM claims WHERE " + " AND ".join(clauses) + " ORDER BY start_offset"
        with self._lock:
            return self._all(sql, tuple(args))

    def active_relations(self, notebook_id: str) -> list[dict]:
        with self._lock:
            return self._all(
                "SELECT * FROM relations WHERE notebook_id=? AND state='active'",
                (notebook_id,),
            )

    def document_view(self, document_id: str) -> dict | None:
        with self._lock:
            document = self._one("SELECT * FROM documents WHERE id=?", (document_id,))
            if not document:
                return None
            sections = self._all(
                "SELECT * FROM sections WHERE document_id=? ORDER BY ordinal",
                (document_id,),
            )
            for section in sections:
                section["classification"] = self._one(
                    "SELECT * FROM classifications WHERE section_id=? AND state='active'",
                    (section["id"],),
                )
                section["fields"] = self._all(
                    "SELECT * FROM fields WHERE section_id=? AND state='active'",
                    (section["id"],),
                )
            claims = self._all(
                "SELECT * FROM claims WHERE document_id=? AND state='active' ORDER BY start_offset",
                (document_id,),
            )
            job = self._one(
                "SELECT * FROM jobs WHERE document_id=? ORDER BY created_at DESC LIMIT 1",
                (document_id,),
            )
            stale = self._all(
                "SELECT id, name, value, state FROM fields WHERE document_id=? AND state='stale'",
                (document_id,),
            )
            return {
                "document": document,
                "sections": sections,
                "claims": claims,
                "job": job,
                "stale_fields": stale,
            }

    def count_active_claims(self, document_id: str) -> int:
        with self._lock:
            row = self._one(
                "SELECT COUNT(*) AS n FROM claims WHERE document_id=? AND state='active'",
                (document_id,),
            )
            return int(row["n"])

    def table_exists(self, name: str) -> bool:
        with self._lock:
            row = self._one(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (name,),
            )
            return row is not None
