"""Start the local notebook, seed demo text, or smoke-test Grok CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from klayer.domain import parse_sections
from klayer.pipeline import upload
from klayer.providers import GrokCliProvider, build_provider
from klayer.server import serve
from klayer.store import Store


def _seed(store: Store, folder: Path) -> str:
    notebook = store.create_notebook("Operasional dummy")
    for path in sorted(folder.glob("*.md")):
        upload(store, notebook["id"], path.name, path.read_text(encoding="utf-8"), "rules")
    return notebook["id"]


def _serve(args: argparse.Namespace) -> None:
    store = Store(args.db)
    if args.seed:
        _seed(store, Path(args.seed))
    provider = build_provider(args.provider)
    server = serve(store, provider, "127.0.0.1", args.port)
    print(f"http://127.0.0.1:{args.port}", flush=True)
    print(f"provider={args.provider} offline_model=false", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


def _smoke(args: argparse.Namespace) -> None:
    nonce = args.nonce
    text = (
        f"Notulen rapat operasional.\n"
        f"Peserta: Sari.\n"
        f"Keputusan: pilot direncanakan mulai 15 November.\n"
        f"Kode unik {nonce} ditulis di sini."
    )
    sections = parse_sections(text)
    outcome = GrokCliProvider(timeout=args.timeout).extract(sections, None)
    grok_quotes = [
        claim.quote
        for draft in outcome.sections
        for claim in draft.claims
        if claim.method == "grok"
    ]
    exact = any(nonce in quote and quote in text for quote in grok_quotes)
    report = {
        "inference": outcome.label,
        "offline_model": False,
        "method": outcome.method,
        "provider_error": outcome.provider_error,
        "categories": [draft.category for draft in outcome.sections],
        "nonce_quote_exact": exact,
        "grok_quote_count": len(grok_quotes),
        "warnings": outcome.warnings,
    }
    Path(args.out).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if outcome.provider_error or not exact:
        sys.exit(1)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Local knowledge-layer notebook")
    sub = parser.add_subparsers(dest="command", required=True)

    serve_parser = sub.add_parser("serve")
    serve_parser.add_argument("--db", default="data/notebook.sqlite")
    serve_parser.add_argument("--port", type=int, default=8765)
    serve_parser.add_argument("--seed", default="")
    serve_parser.add_argument("--provider", default="auto", choices=("auto", "grok", "rules"))
    serve_parser.set_defaults(func=_serve)

    smoke_parser = sub.add_parser("smoke")
    smoke_parser.add_argument("--nonce", required=True)
    smoke_parser.add_argument("--timeout", type=int, default=75)
    smoke_parser.add_argument("--out", default="provider-smoke.json")
    smoke_parser.set_defaults(func=_smoke)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
