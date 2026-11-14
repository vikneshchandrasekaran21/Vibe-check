#!/usr/bin/env python3
"""vibe-check share_stats: an OPT-IN, anonymous summary of one audit's counts.

Helps the vibe-check project learn which problems are most common (for example "IDOR in 30% of apps"),
without collecting anything about the user or their app.

What is shared: the vibe-check version, the level, the month, the stack's ecosystems and framework names,
which modules ran, pass/fail/N/A/can't-tell counts, failed check IDs by severity, hunt counts,
sweep-hit and version-verdict counts. NOT shared: code, file paths, URLs, app or repo names, emails,
secrets, evidence text, or anything else from the ledger rows.

Usage:
  python3 share_stats.py [LEDGER]                  preview only: prints exactly what would be sent (default)
  python3 share_stats.py [LEDGER] --send --yes     sends it, only after the user said yes in this conversation
Never run --send in unattended or scheduled runs, and never without asking. If the user declines,
add `share_stats: false` to .vibe-check/config and don't ask again.
Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# The endpoint is set by the vibe-check maintainers. Empty = sharing isn't set up yet, and nothing is sent.
STATS_URL = ""
TIMEOUT = 5
SKILL = Path(__file__).resolve().parent.parent
ALLOWED_KEYS = {"schema", "vibe_check_version", "level", "month", "ecosystems", "frameworks", "modules_run",
                "counts", "failed_checks", "hunt", "sweep_hits", "versions"}


def summary(ledger: Path) -> dict:
    text = ledger.read_text("utf-8")
    for part in sorted((ledger.parent / "ledger.d").glob("*.md")):
        text += "\n" + part.read_text("utf-8")
    skill = (SKILL / "SKILL.md").read_text("utf-8")
    version = (re.search(r'^\s*version:\s*"?([\d.]+)', skill, re.M) or [None, "unknown"])[1]
    sev = {}
    for f in (SKILL / "references").glob("*.md"):
        for s, cid in re.findall(r"^- \[ \] (🔴|🟡|🟢) ([A-Z]+-\d{3}) ", f.read_text("utf-8"), re.M):
            sev[cid] = s
    for cid, s in re.findall(r"^\| (BS-\d{2}) \| (🔴|🟡|🟢)", skill, re.M):
        sev[cid] = s
    level = (re.search(r"^\s*Level:\s*\**\s*(quick|full|launch|enterprise)", text, re.I | re.M) or [None, "full"])[1].lower()
    counts = {"pass": 0, "fail": 0, "n/a": 0, "cant_tell": 0}
    failed = {"red": [], "yellow": [], "green": []}
    modules = set()
    hunt = {"hypotheses": 0, "proven": 0, "proven_new": 0}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        key = cells[0].strip("`")
        if re.match(r"^T-\d+$", key) and len(cells) >= 4:
            hunt["hypotheses"] += 1
            if cells[3].upper().startswith("PROVEN"):
                hunt["proven"] += 1
                hunt["proven_new"] += cells[3].upper().startswith("PROVEN NEW")
            continue
        m = re.match(r"^((?:BS|[A-Z]+))-(\d{2,3})$", key)
        if not m or key not in sev:
            continue
        modules.add(m.group(1))
        res = cells[1].upper().replace("’", "'")
        if res.startswith("PASS"):
            counts["pass"] += 1
        elif res.startswith("FAIL"):
            counts["fail"] += 1
            failed[{"🔴": "red", "🟡": "yellow", "🟢": "green"}[sev[key]]].append(key)
        elif res.startswith("N/A"):
            counts["n/a"] += 1
        elif res.startswith("CAN"):
            counts["cant_tell"] += 1
    out = {"schema": 1, "vibe_check_version": version, "level": level,
           "month": datetime.now(timezone.utc).strftime("%Y-%m"), "ecosystems": [], "frameworks": [],
           "modules_run": sorted(modules), "counts": counts, "failed_checks": {k: sorted(v) for k, v in failed.items()},
           "hunt": hunt, "sweep_hits": None, "versions": None}
    vj = ledger.parent / "versions.json"
    if vj.exists():
        data = json.loads(vj.read_text("utf-8"))
        out["ecosystems"] = sorted(data.get("ecosystems", {}))
        # framework and runtime NAMES only (public product names), never versions or paths
        out["frameworks"] = sorted({c["name"] for c in data.get("components", []) if c.get("kind") in ("framework", "cms", "runtime")
                                    and re.fullmatch(r"[\w@./ -]{1,40}", c["name"]) and not c["name"].startswith("WordPress plugin")})
    sj = ledger.parent / "sweep.json"
    if sj.exists():
        out["sweep_hits"] = len(json.loads(sj.read_text("utf-8")).get("hits", []))
    vcount = {"current": 0, "outdated": 0, "eol": 0, "vulnerable": 0}
    for m in re.finditer(r"^\|\s*V-(\d+)(?:\s*\.\.\s*V-(\d+))?\s*\|\s*(CURRENT|OUTDATED|EOL|VULNERABLE)", text, re.M):
        n = int(m.group(2) or m.group(1)) - int(m.group(1)) + 1
        vcount[m.group(3).lower()] += n
    out["versions"] = vcount
    assert set(out) <= ALLOWED_KEYS
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ledger = Path(args[0] if args else ".vibe-check/ledger.md")
    if not ledger.exists():
        print(f"No ledger at {ledger}.")
        return 1
    data = summary(ledger)
    body = json.dumps(data, indent=1, ensure_ascii=False)
    if "--send" not in sys.argv:
        print("This is everything that would be shared (anonymous counts only; no code, paths, names or URLs):\n")
        print(body)
        print("\nIt is sent only if the user says yes: share_stats.py --send --yes")
        return 0
    if "--yes" not in sys.argv:
        print("Not sent: --send needs --yes, given only after the user agreed in this conversation.")
        return 1
    cfg = ledger.parent / "config"
    if cfg.exists() and re.search(r"^\s*share_stats\s*:\s*false\b", cfg.read_text("utf-8"), re.M | re.I):
        print("Not sent: the user turned sharing off (.vibe-check/config).")
        return 0
    if not STATS_URL:
        print("Not sent: sharing isn't set up in this version of vibe-check yet. Nothing left this computer.")
        return 0
    req = urllib.request.Request(STATS_URL, data=body.encode(), headers={"content-type": "application/json",
                                                                       "User-Agent": "vibe-check-share-stats"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:  # noqa: S310 (fixed https URL)
            print(f"Shared, thank you ({r.status}).")
    except Exception as e:  # never break the audit over this
        print(f"Couldn't share ({type(e).__name__}); nothing else was affected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
