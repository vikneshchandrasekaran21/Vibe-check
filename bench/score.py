#!/usr/bin/env python3
"""Score a vibe-check hunt against the benchmark's answer key.

Usage:  python3 bench/score.py <path to the audited copy's .vibe-check/ledger.md> [bench/hunt-answers.json]

A bug counts as found when a PROVEN hunt row (T-) or a FAIL row mentions the bug's file
and at least one of its keywords. Prints recall (found / total) and what was missed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def rows(text: str):
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        key = cells[0].strip("`")
        if re.match(r"^T-\d+$", key) and len(cells) >= 5 and cells[3].upper().startswith("PROVEN"):
            yield key, " ".join(cells[1:]).lower()
        elif re.match(r"^[A-Z0-9]+-\d{2,3}$", key) and cells[1].upper().startswith("FAIL"):
            yield key, " ".join(cells[1:]).lower()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    ledger = Path(sys.argv[1]).read_text("utf-8")
    key = Path(sys.argv[2] if len(sys.argv) > 2 else Path(__file__).with_name("hunt-answers.json"))
    bugs = json.loads(key.read_text("utf-8"))["bugs"]
    found, missed = [], []
    evidence = list(rows(ledger))
    for b in bugs:
        base = b["file"].lower()
        stem = Path(base).name
        hit = next((k for k, txt in evidence if (base in txt or stem in txt) and any(w.lower() in txt for w in b["keywords"])), None)
        (found if hit else missed).append((b, hit))
    print(f"Hunt benchmark: found {len(found)} of {len(bugs)} planted bugs ({100 * len(found) // len(bugs)}%)")
    for b, hit in found:
        print(f"  ✅ {b['id']} {b['title']}  (ledger {hit})")
    for b, _ in missed:
        print(f"  ❌ {b['id']} {b['title']}  [{b['method']}, {b['file']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
