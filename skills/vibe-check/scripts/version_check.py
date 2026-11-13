#!/usr/bin/env python3
"""vibe-check version check: is a newer vibe-check released?

The only network request vibe-check itself makes. It reads one public GitHub page (the latest
release of the vibe-check repo) and compares that version with the installed SKILL.md.
It sends nothing about the user: no code, no report, no project name, no ID. Just the request.
It gives up after 3 seconds, never blocks the audit, and stays silent if it can't connect.

Turn it off with the environment variable VIBE_CHECK_NO_UPDATE_CHECK=1 (DO_NOT_TRACK=1 also works),
or with a line `update_check: false` in .vibe-check/config in the project.

Usage:  python3 version_check.py [--latest X.Y.Z]     (--latest skips the network, for tests)
Prints one line and always exits 0:
  UP TO DATE: vibe-check v2.7.1
  UPDATE AVAILABLE: vibe-check v2.8.0 (installed v2.7.1). Update: npx skills update, then start a new session.
  SKIPPED: <reason>
Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

LATEST_RELEASE_URL = "https://api.github.com/repos/vikneshchandrasekaran21/Vibe-check/releases/latest"
FALLBACK_URL = "https://raw.githubusercontent.com/vikneshchandrasekaran21/Vibe-check/main/skills/vibe-check/SKILL.md"
TIMEOUT = 3
UPDATE_HOW = "Update: npx skills update (Claude app: download the new zip from the GitHub release), then start a new session."


def parse(v: str):
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", v or "")
    return tuple(int(x) for x in m.groups()) if m else None


def installed() -> str:
    text = (Path(__file__).resolve().parent.parent / "SKILL.md").read_text("utf-8")
    m = re.search(r'^\s*version:\s*"?(\d+\.\d+\.\d+)', text, re.M)
    return m.group(1) if m else ""


def disabled() -> str:
    for var in ("VIBE_CHECK_NO_UPDATE_CHECK", "DO_NOT_TRACK"):
        if os.environ.get(var, "").strip().lower() in ("1", "true", "yes"):
            return f"turned off ({var})"
    cfg = Path(".vibe-check") / "config"
    try:
        if cfg.exists() and re.search(r"^\s*update_check\s*:\s*false\b", cfg.read_text("utf-8"), re.M | re.I):
            return "turned off (.vibe-check/config)"
    except OSError:
        pass
    return ""


def get(url: str) -> str:
    # A plain GET with no cookies, no body and no identifying headers beyond a generic User-Agent.
    req = urllib.request.Request(url, headers={"User-Agent": "vibe-check-version-check",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:  # noqa: S310 (fixed https URLs only)
        return r.read(200_000).decode("utf-8", "replace")


def latest() -> str:
    try:
        tag = json.loads(get(LATEST_RELEASE_URL)).get("tag_name", "")
        if parse(tag):
            return tag.lstrip("v")
    except Exception:  # offline, blocked, rate-limited: try the fallback, then give up quietly
        pass
    m = re.search(r'^\s*version:\s*"?(\d+\.\d+\.\d+)', get(FALLBACK_URL), re.M)
    return m.group(1) if m else ""


def main() -> int:
    mine = installed()
    if not parse(mine):
        print("SKIPPED: installed version unknown")
        return 0
    if "--latest" in sys.argv:
        newest = sys.argv[sys.argv.index("--latest") + 1].lstrip("v")
    else:
        why = disabled()
        if why:
            print(f"SKIPPED: {why}. Installed: vibe-check v{mine}")
            return 0
        try:
            newest = latest()
        except Exception:
            print(f"SKIPPED: couldn't reach GitHub (offline or blocked). Installed: vibe-check v{mine}")
            return 0
    if not parse(newest):
        print(f"SKIPPED: latest version unknown. Installed: vibe-check v{mine}")
    elif parse(newest) > parse(mine):
        print(f"UPDATE AVAILABLE: vibe-check v{newest} (installed v{mine}). {UPDATE_HOW}")
    else:
        print(f"UP TO DATE: vibe-check v{mine}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
