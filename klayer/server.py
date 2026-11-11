"""Loopback HTTP API and a small inspection page."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from klayer.domain import CATEGORIES, CATEGORY_FIELDS
from klayer.pipeline import (
    PipelineError,
    ask,
    correct_category,
    document_category,
    retry_job,
    structured_query,
    upload,
)
from klayer.store import Store

STATIC = Path(__file__).with_name("static")
MAX_REQUEST = 250_000


class App:
    def __init__(self, store: Store, provider):
        self.store = store
        self.provider = provider


def make_handler(app: App):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:
            return

        def _send(self, status: int, payload: dict | None = None, body: bytes | None = None, content_type: str = "application/json") -> None:
            data = body if body is not None else json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _read_json(self) -> dict:
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_REQUEST:
                raise PipelineError("validation", "request body is too large")
            raw = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise PipelineError("validation", "request body is not JSON") from exc
            if not isinstance(data, dict):
                raise PipelineError("validation", "JSON object required")
            return data

        def _error(self, exc: PipelineError) -> None:
            status = {"not_found": 404, "validation": 400}.get(exc.code, 400)
            self._send(status, {"error": exc.message, "code": exc.code})

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            try:
                if path == "/" or path == "/index.html":
                    page = (STATIC / "index.html").read_bytes()
                    self._send(200, body=page, content_type="text/html; charset=utf-8")
                    return
                if path == "/api/categories":
                    self._send(200, {"categories": {name: list(fields) for name, fields in CATEGORY_FIELDS.items()}})
                    return
                if path == "/api/notebooks":
                    self._send(200, {"notebooks": app.store.list_notebooks()})
                    return
                if path.startswith("/api/jobs/"):
                    job = app.store.get_job(path.split("/")[-1])
                    if job is None:
                        raise PipelineError("not_found", "job not found")
                    self._send(200, {"job": job})
                    return
                if path.startswith("/api/documents/"):
                    view = app.store.document_view(path.split("/")[-1])
                    if view is None:
                        raise PipelineError("not_found", "document not found")
                    view["category"] = document_category(view)
                    view["offline_model"] = False
                    self._send(200, view)
                    return
                self._send(404, {"error": "not found", "code": "not_found"})
            except PipelineError as exc:
                self._error(exc)

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            try:
                if path == "/api/notebooks":
                    data = self._read_json()
                    notebook = app.store.create_notebook(str(data.get("name") or "Notebook"))
                    self._send(201, {"notebook": notebook, "categories": list(CATEGORIES)})
                    return
                if path.startswith("/api/notebooks/") and path.endswith("/documents"):
                    notebook_id = path.split("/")[3]
                    data = self._read_json()
                    created = upload(
                        app.store,
                        notebook_id,
                        str(data.get("filename") or "catatan.txt"),
                        str(data.get("text") or ""),
                        app.provider,
                    )
                    status = 200 if not created["created"] else 201
                    self._send(status, created)
                    return
                if path.startswith("/api/notebooks/") and path.endswith("/query"):
                    notebook_id = path.split("/")[3]
                    data = self._read_json()
                    if data.get("question"):
                        result = ask(app.store, notebook_id, str(data["question"]), app.provider)
                    else:
                        result = structured_query(app.store, notebook_id, data)
                    self._send(200, result)
                    return
                if path.startswith("/api/jobs/") and path.endswith("/retry"):
                    job_id = path.split("/")[3]
                    job = retry_job(app.store, job_id, app.provider)
                    self._send(200, {"job": job})
                    return
                if path.startswith("/api/sections/") and path.endswith("/category"):
                    section_id = path.split("/")[3]
                    data = self._read_json()
                    view = correct_category(app.store, section_id, str(data.get("category") or ""), app.provider)
                    view["category"] = document_category(view)
                    self._send(200, view)
                    return
                self._send(404, {"error": "not found", "code": "not_found"})
            except PipelineError as exc:
                self._error(exc)

    return Handler


def serve(store: Store, provider, host: str, port: int) -> ThreadingHTTPServer:
    if host != "127.0.0.1":
        raise RuntimeError("the server only binds to 127.0.0.1")
    server = ThreadingHTTPServer((host, port), make_handler(App(store, provider)))
    return server
