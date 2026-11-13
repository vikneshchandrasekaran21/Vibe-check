#!/usr/bin/env python3
"""Test bench for the skill's scripts: a small app with bugs planted on purpose.

Builds the app in a temp folder (fake secrets are assembled at runtime so no secret-looking
string is ever committed), runs inventory.py, sweep.py and coverage.py, and checks that every
planted problem is caught and that coverage.py rejects incomplete or sloppy ledgers.
Usage: python3 tests/test_scripts.py   (exit code 1 on any failure)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "skills" / "vibe-check" / "scripts"
failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def run(script: str, *args: str, cwd: Path | None = None, env: dict | None = None):
    return subprocess.run([sys.executable, "-I", str(SCRIPTS / script), *args], capture_output=True, text=True,
                          cwd=cwd, env=env, timeout=60)


# fake credentials, assembled so this file never contains them literally
AWS = "AKIA" + "QX7Z" * 4
STRIPE = "sk_" + "live_" + "4eC39HqLyjWDarjtT1zdp7dc"
FILES = {
    "app/page.tsx": 'export default function Home() { return <a href="/notes">Notes</a> }\n',
    "app/notes/[id]/page.tsx": "export default function Note({ note }) {\n  return <div dangerouslySetInnerHTML={{ __html: note.body }} />\n}\n",
    "app/api/notes/route.ts": (
        "import Stripe from 'stripe'\n"
        f"const stripe = new Stripe('{STRIPE}')\n"
        "export async function GET(req) {\n"
        "  const id = new URL(req.url).searchParams.get('id')\n"
        "  const rows = await db.query(`SELECT * FROM notes WHERE id = ${id}`)\n"
        "  try { await audit(id) } catch (e) {}\n"
        "  return Response.json(rows)\n}\n"
    ),
    "app/api/stripe/webhook/route.ts": (
        "export async function POST(req) {\n  const body = await req.json()\n"
        "  const session = await stripe.checkout.sessions.create({ amount: body })\n  return Response.json(session)\n}\n"
    ),
    "app/actions.ts": "'use server'\nexport async function saveNote(formData) { const token = Math.random().toString(36) }\n",
    "supabase/functions/send-email/index.ts": "import { Resend } from 'resend'\nconst r = new Resend(Deno.env.get('RESEND_API_KEY'))\nawait r.emails.send({})\n",
    "supabase/migrations/001_init.sql": (
        "create table if not exists public.notes (id uuid primary key, body text, user_id uuid);\n"
        "create policy \"read all\" on public.notes for select using (true);\n"
        "insert into storage.buckets (id, name, public) values ('avatars', 'avatars', true);\n"
    ),
    "components/NoteForm.tsx": (
        '<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet" />\n'
        '<script async src="https://www.googletagmanager.com/gtag/js?id=G-TEST"></script>\n'
        "export function NoteForm() {\n  localStorage.setItem('auth_token', t)\n"
        '  return <form onSubmit={save}><input type="file" /><button onClick={go}>Save</button></form>\n}\n'
    ),
    "lib/ai.ts": "import OpenAI from 'openai'\nconst c = await openai.chat.completions.create({ model: 'x', messages })\nconst out = eval(c.choices[0].message.content)\n",
    "server.js": (
        "const app = require('express')()\napp.use(cors({ origin: '*' }))\n"
        "app.get('/api/users/:id', (req, res) => res.json({}))\n"
        "exec(`convert ${req.query.file} out.png`)\nconst agent = new https.Agent({ rejectUnauthorized: false })\n"
        "const api = process.env.API_URL\n"
    ),
    "tests/notes.test.ts": "it.skip('only the owner can read a note', () => {})\n",
    # clean file: must produce no hits
    "lib/clean.ts": "const url = 'http://localhost:3000'\ntry { run() } catch (e) { report(e) }\nexport const ok = true\n",
    ".env": "NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY=placeholder\nRESEND_API_KEY=placeholder\n",
}
EXPECT_PATTERNS = {"SECRET-STRIPE", "SECRET-AWS", "PUBLIC-ENV-SECRET", "XSS-HTML", "SQL-CONCAT", "CMD-EXEC", "TLS-OFF",
                   "CORS-ANY", "RLS-TRUE", "EMPTY-CATCH", "CLIENT-PRICE", "GOOGLE-FONTS", "TRACKERS", "TOKEN-STORAGE",
                   "SKIPPED-TESTS", "ENV-TRACKED", "WEAK-RANDOM", "EVAL"}
EXPECT_INVENTORY = {
    "pages": ["/", "/notes/[id]"], "api_routes": ["/api/notes", "GET /api/users/:id"], "server_actions": ["app/actions.ts"],
    "functions": ["supabase:send-email"], "webhooks": ["app/api/stripe/webhook/route.ts"], "db_tables": ["notes"],
    "storage_buckets": ["avatars"], "file_uploads": [], "payments": [], "email": [], "ai_calls": [], "forms": [],
    "buttons_links": [], "env_vars": ["NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY", "RESEND_API_KEY", "API_URL"],
    "third_party_scripts": ["googletagmanager"],
}


def git(cwd: Path, *a: str) -> None:
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a], cwd=cwd, capture_output=True, check=True)


def build_app(root: Path) -> None:
    for rel, body in FILES.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)
    git(root, "init", "-q")
    (root / "old.ts").write_text(f"const key = '{AWS}'\n")  # secret that only lives in history
    git(root, "add", "-A"); git(root, "commit", "-qm", "init")
    (root / "old.ts").unlink()
    git(root, "add", "-A"); git(root, "commit", "-qm", "remove key")


def all_ids() -> list:
    ids = re.findall(r"^\| (BS-\d{2}) \|", (ROOT / "skills/vibe-check/SKILL.md").read_text(), re.M)
    for f in sorted((ROOT / "skills/vibe-check/references").glob("*.md")):
        ids += re.findall(r"^- \[ \] \S+ ([A-Z0-9]+-\d{3}) ", f.read_text(), re.M)
    return ids


def ledger(out: Path, rows: list, level: str = "Full") -> Path:
    p = out / "ledger.md"
    p.write_text(f"# vibe-check ledger\n\nLevel: {level}\n\n| ID | Result | Evidence / reason |\n|---|---|---|\n" + "\n".join(rows) + "\n")
    return p


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        app = Path(tmp) / "app"; app.mkdir()
        build_app(app)
        out = app / ".vibe-check"

        # inventory
        r = run("inventory.py", str(app))
        check(r.returncode == 0, f"inventory.py failed: {r.stderr}")
        inv = json.loads((out / "inventory.json").read_text())
        for cat, needles in EXPECT_INVENTORY.items():
            items = inv["items"].get(cat, [])
            check(bool(items), f"inventory: category '{cat}' found nothing")
            for n in needles:
                check(any(n == i or i.startswith(n + " ") or n in i for i in items), f"inventory: '{cat}' missed {n} (got {items[:6]})")

        # sweep
        r = run("sweep.py", str(app), "--history")
        check(r.returncode == 0, f"sweep.py failed: {r.stderr}")
        sw = json.loads((out / "sweep.json").read_text())
        found = {h["pattern"] for h in sw["hits"]}
        for p in sorted(EXPECT_PATTERNS - found):
            check(False, f"sweep: planted problem not caught: {p}")
        clean = [h for h in sw["hits"] if h["file"] == "lib/clean.ts"]
        check(not clean, f"sweep: false positives in the clean file: {[h['pattern'] for h in clean]}")
        text = (out / "sweep.md").read_text() + (out / "sweep.json").read_text()
        check(STRIPE not in text and AWS not in text, "sweep: a secret was printed in full (must be masked)")
        check(any(h["pattern"] == "SECRET-AWS" and "@" in h["file"] for h in sw["hits"]), "sweep: --history missed the deleted AWS key")

        # coverage: a complete ledger passes
        ids = all_ids()
        counts = inv["counts"]
        inv_rows = [f"| INV-{k} | {n}/{n} | each one traced and checked |" for k, n in counts.items() if n]
        hit_rows = [f"| H-001..H-{len(sw['hits']):03d} | RULED OUT | test bench: reviewed in the test |"]
        full = [f"| {i} | PASS | src/mod{n}.ts:{n} handles it |" for n, i in enumerate(ids, 1)]
        r = run("coverage.py", str(ledger(out, full + inv_rows + hit_rows)))
        check(r.returncode == 0, f"coverage: complete ledger should pass:\n{r.stdout[-800:]}")
        check(f"{len(ids)}/{len(ids)} checks passed" in r.stdout, "coverage: score line is wrong")

        # coverage: each sloppy ledger must fail
        bad = {
            "missing one check": full[:-1] + inv_rows + hit_rows,
            "invented ID": full + ["| SEC-999 | PASS | src/x.ts:1 handled here |"] + inv_rows + hit_rows,
            "FAIL without confidence": [full[0].replace("PASS", "FAIL")] + full[1:] + inv_rows + hit_rows,
            "lazy evidence": ["| BS-01 | PASS | looks fine |"] + full[1:] + inv_rows + hit_rows,
            "evidence with nothing checkable": ["| BS-01 | PASS | the code handles this correctly |"] + full[1:] + inv_rows + hit_rows,
            "copy-pasted evidence": [f"| {i} | PASS | src/auth.ts:1 handles it |" for i in ids[:5]] + full[5:] + inv_rows + hit_rows,
            "range PASS": full + ["| SEC-001..SEC-010 | PASS | all fine in src/a.ts |"] + inv_rows + hit_rows,
            "core module N/A as a whole": [r_ for r_ in full if not r_.startswith("| SEC-")] + ["| SEC-* | N/A | no security needed here |"] + inv_rows + hit_rows,
            "sweep hit not reviewed": full + inv_rows,
            "inventory not accounted": full + hit_rows,
            "inventory undercounted": full + [x.replace(f"{counts['pages']}/{counts['pages']}", "1/1") if x.startswith("| INV-pages") else x for x in inv_rows] + hit_rows,
        }
        for name, rows in bad.items():
            r = run("coverage.py", str(ledger(out, rows)))
            check(r.returncode == 1 and "GAP:" in r.stdout, f"coverage: should reject '{name}'")

        # FAIL with a confidence label and CAN'T TELL are accepted; quick level needs fewer checks
        ok_rows = [full[0].replace("PASS", "FAIL ✅ Confirmed"), full[1].replace("PASS", "CAN'T TELL")] + full[2:] + inv_rows + hit_rows
        r = run("coverage.py", str(ledger(out, ok_rows)))
        check(r.returncode == 0 and "1 blockers" in r.stdout, f"coverage: labelled FAIL should pass and count as a blocker:\n{r.stdout[-400:]}")
        quick = [x for x in full if x.startswith("| BS-")] + inv_rows + hit_rows
        r = run("coverage.py", str(ledger(out, quick, "Quick")))
        check(r.returncode == 1, "coverage: Quick still needs every 🔴 core check")
        r = run("coverage.py", str(ledger(out, quick, "Quick")), "--remaining")
        check("security" in r.stdout and "blind-spots" not in r.stdout, "coverage --remaining: wrong list")

    # version check: never blocks, never fails, says the right thing
    import os, time
    mine = re.search(r'version:\s*"([\d.]+)"', (ROOT / "skills/vibe-check/SKILL.md").read_text()).group(1)
    major = int(mine.split(".")[0])
    r = run("version_check.py", "--latest", f"{major + 1}.0.0")
    check(r.returncode == 0 and r.stdout.startswith("UPDATE AVAILABLE") and "npx skills update" in r.stdout,
          f"version_check: newer release not reported: {r.stdout!r}")
    r = run("version_check.py", "--latest", mine)
    check(r.stdout.startswith("UP TO DATE"), f"version_check: same version should be up to date: {r.stdout!r}")
    r = run("version_check.py", "--latest", "0.0.1")
    check(r.stdout.startswith("UP TO DATE"), f"version_check: older release should be up to date: {r.stdout!r}")
    base = {k: v for k, v in os.environ.items() if "proxy" not in k.lower()}
    dead = dict(base, HTTPS_PROXY="http://127.0.0.1:9", https_proxy="http://127.0.0.1:9", NO_PROXY="", no_proxy="")
    r = run("version_check.py", env=dict(dead, VIBE_CHECK_NO_UPDATE_CHECK="1"))
    check(r.returncode == 0 and r.stdout.startswith("SKIPPED: turned off"), f"version_check: opt-out ignored: {r.stdout!r}")
    with tempfile.TemporaryDirectory() as tmp2:
        (Path(tmp2) / ".vibe-check").mkdir()
        (Path(tmp2) / ".vibe-check" / "config").write_text("footer: true\nupdate_check: false\n")
        r = run("version_check.py", cwd=Path(tmp2), env=dead)
        check(r.stdout.startswith("SKIPPED: turned off (.vibe-check/config)"), f"version_check: config opt-out ignored: {r.stdout!r}")
    t0 = time.time()
    r = run("version_check.py", env=dead)
    check(r.returncode == 0 and r.stdout.startswith("SKIPPED: couldn't reach") and "releases/latest" in r.stdout
          and time.time() - t0 < 15,
          f"version_check: offline should skip quietly and fast: {r.stdout!r} {r.stderr[-200:]!r}")

    print(f"test bench: {len(EXPECT_PATTERNS)} planted problems, {len(EXPECT_INVENTORY)} inventory categories, 13 ledger cases, 6 version-check cases")
    for f in failures:
        print("FAIL:", f)
    print("OK: scripts catch every planted problem." if not failures else f"{len(failures)} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
