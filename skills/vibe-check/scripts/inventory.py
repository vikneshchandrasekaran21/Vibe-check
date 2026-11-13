#!/usr/bin/env python3
"""vibe-check inventory: list everything in the app BEFORE checking it.

Bugs hide in the one route nobody opened. This script lists pages, API routes, server actions,
functions, webhooks, cron jobs, forms, buttons and links, env vars, tables, storage buckets,
file uploads, payment, email and AI calls, and third-party scripts. The AI then accounts for
every item (for example "API routes checked: 47/47") and adds anything the script missed.

Usage:  python3 inventory.py [PROJECT_DIR] [--out .vibe-check]
Writes: <out>/inventory.md and <out>/inventory.json (read by coverage.py)
Read-only. Heuristic: it finds the common patterns; the AI must add what it misses.
Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", ".svelte-kit", ".output", "dist", "build", "out", "coverage",
    ".vibe-check", "vendor", ".venv", "venv", "env", "__pycache__", ".turbo", ".vercel", ".netlify", ".expo",
    "Pods", "target", ".gradle", ".idea", ".cache", "storybook-static", ".wrangler",
}
EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro", ".py", ".rb", ".php",
       ".go", ".dart", ".kt", ".swift", ".html", ".sql", ".prisma", ".rules", ".json", ".yaml", ".yml", ".toml")
PUBLIC_PREFIX = re.compile(r"^(NEXT_PUBLIC_|VITE_|EXPO_PUBLIC_|REACT_APP_|PUBLIC_|NUXT_PUBLIC_|GATSBY_)")

CATEGORIES = {
    "pages": "Pages and screens",
    "api_routes": "API routes and endpoints",
    "server_actions": "Server actions",
    "functions": "Serverless / edge / cloud functions",
    "webhooks": "Webhooks",
    "cron": "Cron and scheduled jobs",
    "admin": "Admin and internal areas",
    "forms": "Forms",
    "buttons_links": "Buttons and links (file:line)",
    "env_vars": "Environment variables",
    "db_tables": "Database tables and collections",
    "storage_buckets": "Storage buckets",
    "file_uploads": "File uploads",
    "payments": "Payment code",
    "email": "Email sending",
    "ai_calls": "AI / LLM calls",
    "third_party_scripts": "Third-party scripts and embeds",
}
# (category, regex on content, capture group or 0 for "file:line")
CONTENT = [
    ("api_routes", re.compile(r"""\b(?:app|router|server|api|route|fastify|hono)\.(get|post|put|patch|delete|all)\(\s*["'`](/[^"'`]*)"""), "method_path"),
    ("api_routes", re.compile(r"""@\w+\.(get|post|put|patch|delete|route|api_route)\(\s*["'](/[^"']*)"""), "method_path"),
    ("api_routes", re.compile(r"""\bpath\(\s*["']([^"']+)["']\s*,"""), 1),
    ("pages", re.compile(r"""<Route\b[^>]*\bpath=["']([^"']+)"""), 1),
    ("pages", re.compile(r"""\{\s*path:\s*["'](/[^"']*)["']"""), 1),
    ("cron", re.compile(r"""cron\.schedule\(\s*["']([^"']+)|schedule\(\s*["']([^"']*\*[^"']*)["']|"schedule"\s*:\s*"([^"]+)"|^\s*-\s*cron:\s*["']?([^"'\n]+)"""), 0),
    ("forms", re.compile(r"<form\b|\bonSubmit\s*=|\bhandleSubmit\(|@submit\b|on:submit"), 0),
    ("buttons_links", re.compile(r"<(?:button|Button|a|Link|NuxtLink|RouterLink|Pressable|TouchableOpacity)\b|\bonClick\s*=|\bonPress\s*=|@click\b|on:click"), 0),
    ("db_tables", re.compile(r"""create\s+table\s+(?:if\s+not\s+exists\s+)?([\w."]+)""", re.I), 1),
    ("db_tables", re.compile(r"""^model\s+(\w+)\s*\{""", re.M), 1),
    ("db_tables", re.compile(r"""(?:pgTable|mysqlTable|sqliteTable)\(\s*["'](\w+)"""), 1),
    ("db_tables", re.compile(r"""\.from\(\s*["'](\w+)["']\s*\)\s*\.\s*(?:select|insert|update|upsert|delete)"""), 1),
    ("db_tables", re.compile(r"""\bcollection\(\s*(?:\w+\s*,\s*)?["'](\w+)["']"""), 1),
    ("db_tables", re.compile(r"""mongoose\.model\(\s*["'](\w+)"""), 1),
    ("storage_buckets", re.compile(r"""storage\s*\.from\(\s*["']([\w-]+)"""), 1),
    ("storage_buckets", re.compile(r"""insert\s+into\s+storage\.buckets[^;]*?values\s*\(\s*'([\w-]+)'""", re.I), 1),
    ("storage_buckets", re.compile(r"""\bBucket\s*:\s*["']([\w.-]+)"""), 1),
    ("file_uploads", re.compile(r"""type=["']file["']|\bmulter\b|createSignedUploadUrl|\bformidable\b|\bbusboy\b|UploadFile|\.upload\(|launchImageLibraryAsync|DocumentPicker"""), 0),
    ("payments", re.compile(r"""from\s+["'](?:stripe|@stripe/[\w-]+|razorpay|@paddle/[\w-]+|@lemonsqueezy/[\w-]+|@paypal/[\w-]+)["']|require\(\s*["'](?:stripe|razorpay)["']\)|^\s*import\s+(?:stripe|razorpay)\b|checkout\.sessions\.create|paymentIntents\.create""", re.M), 0),
    ("email", re.compile(r"""from\s+["'](?:resend|@sendgrid/mail|nodemailer|postmark|mailgun\.js|@react-email/[\w-]+)["']|require\(\s*["'](?:nodemailer|@sendgrid/mail|postmark)["']\)|SendEmailCommand|emails\.send\(|sendMail\("""), 0),
    ("ai_calls", re.compile(r"""chat\.completions\.create|responses\.create|messages\.create|generateContent|\bgenerateText\(|\bstreamText\(|\bgenerateObject\(|\bstreamObject\(|ChatOpenAI|ChatAnthropic|ollama\.chat|\.embeddings\.create"""), 0),
    ("third_party_scripts", re.compile(r"""<(?:script|Script)\b[^>]*\bsrc=["'](https?://[^"']+)|<iframe\b[^>]*\bsrc=["'](https?://[^"']+)"""), 0),
]
ENV_RX = [
    re.compile(r"process\.env\.([A-Z][A-Z0-9_]+)"), re.compile(r"""process\.env\[\s*["']([A-Z][A-Z0-9_]+)"""),
    re.compile(r"import\.meta\.env\.([A-Z][A-Z0-9_]+)"), re.compile(r"""os\.(?:environ\.get|getenv)\(\s*["']([A-Z][A-Z0-9_]+)"""),
    re.compile(r"""os\.environ\[\s*["']([A-Z][A-Z0-9_]+)"""), re.compile(r"""Deno\.env\.get\(\s*["']([A-Z][A-Z0-9_]+)"""),
    re.compile(r"""\benv\(\s*["']([A-Z][A-Z0-9_]+)"""),
]


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = p.relative_to(root).as_posix()
            if fn.startswith(".env"):
                yield rel, p
            elif fn.lower().endswith(EXT) and not fn.endswith((".min.js", "package-lock.json")):
                yield rel, p


def file_based(rel: str):
    """Return (category, item) pairs decided by the file path alone."""
    out = []
    r = rel
    if re.search(r"(^|/)app/(?:.*/)?page\.(tsx|jsx|ts|js|mdx)$", r):
        out.append(("pages", "/" + re.sub(r"(^|.*/)app/|/?page\.\w+$", "", r).strip("/")))
    if re.search(r"(^|/)app/(?:.*/)?route\.(ts|js)$", r):
        out.append(("api_routes", "/" + re.sub(r"(^|.*/)app/|/?route\.\w+$", "", r).strip("/")))
    m = re.search(r"(?:^|/)pages/(.+)\.(tsx|jsx|ts|js|vue|astro|md|mdx)$", r)
    if m and not re.search(r"(^|/)_(app|document|error)\.", r):
        out.append(("api_routes" if m.group(1).startswith("api/") else "pages", "/" + re.sub(r"(^|/)index$", "", m.group(1))))
    m = re.search(r"(?:^|/)app/routes/(.+)\.(tsx|jsx|ts|js)$", r)  # Remix / React Router 7
    if m:
        out.append(("pages", "/" + m.group(1)))
    m = re.search(r"(?:^|/)src/routes/(.*?)/?\+(page|server)\.(svelte|ts|js)$", r)  # SvelteKit
    if m:
        out.append(("pages" if m.group(2) == "page" else "api_routes", "/" + m.group(1)))
    m = re.search(r"(?:^|/)server/api/(.+)\.(ts|js)$", r)  # Nuxt
    if m:
        out.append(("api_routes", "/api/" + m.group(1)))
    m = re.search(r"(?:^|/)supabase/functions/([\w-]+)/index\.(ts|js)$", r)
    if m and not m.group(1).startswith("_"):
        out.append(("functions", "supabase:" + m.group(1)))
    m = re.search(r"(?:^|/)(?:netlify/functions|api)/([\w-]+)\.(ts|js|py)$", r)
    if m and "/app/" not in "/" + r and "pages/" not in r:
        out.append(("functions", r))
    if re.search(r"webhook", r, re.I):
        out.append(("webhooks", r))
    if re.search(r"(^|/)(admin|internal|backoffice|staff)(/|\.|$)", r, re.I):
        out.append(("admin", r))
    return out


def main() -> int:
    argv = sys.argv[1:]
    out_arg = None
    if "--out" in argv:
        i = argv.index("--out"); out_arg = argv[i + 1]; del argv[i:i + 2]
    root = Path(argv[0] if argv else ".").resolve()
    out = Path(out_arg).resolve() if out_arg else root / ".vibe-check"
    found = {k: set() for k in CATEGORIES}
    env_public = {}
    scanned = 0
    for rel, p in walk(root):
        try:
            if p.stat().st_size > 1_500_000:
                continue
            text = p.read_text("utf-8", "replace")
        except OSError:
            continue
        scanned += 1
        for cat, item in file_based(rel):
            found[cat].add(item)
        if p.name.startswith(".env"):
            for k in re.findall(r"^\s*(?:export\s+)?([A-Z][A-Z0-9_]+)\s*=", text, re.M):
                env_public[k] = bool(PUBLIC_PREFIX.match(k))
            continue
        if "use server" in text and re.search(r"""^\s*["']use server["']""", text, re.M):
            found["server_actions"].add(rel)
        if rel.endswith("vercel.json"):
            for path in re.findall(r'"path"\s*:\s*"([^"]+)"', text.split('"crons"', 1)[1] if '"crons"' in text else ""):
                found["cron"].add("vercel cron " + path)
        if re.search(r"exports\.(\w+)\s*=\s*functions\.|export\s+const\s+(\w+)\s*=\s*(?:onCall|onRequest|onSchedule|onDocument\w*)\(", text):
            for name in re.findall(r"exports\.(\w+)\s*=\s*functions\.|export\s+const\s+(\w+)\s*=\s*(?:onCall|onRequest|onSchedule|onDocument\w*)\(", text):
                found["functions"].add("firebase:" + (name[0] or name[1]))
        lines = text.splitlines()
        for cat, rx, how in CONTENT:
            if cat in ("db_tables", "storage_buckets") and how == 1:
                for m in rx.finditer(text):
                    found[cat].add(m.group(1).strip('"').split(".")[-1])
                continue
            for n, line in enumerate(lines, 1):
                if len(line) > 2000:
                    continue
                for m in rx.finditer(line):
                    if how == "method_path":
                        found[cat].add(f"{m.group(1).upper()} {m.group(2)}  ({rel}:{n})")
                    elif how == 1:
                        found[cat].add(f"{m.group(1)}  ({rel}:{n})")
                    elif cat == "third_party_scripts":
                        found[cat].add(f"{m.group(1) or m.group(2)}  ({rel}:{n})")
                    else:
                        found[cat].add(f"{rel}:{n}")
        for rx in ENV_RX:
            for k in rx.findall(text):
                env_public.setdefault(k, bool(PUBLIC_PREFIX.match(k)))
    for k, pub in env_public.items():
        found["env_vars"].add(k + ("  (PUBLIC: reaches the browser)" if pub else ""))

    data = {k: sorted(v) for k, v in found.items()}
    out.mkdir(parents=True, exist_ok=True)
    meta = {"tool": "vibe-check inventory", "version": "2.7.0", "root": str(root),
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "files_scanned": scanned, "counts": {k: len(v) for k, v in data.items()}, "items": data}
    (out / "inventory.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    md = ["# vibe-check inventory", "", f"Files scanned: **{scanned}**. Heuristic: add anything this missed.", "",
          "| Category | Found | Ledger row |", "|---|---|---|"]
    for k, label in CATEGORIES.items():
        md.append(f"| {label} | {len(data[k])} | `INV-{k}` |")
    for k, label in CATEGORIES.items():
        if data[k]:
            md += ["", f"## {label} ({len(data[k])})", ""] + [f"- {x}" for x in data[k]]
    (out / "inventory.md").write_text("\n".join(md) + "\n")
    print(f"inventory: {scanned} files -> {out / 'inventory.md'}")
    for k, label in CATEGORIES.items():
        print(f"  {k:<20} {len(data[k]):>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
