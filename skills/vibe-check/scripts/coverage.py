#!/usr/bin/env python3
"""vibe-check coverage: prove every check was done, by counting.

Compares the ledger (.vibe-check/ledger.md) with the skill's checklist and fails if any
required check ID has no result, if an ID was invented, if a result lacks evidence, if a
FAIL has no confidence label, if a sweep hit has no verdict, or if an inventory category
was never accounted for. It also prints the coverage table and score line for the report,
so the numbers in the report come from a count, not from memory.

Ledger rows (markdown table, one per check):
  | SEC-001 | PASS | src/lib/auth.ts:12 uses Supabase Auth |
  | SEC-030 | FAIL ✅ Confirmed | app/notes/[id]/page.tsx:41 dangerouslySetInnerHTML on user text |
  | SEC-047 | CAN'T TELL | token generation lives in an external service; asked the user |
  | HLT-* | N/A | no health data (whole profile module) |
  | PLT-011..PLT-015 | N/A | not on Firebase |
  | INV-api_routes | 47/47 | every route traced to its auth check |
  | H-001..H-004 | RULED OUT | Supabase anon key: public by design, RLS on |
  | H-005 | FINDING SEC-022 | live Stripe key in src/lib/stripe.ts |
  | V-003 | OUTDATED | PHP 8.3.35 < 8.3.36 security release: https://www.php.net/releases/ (opened 2026-11-14) |
  | V-010..V-014 | CURRENT | npm audit --omit=dev: 0 vulnerabilities |
Results: PASS, FAIL (+ ✅ Confirmed or 🔎 Likely), N/A, CAN'T TELL. Ranges and * are allowed for N/A only.
Core modules can't be N/A as a whole.

Usage:
  python3 coverage.py [LEDGER] [--level quick|full|enterprise] [--remaining]
    LEDGER       default .vibe-check/ledger.md (inventory.json and sweep.json are read from the same folder)
    --remaining  list what is left to check (use it to resume a long run)
Exit code 0 = complete, 1 = gaps found. Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CORE = ["security", "reliability", "devops", "functional-qa", "legal-privacy", "launch-ux", "platforms",
        "lawsuits", "supply-chain", "vulnerabilities", "hunt", "maintainability"]
LAZY = {"ok", "fine", "looks fine", "looks good", "good", "yes", "pass", "passed", "n/a", "na", "none", "-", "checked",
        "done", "no issues", "nothing found", "all good", "seems fine", "looks ok", "verified", "correct"}
CT = "CAN'T TELL"
HUNT_METHODS = {"THREAT", "INVARIANT", "ABUSE", "PATH", "ASSUMPTION", "VARIANT", "CHAIN"}
SOURCE = re.compile(r"https?://|\b(?:npm audit|pnpm audit|yarn npm audit|composer audit|pip-audit|bundle audit|govulncheck|"
                    r"cargo audit|osv-scanner|trivy|docker scout|dependency-check|dotnet list package|wpscan|wp plugin list)\b", re.I)
CHECKABLE = re.compile(r"\w\.\w|/|`|:\d|https?:|\b(?:dashboard|config|setting|header|inventory|sweep|"
                       r"user confirmed|command|grep|npm|pnpm|yarn|pip|curl|git|gh|lighthouse|axe|playwright|policy|"
                       r"migration|env|DNS|SPF|DKIM|DMARC|CLI)\b", re.I)
ID_RX = re.compile(r"^([A-Z0-9]+)-(\d{2,3})$")


def load_checklist():
    """Return (ordered modules, {id: (module, severity, name)}, {prefix: module})."""
    checks, prefixes, modules = {}, {}, ["blind-spots"]
    skill = (SKILL / "SKILL.md").read_text("utf-8")
    for num, sev, name in re.findall(r"^\| (BS-\d{2}) \| (🔴|🟡|🟢) \*\*(.+?)\*\*", skill, re.M):
        checks[num] = ("blind-spots", sev, name)
    prefixes["BS"] = "blind-spots"
    for f in sorted((SKILL / "references").glob("*.md")):
        text = f.read_text("utf-8")
        items = re.findall(r"^- \[ \] (🔴|🟡|🟢) ([A-Z0-9]+-\d{3}) (.*)$", text, re.M)
        if not items:
            continue
        modules.append(f.stem)
        for sev, cid, rest in items:
            nm = re.match(r"\*\*(.+?)\*\*", rest)
            checks[cid] = (f.stem, sev, (nm.group(1) if nm else rest[:70]).rstrip(".:,"))
            prefixes[cid.split("-")[0]] = f.stem
    order = ["blind-spots"] + [m for m in CORE if m in modules] + [m for m in modules if m not in CORE and m != "blind-spots"]
    return order, checks, prefixes


def load_standards():
    """Return [(standard title, [(item id, name, [check ids], human note)])] from references/standards.md."""
    path = SKILL / "references" / "standards.md"
    if not path.exists():
        return []
    out, cur = [], None
    for line in path.read_text("utf-8").splitlines():
        if line.startswith("## "):
            cur = (line[3:].strip(), [])
            out.append(cur)
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if cur and len(cells) == 3 and cells[0] not in ("ID",) and not set(cells[0]) <= set("-: "):
            ids = re.findall(r"\b(?:BS-\d{2}|[A-Z]+-\d{3})\b", cells[2])
            human = "Human:" in cells[2]
            cur[1].append((cells[0], cells[1], ids, human))
    return [s for s in out if s[1]]


def expand(token: str, checks, prefixes):
    """Expand 'SEC-001', 'SEC-001..SEC-010' or 'HLT-*' into IDs. Returns (ids, kind, error)."""
    token = token.strip().strip("`")
    if token.endswith("-*"):
        pre = token[:-2]
        if pre not in prefixes:
            return [], "wild", f"unknown module prefix '{pre}'"
        return [c for c in checks if c.split("-")[0] == pre], "wild", None
    if ".." in token:
        a, b = [x.strip() for x in token.split("..", 1)]
        ma, mb = ID_RX.match(a), ID_RX.match(b)
        if not (ma and mb) or ma.group(1) != mb.group(1):
            return [], "range", f"bad range '{token}'"
        lo, hi, width = int(ma.group(2)), int(mb.group(2)), len(ma.group(2))
        ids = [f"{ma.group(1)}-{n:0{width}d}" for n in range(lo, hi + 1)]
        unknown = [i for i in ids if i not in checks]
        return [i for i in ids if i in checks], "range", (f"range '{token}' includes unknown IDs {unknown[:3]}" if unknown else None)
    return [token], "one", (None if token in checks else f"unknown check ID '{token}' (not in the checklist: invented?)")


def norm_result(r: str):
    u = r.upper().replace("’", "'")
    if u.startswith("PASS"):
        return "PASS"
    if u.startswith("FAIL"):
        return "FAIL"
    if u.startswith("N/A") or u.startswith("NA ") or u == "NA" or u.startswith("NOT APPLICABLE"):
        return "N/A"
    if u.startswith("CAN'T TELL") or u.startswith("CANT TELL") or u.startswith("CANNOT TELL"):
        return "CAN'T TELL"
    return None


def main() -> int:
    argv = sys.argv[1:]
    level = None
    if "--level" in argv:
        i = argv.index("--level"); level = argv[i + 1].lower(); del argv[i:i + 2]
    remaining_only = "--remaining" in argv
    args = [a for a in argv if not a.startswith("--")]
    ledger_path = Path(args[0] if args else ".vibe-check/ledger.md")
    if not ledger_path.exists():
        print(f"No ledger at {ledger_path}. Create it first (see SKILL.md Step 4).")
        return 1
    text = ledger_path.read_text("utf-8")
    if level is None:
        m = re.search(r"^\s*Level:\s*\**\s*(quick|full|launch|enterprise)", text, re.I | re.M)
        level = (m.group(1).lower() if m else "full")
    level = "full" if level == "launch" else level

    order, checks, prefixes = load_checklist()
    errors, warns = [], []
    results = {}   # id -> (result, evidence, confidence)
    inv_rows, hit_rows, ver_rows = {}, {}, {}
    hunt_rows = []
    pass_evidence = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.strip().startswith("|") else []
        if len(cells) < 3 or set(cells[0]) <= set("-: ") or cells[0].lower() in ("id", "check", "hit"):
            continue
        key, res, ev = cells[0].strip("`"), cells[1], " | ".join(cells[2:]).strip()
        if re.match(r"^T-\d+$", key):
            hunt_rows.append((key, cells))
            continue
        if key.startswith("INV-"):
            inv_rows[key[4:]] = (res, ev)
            continue
        if key.startswith("V-"):
            m = re.match(r"^V-(\d+)(?:\s*\.\.\s*V-(\d+))?$", key)
            if not m:
                errors.append(f"{key}: components are written V-001 or V-001..V-009")
                continue
            for n in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                ver_rows[f"V-{n:03d}"] = (res, ev)
            continue
        if key.startswith("H-"):
            m = re.match(r"^H-(\d+)(?:\s*\.\.\s*H-(\d+))?$", key)
            if not m:
                errors.append(f"{key}: sweep hits are written H-001 or H-001..H-009")
                continue
            for n in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                hit_rows[f"H-{n:03d}"] = (res, ev)
            continue
        if not re.match(r"^[A-Z0-9]+-(\d|\*)", key):
            continue
        r = norm_result(res)
        if r is None:
            errors.append(f"{key}: result must be PASS, FAIL, N/A or CAN'T TELL (got '{res}')")
            continue
        ids, kind, e = expand(key, checks, prefixes)
        if e:
            errors.append(e)
        if kind != "one" and r != "N/A":
            errors.append(f"{key}: ranges and * are only allowed for N/A (each {r} needs its own row and evidence)")
            continue
        if kind == "wild" and ids and checks[ids[0]][0] in CORE:
            errors.append(f"{key}: core module '{checks[ids[0]][0]}' can't be N/A as a whole; mark sections or items")
        if not ev or ev.lower().strip(" .") in LAZY or len(ev) < 8:
            errors.append(f"{key}: {r} needs real evidence or a reason (got '{ev or 'nothing'}')")
        if r in ("PASS", "FAIL") and not CHECKABLE.search(ev):
            errors.append(f"{key}: {r} evidence must point to something checkable (file:line, command, URL, "
                          f"config value, dashboard setting or inventory/sweep item), got '{ev[:60]}'")
        if r == "PASS":
            pass_evidence.setdefault(ev.lower(), []).append(key)
        conf = ""
        if r == "FAIL":
            if "confirmed" in res.lower() or "✅" in res:
                conf = "Confirmed"
            elif "likely" in res.lower() or "🔎" in res:
                conf = "Likely"
            else:
                errors.append(f"{key}: FAIL needs a confidence label (✅ Confirmed or 🔎 Likely); unsure items are CAN'T TELL")
        for cid in ids:
            if cid in results and results[cid][0] != r:
                errors.append(f"{cid}: two different results ({results[cid][0]} and {r})")
            results[cid] = (r, ev, conf)

    for ev, keys in pass_evidence.items():
        if len(keys) > 3:
            errors.append(f"same PASS evidence copied onto {len(keys)} rows ({', '.join(keys[:4])} …): "
                          "each check needs its own evidence, or it wasn't really checked")

    # required set
    if level == "quick":
        required = [c for c, (m, s, _) in checks.items() if m == "blind-spots" or (m in CORE and s == "🔴")]
    else:
        required = list(checks)
        if level == "enterprise":
            for mod in ("enterprise", "policies"):
                if all(results.get(c, ("",))[0] == "N/A" for c, v in checks.items() if v[0] == mod):
                    errors.append(f"Enterprise level: module '{mod}' can't be N/A as a whole")
    missing = [c for c in required if c not in results]

    # inventory accounting
    inv_path = ledger_path.parent / "inventory.json"
    inv_lines = []
    if inv_path.exists():
        counts = json.loads(inv_path.read_text("utf-8")).get("counts", {})
        for cat, n in counts.items():
            if not n:
                continue
            row = inv_rows.get(cat)
            if not row:
                errors.append(f"INV-{cat}: inventory found {n}, but the ledger has no INV-{cat} row (checked/found)")
                continue
            m = re.match(r"\s*(\d+)\s*/\s*(\d+)", row[0])
            if not m:
                errors.append(f"INV-{cat}: result must be checked/found, e.g. {n}/{n}")
                continue
            done, total = int(m.group(1)), int(m.group(2))
            if total < n:
                errors.append(f"INV-{cat}: says {total} found, but the inventory script found {n}")
            if done < total:
                warns.append(f"INV-{cat}: only {done}/{total} checked ({row[1] or 'no reason given'}): report as partial")
            inv_lines.append((cat, done, max(total, n)))
    else:
        warns.append("no inventory.json next to the ledger: run inventory.py first (or say why in the report)")

    # sweep hits
    sweep_path = ledger_path.parent / "sweep.json"
    sweep_total = sweep_unreviewed = 0
    if sweep_path.exists():
        hits = json.loads(sweep_path.read_text("utf-8")).get("hits", [])
        sweep_total = len(hits)
        for h in hits:
            row = hit_rows.get(h["id"])
            if not row:
                sweep_unreviewed += 1
            else:
                v = row[0].upper()
                if not (v.startswith("FINDING") or v.startswith("RULED OUT")):
                    errors.append(f"{h['id']}: verdict must be FINDING <check ID> or RULED OUT")
                elif v.startswith("FINDING") and not re.search(r"[A-Z0-9]+-\d{2,3}", row[0] + " " + row[1]):
                    errors.append(f"{h['id']}: FINDING must name the check ID it belongs to")
                elif not row[1] or len(row[1]) < 8:
                    errors.append(f"{h['id']}: verdict needs a reason")
        if sweep_unreviewed:
            errors.append(f"sweep: {sweep_unreviewed} of {sweep_total} hits have no verdict (FINDING or RULED OUT)")
    else:
        warns.append("no sweep.json next to the ledger: run sweep.py first (or say why in the report)")

    # hunt: hypotheses tested by attacking the app's own logic (references/hunt.md)
    hunt_stats = None
    if level in ("full", "enterprise"):
        need_n, need_m = (12, 4) if level == "full" else (25, 6)
        methods, proven, proven_new, disproven, untested = set(), 0, 0, 0, 0
        for key, cells in hunt_rows:
            if len(cells) < 5:
                errors.append(f"{key}: hunt rows are | ID | Hypothesis | Method | Result | Evidence |")
                continue
            hyp, meth, resu, evid = cells[1], cells[2].upper().strip("` "), cells[3].upper().strip("` "), " | ".join(cells[4:]).strip()
            if meth not in HUNT_METHODS:
                errors.append(f"{key}: method must be one of {', '.join(sorted(HUNT_METHODS))} (got '{cells[2]}')")
            methods.add(meth)
            if len(hyp) < 10:
                errors.append(f"{key}: write the hypothesis as a full sentence")
            if resu.startswith("PROVEN"):
                proven += 1
                ref = resu[len("PROVEN"):].strip()
                if ref == "NEW":
                    proven_new += 1
                elif not (ref in checks):
                    errors.append(f"{key}: PROVEN must be followed by NEW or an existing check ID (got '{cells[3]}')")
                if not CHECKABLE.search(evid):
                    errors.append(f"{key}: PROVEN needs a proof: a test or script in .vibe-check/proofs/, or the quoted code path")
            elif resu.startswith("DISPROVEN"):
                disproven += 1
                if not CHECKABLE.search(evid):
                    errors.append(f"{key}: DISPROVEN needs what stopped it (file:line, constraint, test)")
            elif resu.startswith("UNTESTED"):
                untested += 1
                if len(evid) < 8:
                    errors.append(f"{key}: UNTESTED needs why, and what would test it")
            else:
                errors.append(f"{key}: result must be PROVEN NEW, PROVEN <check ID>, DISPROVEN or UNTESTED")
        n_fail = sum(1 for v in results.values() if v[0] == "FAIL")
        if len(hunt_rows) < need_n:
            errors.append(f"hunt: {len(hunt_rows)} hypotheses; a {level} check needs at least {need_n} (references/hunt.md)")
        if len(methods & HUNT_METHODS) < need_m:
            errors.append(f"hunt: {len(methods & HUNT_METHODS)} methods used; a {level} check needs at least {need_m}")
        for must in ("INVARIANT", "ABUSE"):
            if hunt_rows and must not in methods:
                errors.append(f"hunt: no {must} hypotheses (required)")
        if n_fail and "VARIANT" not in methods:
            errors.append("hunt: there are confirmed FAILs but no VARIANT hypotheses (search for siblings of each finding)")
        if n_fail >= 2 and "CHAIN" not in methods:
            errors.append("hunt: two or more FAILs but no CHAIN hypotheses (can they combine?)")
        tm = re.search(r"^##\s*Threat model\s*\n((?:\s*[-*].*\n?)+)", text, re.M)
        if not tm or len([l for l in tm.group(1).splitlines() if l.strip()]) < 3:
            errors.append("hunt: the ledger needs a '## Threat model' section with assets, actors, boundaries and entry points")
        hunt_stats = (len(hunt_rows), proven, proven_new, disproven, untested, len(methods & HUNT_METHODS))

    # component versions: each needs a verdict backed by a source opened in this run, or an audit tool
    ver_path = ledger_path.parent / "versions.json"
    ver_total = ver_open = 0
    ver_bad = []
    if ver_path.exists():
        comps = json.loads(ver_path.read_text("utf-8")).get("components", [])
        ver_total = len(comps)
        for c in comps:
            row = ver_rows.get(c["id"])
            if not row:
                ver_open += 1
                continue
            v = row[0].upper().replace("’", "'")
            status = next((s for s in ("CURRENT", "OUTDATED", "EOL", "VULNERABLE", "CAN'T TELL") if v.startswith(s)), None)
            if not status:
                errors.append(f"{c['id']}: verdict must be CURRENT, OUTDATED, EOL, VULNERABLE or CAN'T TELL")
            elif status != "CAN'T TELL" and not SOURCE.search(row[1]):
                errors.append(f"{c['id']} ({c['name']} {c['version']}): {status} needs the source URL opened in this run "
                              "or the audit tool that checked it (no versions from memory)")
            elif len(row[1]) < 8:
                errors.append(f"{c['id']}: verdict needs a reason")
            elif status in ("OUTDATED", "EOL", "VULNERABLE"):
                ver_bad.append(f"{c['id']} {c['name']} {c['version']}: {status}")
        if ver_open:
            errors.append(f"versions: {ver_open} of {ver_total} components have no verdict (V- rows)")
    elif level != "quick":
        warns.append("no versions.json next to the ledger: run versions.py first (or say why in the report)")

    if remaining_only:
        by_mod = {}
        for c in missing:
            by_mod.setdefault(checks[c][0], []).append(c)
        print(f"Level: {level} · remaining: {len(missing)} of {len(required)} required checks")
        for mod in order:
            if mod in by_mod:
                ids = by_mod[mod]
                print(f"  {mod:<20} {len(ids):>3} left: {', '.join(ids[:12])}{' …' if len(ids) > 12 else ''}")
        if sweep_unreviewed:
            print(f"  sweep hits without a verdict: {sweep_unreviewed}")
        if ver_open:
            print(f"  components without a version verdict: {ver_open}")
        return 0 if not missing else 1

    # coverage table
    rows = []
    tot = {"PASS": 0, "FAIL": 0, "N/A": 0, "CAN'T TELL": 0}
    blockers = unresolved = 0
    for mod in order:
        ids = [c for c in required if checks[c][0] == mod]
        if not ids:
            continue
        cnt = {"PASS": 0, "FAIL": 0, "N/A": 0, "CAN'T TELL": 0}
        for c in ids:
            if c in results:
                cnt[results[c][0]] += 1
                if results[c][0] == "FAIL" and checks[c][1] == "🔴":
                    blockers += 1
                if results[c][0] == "CAN'T TELL" and checks[c][1] == "🔴":
                    unresolved += 1
        miss = len(ids) - sum(cnt.values())
        for k in tot:
            tot[k] += cnt[k]
        status = "➖" if cnt["N/A"] == len(ids) else ("❌" if miss == len(ids) else ("◐" if miss or cnt["CAN'T TELL"] else "✅"))
        rows.append((mod, status, len(ids), cnt, miss))
    applicable = tot["PASS"] + tot["FAIL"] + tot["CAN'T TELL"] + len(missing)

    print(f"## Coverage (counted by coverage.py · level: {level})\n")
    print("| Module | Status | Checks | ✅ Pass | ❌ Fail | ➖ N/A | ❓ Can't tell | Not done |")
    print("|---|---|---|---|---|---|---|---|")
    for mod, status, n, cnt, miss in rows:
        print("| %s | %s | %d | %d | %d | %d | %d | %d |" % (mod, status, n, cnt["PASS"], cnt["FAIL"], cnt["N/A"], cnt[CT], miss))
    print("| **Total** | | **%d** | **%d** | **%d** | **%d** | **%d** | **%d** |" % (len(required), tot["PASS"], tot["FAIL"], tot["N/A"], tot[CT], len(missing)))
    if inv_lines:
        print("\n| Inventory | Checked |\n|---|---|")
        for cat, done, total in inv_lines:
            print(f"| {cat} | {done}/{total}{'' if done >= total else ' ◐'} |")
    if sweep_path.exists():
        print(f"\nSweep: {sweep_total} hits, {sweep_total - sweep_unreviewed} reviewed.")
    if hunt_stats:
        n, pr, new, dis, unt, nm = hunt_stats
        print(f"\nHunt: {n} hypotheses ({nm} methods): {pr} proven ({new} new, not in any checklist), {dis} disproven, {unt} untested.")
    if ver_path.exists():
        print(f"\nVersions: {ver_total} components, {ver_total - ver_open} checked, {len(ver_bad)} outdated / end-of-life / vulnerable.")
        for b in ver_bad:
            print(f"  - {b}")
    stds = load_standards()
    if stds and not remaining_only:
        print("\n## Standards (how this audit's checks came out for each item; not a certification)\n")
        print("| Standard | ✅ | ❌ | ◐ | ➖ | Items that failed |")
        print("|---|---|---|---|---|---|")
        for title, items in stds:
            tally = {"ok": 0, "fail": 0, "part": 0, "na": 0}
            failed = []
            for iid, name, ids, human in items:
                rs = [results[c][0] for c in ids if c in results]
                if any(r == "FAIL" for r in rs):
                    tally["fail"] += 1; failed.append(iid)
                elif rs and all(r == "N/A" for r in rs) and len(rs) == len(ids):
                    tally["na"] += 1
                elif rs and len(rs) == len(ids) and all(r in ("PASS", "N/A") for r in rs) and not human:
                    tally["ok"] += 1
                else:
                    tally["part"] += 1
            print(f"| {title} | {tally['ok']} | {tally['fail']} | {tally['part']} | {tally['na']} | {', '.join(failed) or '-'} |")
        print("\n◐ = some mapped checks couldn't be confirmed, weren't done, or need a human specialist (see references/standards.md).")
    print(f"\nScore line: {tot['PASS']}/{applicable} checks passed · {blockers} blockers · {unresolved} unresolved 🔴 can't-tell")

    for w in warns:
        print("warning:", w)
    if missing:
        errors.insert(0, f"{len(missing)} required checks have no result: {', '.join(missing[:15])}{' …' if len(missing) > 15 else ''}"
                         " (run with --remaining)")
    for e in errors:
        print("GAP:", e)
    print("\nCOMPLETE: every required check has a result." if not errors else f"\nINCOMPLETE: {len(errors)} gap(s). Fix them before writing the report.")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
