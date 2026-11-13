#!/usr/bin/env python3
"""vibe-check versions: list everything the app runs, with exact versions.

Package audits only see libraries. This lists the runtime (PHP, Node, Python, Ruby, Go, Java…),
frameworks and key packages with their locked versions, WordPress core, plugins and themes,
Docker base images and services, database engines, mobile SDK targets and hosting runtimes,
plus which audit tool to run for each ecosystem found. The AI then checks every component
against today's advisories (references/vulnerabilities.md) and records a verdict per V- row.

Usage:  python3 versions.py [PROJECT_DIR] [--out .vibe-check]
Writes: <out>/versions.md and <out>/versions.json (read by coverage.py)
Read-only and offline: it only reads files in the project. Python 3.8+, standard library only.
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
    "Pods", "target", ".gradle", ".idea", ".cache", ".wrangler",
}
# packages worth tracking by name (frameworks, auth, parsers, servers, SDKs): ecosystem -> names
KEY_PACKAGES = {
    "npm": ["next", "react", "react-dom", "nuxt", "vue", "@sveltejs/kit", "svelte", "astro", "@remix-run/node",
            "react-router", "express", "fastify", "@nestjs/core", "hono", "koa", "vite", "@angular/core", "gatsby",
            "@strapi/strapi", "electron", "expo", "react-native", "@capacitor/core", "@tauri-apps/api",
            "@supabase/supabase-js", "@supabase/ssr", "firebase", "firebase-admin", "stripe", "next-auth",
            "@auth/core", "@clerk/nextjs", "jsonwebtoken", "jose", "passport", "axios", "graphql", "@apollo/server",
            "apollo-server", "socket.io", "ws", "prisma", "@prisma/client", "drizzle-orm", "sequelize", "mongoose",
            "typeorm", "multer", "sharp", "puppeteer", "xml2js", "fast-xml-parser", "lodash", "handlebars", "ejs",
            "pug", "marked", "dompurify", "openai", "@anthropic-ai/sdk", "ai", "wrangler"],
    "composer": ["laravel/framework", "symfony/http-kernel", "symfony/symfony", "slim/slim", "cakephp/cakephp",
                 "yiisoft/yii2", "codeigniter4/framework", "drupal/core", "magento/product-community-edition",
                 "guzzlehttp/guzzle", "twig/twig", "phpmailer/phpmailer", "firebase/php-jwt", "league/flysystem",
                 "livewire/livewire", "filament/filament", "laravel/sanctum", "laravel/passport"],
    "pypi": ["django", "flask", "fastapi", "starlette", "uvicorn", "gunicorn", "werkzeug", "jinja2", "sqlalchemy",
             "pydantic", "requests", "urllib3", "pyjwt", "cryptography", "pillow", "lxml", "celery", "langchain",
             "openai", "anthropic", "streamlit", "gradio"],
    "rubygems": ["rails", "rack", "puma", "devise", "nokogiri", "sidekiq"],
}
Q = '"'
FRAMEWORKS = {"next", "nuxt", "@sveltejs/kit", "astro", "@remix-run/node", "react-router", "express", "fastify",
              "@nestjs/core", "hono", "koa", "@angular/core", "gatsby", "@strapi/strapi", "electron", "expo", "react-native",
              "@capacitor/core"}
PIN = re.compile(r"^\s*(\d+(?:\.\d+){0,3})")


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        depth = len(Path(dirpath).relative_to(root).parts)
        for fn in filenames:
            yield Path(dirpath) / fn, depth


def read(p: Path) -> str:
    try:
        return p.read_text("utf-8", "replace") if p.stat().st_size < 3_000_000 else ""
    except OSError:
        return ""


def line_of(text: str, needle: str) -> int:
    i = text.find(needle)
    return text.count("\n", 0, i) + 1 if i >= 0 else 0


class Found:
    def __init__(self):
        self.items = []
        self.seen = set()

    def add(self, kind, name, version, where, ecosystem=""):
        version = (version or "").strip().strip("\"'")
        key = (kind, name.lower(), version, where.split(":")[0])
        if key in self.seen or not name:
            return
        self.seen.add(key)
        self.items.append({"kind": kind, "name": name, "version": version or "unknown (not pinned)",
                           "where": where, "ecosystem": ecosystem})


def npm_locked(root_dir: Path, files: dict):
    """name -> exact version from package-lock.json, pnpm-lock.yaml, yarn.lock or bun.lock in this folder."""
    out = {}
    pl = files.get("package-lock.json")
    if pl:
        try:
            data = json.loads(read(pl))
            for k, v in (data.get("packages") or {}).items():
                if k.startswith("node_modules/") and k.count("node_modules/") == 1 and isinstance(v, dict):
                    out.setdefault(k[len("node_modules/"):], v.get("version", ""))
            for k, v in (data.get("dependencies") or {}).items():
                if isinstance(v, dict):
                    out.setdefault(k, v.get("version", ""))
        except ValueError:
            pass
    pn = files.get("pnpm-lock.yaml")
    if pn:
        for m in re.finditer(r"^\s{2,4}'?/?(@?[^@\s'/]+(?:/[^@\s']+)?)@(\d+\.\d+\.\d+[^\s:'(]*)", read(pn), re.M):
            out.setdefault(m.group(1), m.group(2))
    yl = files.get("yarn.lock")
    if yl:
        for m in re.finditer(r'^"?(@?[^@\s"]+)@[^\n]*:\n\s+version:?\s+"?([\d][^"\s]*)', read(yl), re.M):
            out.setdefault(m.group(1), m.group(2))
    bl = files.get("bun.lock")
    if bl:
        for m in re.finditer(r'"(@?[^"@]+)":\s*\["\1@(\d[^"]*)"', read(bl)):
            out.setdefault(m.group(1), m.group(2))
    return out


def main() -> int:
    argv = sys.argv[1:]
    out_arg = None
    if "--out" in argv:
        i = argv.index("--out"); out_arg = argv[i + 1]; del argv[i:i + 2]
    root = Path(argv[0] if argv else ".").resolve()
    out = Path(out_arg).resolve() if out_arg else root / ".vibe-check"
    f = Found()
    ecosystems = {}
    by_dir = {}
    plugin_files = []
    for p, depth in walk(root):
        by_dir.setdefault(p.parent, {})[p.name] = p
        rel = p.relative_to(root).as_posix()
        if re.search(r"wp-content/(plugins|themes)/[^/]+/[^/]+\.(php|css)$", rel):
            plugin_files.append(p)

    for d, files in sorted(by_dir.items()):
        reld = d.relative_to(root).as_posix()
        pre = "" if reld == "." else reld + "/"
        # ---- JavaScript
        if "package.json" in files:
            pj = read(files["package.json"])
            try:
                data = json.loads(pj)
            except ValueError:
                data = {}
            eng = (data.get("engines") or {}).get("node")
            if eng:
                f.add("runtime", "Node.js", eng, f"{pre}package.json:{line_of(pj, Q + 'node' + Q)} (engines)", "npm")
            locked = npm_locked(d, files)
            declared = {}
            for sect in ("dependencies", "devDependencies", "peerDependencies"):
                declared.update({k: v for k, v in (data.get(sect) or {}).items()})
            lock_name = next((n for n in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock") if n in files), "")
            if declared:
                ecosystems.setdefault("npm", set()).add(pre + (lock_name or "package.json (no lockfile!)"))
            for name in KEY_PACKAGES["npm"]:
                if name in declared:
                    v = locked.get(name) or declared[name]
                    src = f"{pre}{lock_name}" if locked.get(name) else f"{pre}package.json:{line_of(pj, Q + name + Q)} (range, no lockfile entry)"
                    f.add("framework" if name in FRAMEWORKS else "package", name, v, src, "npm")
        for fn in (".nvmrc", ".node-version"):
            if fn in files:
                f.add("runtime", "Node.js", read(files[fn]).strip().splitlines()[0] if read(files[fn]).strip() else "", f"{pre}{fn}:1")
        # ---- PHP
        if "composer.json" in files:
            cj = read(files["composer.json"])
            try:
                data = json.loads(cj)
            except ValueError:
                data = {}
            req = data.get("require") or {}
            if req.get("php"):
                f.add("runtime", "PHP", req["php"], f"{pre}composer.json:{line_of(cj, Q + 'php' + Q)} (require)", "composer")
            plat = ((data.get("config") or {}).get("platform") or {}).get("php")
            if plat:
                f.add("runtime", "PHP", plat, f"{pre}composer.json:{line_of(cj, Q + 'platform' + Q)} (config.platform)", "composer")
            ecosystems.setdefault("composer", set()).add(pre + ("composer.lock" if "composer.lock" in files else "composer.json (no lockfile!)"))
            locked = {}
            if "composer.lock" in files:
                try:
                    lk = json.loads(read(files["composer.lock"]))
                    for pkg in (lk.get("packages") or []) + (lk.get("packages-dev") or []):
                        locked[pkg.get("name", "")] = pkg.get("version", "")
                except ValueError:
                    pass
            for name in KEY_PACKAGES["composer"]:
                if name in req or name in locked:
                    f.add("framework" if name in ("laravel/framework", "symfony/http-kernel", "symfony/symfony", "drupal/core") else "package",
                          name, locked.get(name) or req.get(name, ""), f"{pre}{'composer.lock' if name in locked else 'composer.json'}", "composer")
        if ".php-version" in files:
            f.add("runtime", "PHP", read(files[".php-version"]).strip(), f"{pre}.php-version:1")
        if "version.php" in files and pre.endswith("wp-includes/"):
            m = re.search(r"\$wp_version\s*=\s*'([^']+)'", read(files["version.php"]))
            if m:
                f.add("cms", "WordPress core", m.group(1), f"{pre}version.php", "wordpress")
                ecosystems.setdefault("wordpress", set()).add(pre)
        # ---- Python
        for fn in (".python-version", "runtime.txt"):
            if fn in files:
                f.add("runtime", "Python", read(files[fn]).strip().replace("python-", ""), f"{pre}{fn}:1")
        if "pyproject.toml" in files:
            pt = read(files["pyproject.toml"])
            m = re.search(r'requires-python\s*=\s*"([^"]+)"', pt) or re.search(r'^python\s*=\s*"([^"]+)"', pt, re.M)
            if m:
                f.add("runtime", "Python", m.group(1), f"{pre}pyproject.toml:{line_of(pt, m.group(0))}")
            ecosystems.setdefault("pypi", set()).add(pre + "pyproject.toml")
        pylocks = {}
        for fn in ("poetry.lock", "uv.lock"):
            if fn in files:
                for m in re.finditer(r'name\s*=\s*"([^"]+)"\s*\nversion\s*=\s*"([^"]+)"', read(files[fn])):
                    pylocks[m.group(1).lower()] = (m.group(2), fn)
                ecosystems.setdefault("pypi", set()).add(pre + fn)
        for fn in [n for n in files if re.match(r"requirements.*\.txt$", n)]:
            txt = read(files[fn])
            ecosystems.setdefault("pypi", set()).add(pre + fn)
            for n, line in enumerate(txt.splitlines(), 1):
                m = re.match(r"\s*([A-Za-z0-9_.\-\[\]]+)\s*(==|>=|~=|<=)?\s*([\w.*]+)?", line)
                if m and m.group(1).split("[")[0].lower() in KEY_PACKAGES["pypi"]:
                    f.add("framework" if m.group(1).lower() in ("django", "flask", "fastapi") else "package",
                          m.group(1).split("[")[0].lower(), ((m.group(2) or "") + (m.group(3) or "")).lstrip("="), f"{pre}{fn}:{n}", "pypi")
        for name in KEY_PACKAGES["pypi"]:
            if name in pylocks:
                f.add("framework" if name in ("django", "flask", "fastapi") else "package", name, pylocks[name][0], f"{pre}{pylocks[name][1]}", "pypi")
        # ---- Ruby
        if ".ruby-version" in files:
            f.add("runtime", "Ruby", read(files[".ruby-version"]).strip(), f"{pre}.ruby-version:1")
        if "Gemfile.lock" in files:
            gl = read(files["Gemfile.lock"])
            ecosystems.setdefault("rubygems", set()).add(pre + "Gemfile.lock")
            for name in KEY_PACKAGES["rubygems"]:
                m = re.search(r"^\s{4}" + re.escape(name) + r" \(([^)]+)\)", gl, re.M)
                if m:
                    f.add("framework" if name == "rails" else "package", name, m.group(1), f"{pre}Gemfile.lock:{line_of(gl, m.group(0))}", "rubygems")
            m = re.search(r"RUBY VERSION\s*\n\s*ruby ([\d.]+)", gl)
            if m:
                f.add("runtime", "Ruby", m.group(1), f"{pre}Gemfile.lock (RUBY VERSION)")
        # ---- Go / Rust / Java / .NET
        if "go.mod" in files:
            gm = read(files["go.mod"])
            m = re.search(r"^go (\d[\d.]*)", gm, re.M)
            if m:
                f.add("runtime", "Go", m.group(1), f"{pre}go.mod:{line_of(gm, m.group(0))}", "go")
            ecosystems.setdefault("go", set()).add(pre + "go.mod")
        if "Cargo.lock" in files:
            ecosystems.setdefault("cargo", set()).add(pre + "Cargo.lock")
        for fn in ("rust-toolchain", "rust-toolchain.toml"):
            if fn in files:
                m = re.search(r"(\d+\.\d+(?:\.\d+)?|stable|nightly)", read(files[fn]))
                f.add("runtime", "Rust", m.group(1) if m else "", f"{pre}{fn}")
        if "pom.xml" in files or "build.gradle" in files or "build.gradle.kts" in files:
            for fn in ("pom.xml", "build.gradle", "build.gradle.kts"):
                if fn in files:
                    t = read(files[fn])
                    ecosystems.setdefault("maven/gradle", set()).add(pre + fn)
                    m = re.search(r"<java\.version>([^<]+)<|<maven\.compiler\.release>([^<]+)<|JavaVersion\.VERSION_(\d+)|jvmTarget\s*=\s*[\"']?(\d+)", t)
                    if m:
                        f.add("runtime", "Java", next(g for g in m.groups() if g), f"{pre}{fn}:{line_of(t, m.group(0))}")
                    m = re.search(r"org\.springframework\.boot['\"]?\s*version\s*['\"]([\d.]+)|<artifactId>spring-boot-starter-parent</artifactId>\s*<version>([\d.]+)", t)
                    if m:
                        f.add("framework", "Spring Boot", next(g for g in m.groups() if g), f"{pre}{fn}:{line_of(t, m.group(0))}", "maven")
                    for key, label in (("targetSdk", "Android targetSdk"), ("compileSdk", "Android compileSdk")):
                        m = re.search(key + r"(?:Version)?\s*[= ]\s*(\d+)", t)
                        if m:
                            f.add("sdk", label, m.group(1), f"{pre}{fn}:{line_of(t, m.group(0))}")
        for fn in [n for n in files if n.endswith(".csproj")]:
            t = read(files[fn])
            m = re.search(r"<TargetFramework>([^<]+)<", t)
            if m:
                f.add("runtime", ".NET", m.group(1), f"{pre}{fn}:{line_of(t, m.group(0))}", "nuget")
            ecosystems.setdefault("nuget", set()).add(pre + fn)
        if "Podfile" in files:
            m = re.search(r"platform\s+:ios,\s*'([\d.]+)'", read(files["Podfile"]))
            if m:
                f.add("sdk", "iOS deployment target", m.group(1), f"{pre}Podfile")
        if ".tool-versions" in files:
            for n, line in enumerate(read(files[".tool-versions"]).splitlines(), 1):
                parts = line.split()
                if len(parts) >= 2:
                    f.add("runtime", {"nodejs": "Node.js", "php": "PHP", "python": "Python", "ruby": "Ruby",
                                      "golang": "Go", "java": "Java"}.get(parts[0], parts[0]), parts[1], f"{pre}.tool-versions:{n}")
        # ---- Containers, services, hosting
        for fn in [n for n in files if n == "Dockerfile" or n.startswith("Dockerfile.") or n.endswith(".Dockerfile") or n == "Containerfile"]:
            t = read(files[fn])
            stages = set(m.group(1).lower() for m in re.finditer(r"^FROM\s+\S+\s+(?:AS|as)\s+(\S+)", t, re.M))
            for m in re.finditer(r"^FROM\s+(?:--platform=\S+\s+)?(\S+)", t, re.M):
                img = m.group(1)
                if img.lower() in stages or img.startswith("$"):
                    continue
                name, _, tag = img.partition(":")
                f.add("image", name, tag or "latest (not pinned)", f"{pre}{fn}:{line_of(t, m.group(0))}", "docker")
                ecosystems.setdefault("docker", set()).add(pre + fn)
        for fn in [n for n in files if re.match(r"(docker-)?compose(\.[\w-]+)?\.ya?ml$", n)]:
            t = read(files[fn])
            for m in re.finditer(r"^\s+image:\s*[\"']?([^\s\"'#]+)", t, re.M):
                name, _, tag = m.group(1).partition(":")
                f.add("service", name, tag or "latest (not pinned)", f"{pre}{fn}:{line_of(t, m.group(0))}", "docker")
                ecosystems.setdefault("docker", set()).add(pre + fn)
        if "config.toml" in files and pre.endswith("supabase/"):
            m = re.search(r"major_version\s*=\s*(\d+)", read(files["config.toml"]))
            if m:
                f.add("service", "Postgres (Supabase)", m.group(1), f"{pre}config.toml")
        for fn in ("wrangler.toml", "wrangler.json", "wrangler.jsonc"):
            if fn in files:
                t = read(files[fn])
                m = re.search(r"compatibility_date[\"']?\s*[:=]\s*[\"']([\d-]+)", t)
                if m:
                    f.add("platform", "Cloudflare Workers compatibility date", m.group(1), f"{pre}{fn}:{line_of(t, m.group(0))}")
        for fn in ("netlify.toml",):
            if fn in files:
                m = re.search(r"NODE_VERSION\s*=\s*[\"']?([\d.]+)", read(files[fn]))
                if m:
                    f.add("runtime", "Node.js", m.group(1), f"{pre}{fn} (NODE_VERSION)")
        if "app.json" in files or "app.config.js" in files:
            t = read(files.get("app.json") or files["app.config.js"])
            m = re.search(r"\"sdkVersion\"\s*:\s*\"([^\"]+)\"", t)
            if m:
                f.add("sdk", "Expo SDK", m.group(1), f"{pre}app.json")

    # ---- WordPress plugins and themes (each one is a component)
    for p in plugin_files:
        t = read(p)[:8000]
        rel = p.relative_to(root).as_posix()
        kind = "plugin" if "/plugins/" in rel else "theme"
        name = re.search(r"^\s*\*?\s*(?:Plugin|Theme) Name:\s*(.+)$", t, re.M)
        ver = re.search(r"^\s*\*?\s*Version:\s*([\w.\-]+)", t, re.M)
        if name:
            f.add(kind, "WordPress " + kind + ": " + name.group(1).strip(), ver.group(1) if ver else "", rel, "wordpress")
            ecosystems.setdefault("wordpress", set()).add(rel.split("/wp-content/")[0] + "/wp-content" if "/wp-content/" in rel else "wp-content")

    items = sorted(f.items, key=lambda x: (["runtime", "framework", "cms", "plugin", "theme", "image", "service", "platform", "sdk", "package"].index(x["kind"]), x["name"].lower()))
    for i, it in enumerate(items, 1):
        it["id"] = f"V-{i:03d}"
    tools = {
        "npm": "npm audit --omit=dev / pnpm audit --prod / yarn npm audit", "composer": "composer audit",
        "pypi": "pip-audit", "rubygems": "bundle audit check --update", "go": "govulncheck ./...",
        "cargo": "cargo audit", "maven/gradle": "osv-scanner or OWASP Dependency-Check", "nuget": "dotnet list package --vulnerable",
        "docker": "trivy image <name> or docker scout cves", "wordpress": "wp plugin list --update=available (WP-CLI) or WPScan",
    }
    eco = {k: sorted(v) for k, v in ecosystems.items()}
    out.mkdir(parents=True, exist_ok=True)
    meta = {"tool": "vibe-check versions", "version": "2.8.0", "root": str(root),
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "components": items, "ecosystems": eco, "audit_tools": {k: tools.get(k, "osv-scanner") for k in eco}}
    (out / "versions.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    md = ["# vibe-check versions", "",
          f"**{len(items)} components** found. Check each against today's advisories and end-of-life dates "
          "(`references/vulnerabilities.md`), then give each `V-` row a verdict in the ledger: "
          "`CURRENT`, `OUTDATED`, `EOL`, `VULNERABLE` or `CAN'T TELL`, with the source URL you opened (or the audit tool you ran). "
          "Add anything this missed.", "",
          "| Row | Kind | Component | Version | Found in |", "|---|---|---|---|---|"]
    for it in items:
        md.append(f"| {it['id']} | {it['kind']} | {it['name']} | `{it['version']}` | `{it['where']}` |")
    md += ["", "## Ecosystems and the audit tool to run", "", "| Ecosystem | Files | Run |", "|---|---|---|"]
    for k, files_ in eco.items():
        md.append(f"| {k} | {', '.join('`' + x + '`' for x in files_)} | `{tools.get(k, 'osv-scanner')}` |")
    (out / "versions.md").write_text("\n".join(md) + "\n")
    print(f"versions: {len(items)} components, ecosystems: {', '.join(eco) or 'none'} -> {out / 'versions.md'}")
    for it in items:
        print(f"  {it['id']}  {it['kind']:<9} {it['name'][:40]:<40} {it['version'][:24]:<24} {it['where'][:50]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
