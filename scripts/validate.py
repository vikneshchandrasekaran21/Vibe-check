#!/usr/bin/env python3
"""Validate the vibe-check skill so nothing is missing, broken or duplicated.

Checks:
  1. SKILL.md frontmatter (name matches folder, lowercase, description length, version).
  2. Every reference file is listed in SKILL.md's module tables, and every file SKILL.md mentions exists.
  3. Every reference file is in scripts/build.py REF_ORDER (so it reaches dist/ and the Claude app zip).
  4. Every module file has a title and at least one check; every check has a severity (🔴/🟡/🟢) and a bold name.
  5. No duplicate check names inside a module; reports near-duplicates across modules.
  6. AI blind spots are numbered 1..N with no gaps.
  7. Report template contains every required section; SKILL.md self-check covers them.
  8. README mentions every module and links only to files that exist.
  9. Generated files are up to date; dist/vibe-check.md contains every module; the zip has every file;
     the Gemini TOML parses.
 10. Every check has a permanent ID (PREFIX-NNN), unique, one prefix per module; coverage.py agrees with
     SKILL.md on the core modules; the scripts compile and the test bench (tests/test_scripts.py) passes.
Usage: python3 scripts/validate.py   (exit code 1 on any error)
"""
from __future__ import annotations
import re, sys, zipfile, subprocess
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # older Python: use tomli if installed, else skip the TOML check
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:
        tomllib = None
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SK = ROOT / "skills" / "vibe-check"
REFS = SK / "references"
errors: list[str] = []
warnings: list[str] = []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

skill = (SK / "SKILL.md").read_text()

# 1. frontmatter
m = re.match(r"---\n(.*?)\n---\n", skill, re.S)
if not m: err("SKILL.md: missing frontmatter")
else:
    fm = m.group(1)
    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    ver = re.search(r'version:\s*"(\d+\.\d+\.\d+)"', fm)
    if not name or name.group(1) != SK.name: err("SKILL.md: name must match folder name")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1)): err("SKILL.md: name must be lowercase-hyphen")
    if not desc or not (20 <= len(desc.group(1)) <= 200): err(f"SKILL.md: description must be 20-200 chars (is {len(desc.group(1)) if desc else 0})")
    if not ver: err("SKILL.md: metadata.version missing")
    else:
        cl = (ROOT / "CHANGELOG.md").read_text()
        if f"## v{ver.group(1)}" not in cl: err(f"CHANGELOG.md: no entry for v{ver.group(1)}")

# 2. module tables <-> files
ref_files = {p.name for p in REFS.glob("*.md")}
mentioned = set(re.findall(r"`references/([a-z0-9-]+\.md)`", skill))
for f in sorted(mentioned - ref_files): err(f"SKILL.md mentions missing file references/{f}")
support = {"fixes.md", "report-template.md", "sweep-patterns.md", "standards.md"}
for f in sorted(ref_files - mentioned - support): err(f"references/{f} is not listed in SKILL.md's module tables")
# bare `x.md` mentions anywhere in the skill must exist
all_text = skill + "".join((REFS / f).read_text() for f in ref_files)
for f in sorted(set(re.findall(r"`([a-z0-9-]+\.md)`", all_text)) - ref_files):
    err(f"`{f}` is referenced but doesn't exist")

# 3. build order
build = (ROOT / "scripts" / "build.py").read_text()
order = re.findall(r'"([a-z0-9-]+\.md)"', build.split("REF_ORDER", 1)[1].split("]", 1)[0])
for f in sorted(ref_files - set(order)): err(f"scripts/build.py REF_ORDER is missing {f}")
for f in sorted(set(order) - ref_files): err(f"scripts/build.py REF_ORDER lists missing file {f}")

# 4/5. module structure, severities, duplicates
names_by_module: dict[str, list[str]] = {}
total = blockers = 0
all_ids: dict[str, str] = {}
prefix_owner: dict[str, str] = {}
for f in sorted(ref_files - support):
    text = (REFS / f).read_text()
    if not text.startswith("# "): err(f"{f}: must start with a '# ' title")
    items = re.findall(r"^- \[ \] (.*)$", text, re.M)
    if not items: err(f"{f}: has no checklist items")
    names = []
    for it in items:
        sev = re.match(r"(🔴|🟡|🟢) ", it)
        if not sev: err(f"{f}: item without severity: {it[:60]}"); continue
        total += 1; blockers += sev.group(1) == "🔴"
        idm = re.match(r"(?:🔴|🟡|🟢) ([A-Z0-9]+)-(\d{3}) ", it)
        if not idm: err(f"{f}: item without a check ID (PREFIX-NNN after the severity): {it[:60]}")
        else:
            cid, pre = f"{idm.group(1)}-{idm.group(2)}", idm.group(1)
            if cid in all_ids: err(f"{f}: duplicate check ID {cid} (also in {all_ids[cid]})")
            all_ids[cid] = f
            if prefix_owner.setdefault(pre, f) != f: err(f"{f}: ID prefix {pre} is already used by {prefix_owner[pre]}")
            it = re.sub(r"^(🔴|🟡|🟢) [A-Z0-9]+-\d{3} ", r"\1 ", it)
        nm = re.match(r"(?:🔴|🟡|🟢) \*\*(.+?)\*\*", it)
        if not nm and f != "platforms.md": warn(f"{f}: item without a bold name: {it[:60]}")
        names.append(re.sub(r"[^a-z0-9 ]", "", (nm.group(1) if nm else it[3:60]).lower()).strip())
    dup = {n for n in names if names.count(n) > 1}
    for d in dup: err(f"{f}: duplicate check '{d}'")
    names_by_module[f] = names
seen: dict[str, str] = {}
for f, names in names_by_module.items():
    for n in names:
        if len(n) > 12 and n in seen and seen[n] != f: warn(f"same check name in {seen[n]} and {f}: '{n}'")
        seen.setdefault(n, f)

# 6. blind spots numbering
nums = [int(n) for n in re.findall(r"^\| BS-(\d{2}) \| (?:🔴|🟡|🟢)", skill, re.M)]
for f in sorted(ref_files - support):
    owners = {p for p, o in prefix_owner.items() if o == f}
    if len(owners) > 1: err(f"{f}: uses more than one ID prefix: {sorted(owners)}")
if nums != list(range(1, len(nums) + 1)): err(f"SKILL.md: blind spots not numbered 1..N: {nums}")

# 7. report template + self-check
tpl = (REFS / "report-template.md").read_text()
for sec in ["Verdict", "Blockers", "Fix before scale", "Questions for you", "Needs a lawyer", "What passed", "Coverage", "Not checked", "Score card", "Safe to auto-fix", "Prompt to fix it",
            "Evidence:", "Ruled out:", "✅ Confirmed", "🔎 Likely", "Needs checking", "Confidence",
            "coverage.py", "Inventory", "Sweep", "Tools run", "Not done"]:
    if sec not in tpl: err(f"report-template.md: missing '{sec}'")
for must in ["coverage table", "fix prompt", "safe to auto-fix", "score card", "re-check", ".vibe-check/",
             "quote the proof", "second look", "Confirmed", "Likely", "Needs checking", "No facts from memory", "Ruled out", "try to prove the finding wrong",
             "scripts/inventory.py", "scripts/sweep.py", "scripts/coverage.py", ".vibe-check/ledger.md", "--remaining", "COMPLETE",
             "Tools run", "INV-", "RULED OUT", "references/sweep-patterns.md", "just before", "Never write a row you didn't actually check"]:
    if must.lower() not in skill.lower(): err(f"SKILL.md: report or accuracy rules don't mention '{must}'")
# accuracy rules must also be in the self-check list
selfcheck = skill.split("### Before you reply", 1)[1].split("## Step 6", 1)[0] if "### Before you reply" in skill else ""
for must in ["quotes", "second look", "Confirmed", "Likely", "from memory", "coverage.py", "COMPLETE", "inventory", "sweep hit", "Tools run", "pasted from"]:
    if must.lower() not in selfcheck.lower(): err(f"SKILL.md self-check is missing the accuracy item '{must}'")
if "## Step 4b: Verify before reporting" not in skill: err("SKILL.md: missing 'Step 4b: Verify before reporting'")
# every module in coverage template rows
cov = tpl.split("## 🧭 Coverage", 1)[1].split("## Not checked", 1)[0] if "## 🧭 Coverage" in tpl else ""
for label in ["blind-spots", "security", "reliability", "devops", "functional-qa", "legal-privacy", "launch-ux", "platforms", "lawsuits", "supply-chain", "vulnerabilities", "hunt", "maintainability"]:
    if label.lower() not in cov.lower(): err(f"report-template.md coverage table is missing '{label}'")

# 10. scripts, IDs, test bench
SCRIPTS = SK / "scripts"
for s in ["inventory.py", "sweep.py", "coverage.py", "version_check.py", "versions.py", "profile.py"]:
    if not (SCRIPTS / s).exists(): err(f"skills/vibe-check/scripts/{s} is missing")
    else:
        try: compile((SCRIPTS / s).read_text(), s, "exec")
        except SyntaxError as e: err(f"scripts/{s} doesn't compile: {e}")
# 11. privacy: only version_check.py may use the network, and only to read two fixed GitHub URLs
NET = re.compile(r"^\s*(?:import|from)\s+(urllib|socket|http|requests|httpx|aiohttp|ftplib|smtplib)\b", re.M)
for s in ["inventory.py", "sweep.py", "coverage.py", "versions.py", "profile.py"]:
    src = (SCRIPTS / s).read_text() if (SCRIPTS / s).exists() else ""
    if NET.search(src): err(f"scripts/{s} imports a network module: only version_check.py may use the network")
    for cmd in re.findall(r"subprocess\.(?:run|Popen|call|check_output)\(\s*\[\s*\"([^\"]+)\"", src):
        if cmd != "git": err(f"scripts/{s} runs '{cmd}': helper scripts may only run read-only git commands")
vc = (SCRIPTS / "version_check.py").read_text() if (SCRIPTS / "version_check.py").exists() else ""
allowed = {"https://api.github.com/repos/vikneshchandrasekaran21/Vibe-check/releases/latest",
           "https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest",  # shown to the user, never fetched
           "https://raw.githubusercontent.com/vikneshchandrasekaran21/Vibe-check/main/skills/vibe-check/SKILL.md"}
for url in set(re.findall(r"https?://[^\s\"')]+", vc)):
    if url not in allowed: err(f"version_check.py contains a URL outside the two allowed GitHub URLs: {url}")
for bad, why in [(r"\bdata\s*=", "sends a request body"), (r"method\s*=", "uses a non-GET method"),
                 (r"\bsubprocess\b|\bsocket\b", "uses subprocess or raw sockets"), (r"os\.walk|glob\(|rglob\(", "reads project files"),
                 (r"os\.environ\b(?!\.get\(var)", "reads environment variables other than the opt-out")]:
    if re.search(bad, vc): err(f"version_check.py {why}: it may only GET the latest version and send nothing")
if re.search(r"get\(\s*RELEASES_PAGE", vc): err("version_check.py fetches the releases page: it may only be shown, never fetched")
for must in ["VIBE_CHECK_NO_UPDATE_CHECK", "update_check", "timeout=TIMEOUT", "TIMEOUT = 3"]:
    if must not in vc: err(f"version_check.py is missing '{must}'")
for must in ["## Step 0: Version check", "scripts/version_check.py", "VIBE_CHECK_NO_UPDATE_CHECK", "carry on",
             "Never send the user's code or data anywhere", "Never retry", "curl -s --max-time 3",
             "https://raw.githubusercontent.com/vikneshchandrasekaran21/Vibe-check/main/skills/vibe-check/SKILL.md",
             "couldn't connect", "npx skills update", "Lovable", "Claude app", "adapters/", "dist/vibe-check.md"]:
    if must not in skill: err(f"SKILL.md is missing '{must}' (version check / privacy rule)")
for must in ["v<installed>", "A newer vibe-check is out", "Update check:** couldn't connect here", "releases/latest", "update step for this tool"]:
    if must not in tpl: err(f"report-template.md is missing '{must}' (version line / update notice)")
rel = (ROOT / "scripts" / "release.sh").read_text() if (ROOT / "scripts" / "release.sh").exists() else ""
for must in ["skills/vibe-check/SKILL.md", 'gh release create "v$V"', "CHANGELOG.md", "scripts/validate.py"]:
    if must not in rel: err(f"scripts/release.sh is missing '{must}' (release tag must come from SKILL.md)")

# 12. known vulnerabilities and sweep patterns stay wired to real checks
import importlib.util as _u
_spec = _u.spec_from_file_location("vc_sweep_v", SCRIPTS / "sweep.py")
_mod = _u.module_from_spec(_spec); _spec.loader.exec_module(_mod)
bs_ids = {f"BS-{n:02d}" for n in nums}
for pid, cid, *_ in _mod.PATTERNS:
    if cid not in all_ids and cid not in bs_ids:
        err(f"sweep.py pattern {pid} points at {cid}, which isn't a check ID")
sweep_src = (SCRIPTS / "sweep.py").read_text()
for extra, cid in [("ENV-TRACKED", "SEC-022"), ("DOCKER-ROOT", "OPS-041")]:
    if extra not in sweep_src: err(f"sweep.py lost the {extra} file check")
    elif cid not in all_ids: err(f"sweep.py {extra} points at {cid}, which isn't a check ID")
n_patterns = len(_mod.PATTERNS) + 2
for must in ["scripts/versions.py", ".vibe-check/versions.md", "V-", "CURRENT", "OUTDATED", "EOL", "VULNERABLE", "references/vulnerabilities.md"]:
    if must not in skill: err(f"SKILL.md is missing '{must}' (known vulnerabilities)")
vul = (REFS / "vulnerabilities.md").read_text() if (REFS / "vulnerabilities.md").exists() else ""
for must in ["Never from memory", "CISA", "endoflife.date", "Never paste the user's dependency list", "composer audit", "osv-scanner", "trivy"]:
    if must not in vul: err(f"references/vulnerabilities.md is missing '{must}'")
for must in ["Known vulnerabilities", "versions.py", "actively exploited"]:
    if must not in tpl: err(f"report-template.md is missing '{must}' (known vulnerabilities table)")

# 13. the skill can't be mistaken for a design review, and works when only SKILL.md is available
desc = re.search(r"^description:\s*(.+)$", skill, re.M)
fm = skill.split("---", 2)[1] if skill.startswith("---") else ""
for line in fm.splitlines():
    m = re.match(r"^\s*[\w-]+:\s+(.+)$", line)
    if m and not m.group(1).startswith(("'", '"', "|", ">")) and (": " in m.group(1) or " #" in m.group(1)):
        err(f"SKILL.md frontmatter: unquoted value contains ': ' or ' #', which breaks YAML parsers: {line.strip()[:60]}")
try:
    import yaml  # optional: a real parse when PyYAML is installed
    yaml.safe_load(fm)
except ImportError:
    pass
except Exception as e:
    err(f"SKILL.md frontmatter isn't valid YAML: {e}")
if not desc or "Not a design review" not in desc.group(1): err("SKILL.md description must say 'Not a design review'")
for must in ["Running vibe-check v<version>", "## Step 0a: Make sure you have the whole skill", "Never download and run scripts",
             "https://raw.githubusercontent.com/vikneshchandrasekaran21/Vibe-check/v<version>/skills/vibe-check/references/",
             "never a look at the preview", "Never replace the audit with a design or screenshot review"]:
    if must not in skill: err(f"SKILL.md is missing '{must}' (start line / whole-skill check)")
import os as _os
for _d, _, _fs in _os.walk(ROOT / "adapters"):
    for _fn in _fs:
        _t = (Path(_d) / _fn).read_text()
        if not _t.startswith("---"):
            continue
        for line in _t.split("---", 2)[1].splitlines():
            m = re.match(r"^\s*[\w-]+:\s+(.+)$", line)
            if m and not m.group(1).startswith(("'", '"', "|", ">")) and (": " in m.group(1) or " #" in m.group(1)):
                err(f"{Path(_d, _fn).relative_to(ROOT)}: unquoted header value with ': ' or ' #' breaks YAML: {line.strip()[:50]}")
        try:
            import yaml
            yaml.safe_load(_t.split("---", 2)[1])
        except ImportError:
            pass
        except Exception as e:
            err(f"{Path(_d, _fn).relative_to(ROOT)}: header isn't valid YAML: {e}")
if "Skill files:" not in tpl: err("report-template.md header is missing 'Skill files:'")
if "--cleanup-tag" in rel: err("release.sh must not delete tags: older installs read their checklists from their version tag")

# 14. exactly one skill in the repo (a stray local install would be picked up by installers)
import subprocess as _sp
_skills = []
for _d, _dirs, _fs in _os.walk(ROOT):
    _dirs[:] = [x for x in _dirs if x not in (".git", "node_modules", "__pycache__")]
    if "SKILL.md" in _fs:
        _skills.append(Path(_d, "SKILL.md").relative_to(ROOT).as_posix())
if _skills != ["skills/vibe-check/SKILL.md"]:
    err(f"the repo must contain exactly one SKILL.md (skills/vibe-check/SKILL.md), found: {_skills}. "
        "Delete local installs like .agents/ (they're gitignored)")
_gi = (ROOT / ".gitignore").read_text() if (ROOT / ".gitignore").exists() else ""
for _must in [".agents/", "skills-lock.json", ".vibe-check/"]:
    if _must not in _gi: err(f".gitignore must include {_must}")
if "git rm -r -q --cached --ignore-unmatch .agents" not in rel: err("release.sh must untrack local skill installs before committing")

# 15. hunt mode: method, safety rules, report section, benchmark
hunt = (REFS / "hunt.md").read_text() if (REFS / "hunt.md").exists() else ""
for must in ["Only the user's own app", "No working exploits", ".vibe-check/proofs/", "report it privately", "## Threat model",
             "PROVEN NEW", "DISPROVEN", "UNTESTED", "at least 12 hypotheses", "at least 25"]:
    if must not in hunt: err(f"references/hunt.md is missing '{must}'")
for must in ["## Step 4a: Hunt", "references/hunt.md", "Found by hunting"]:
    if must not in skill: err(f"SKILL.md is missing '{must}' (hunt mode)")
for must in ["🎯 Hunt", "found by hunting"]:
    if must.lower() not in tpl.lower(): err(f"report-template.md is missing '{must}' (hunt section)")
for f in ["bench/hunt-app/server.js", "bench/hunt-answers.json", "bench/score.py", "bench/README.md"]:
    if not (ROOT / f).exists(): err(f"{f} is missing (hunt benchmark)")
if (ROOT / "bench" / "hunt-app" / "hunt-answers.json").exists() or any(p.name.endswith("answers.json") for p in (ROOT / "bench" / "hunt-app").rglob("*")):
    err("the hunt answer key must stay outside bench/hunt-app/")
if ".vibe-check/proofs" not in skill: err("SKILL.md must say hunt proofs go in .vibe-check/proofs")

# 16. standards mapping: complete, real check IDs, known item counts
std_text = (REFS / "standards.md").read_text() if (REFS / "standards.md").exists() else ""
expected = {"OWASP Top 10:2025": 10, "OWASP API Security Top 10 (2023)": 10, "OWASP Top 10 for LLM Applications (2025)": 10,
            "OWASP Mobile Top 10 (2024)": 10, "OWASP ASVS 5.0.0 (by chapter)": 17, "2025 CWE Top 25": 25}
sections = {}
cur = None
for line in std_text.splitlines():
    if line.startswith("## "):
        cur = line[3:].strip(); sections[cur] = []
    elif cur and line.startswith("|"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 3 and cells[0] != "ID" and not set(cells[0]) <= set("-: "):
            sections[cur].append(cells)
for title, n in expected.items():
    items = sections.get(title)
    if items is None:
        err(f"standards.md is missing the section '{title}'"); continue
    if len(items) != n: err(f"standards.md '{title}' has {len(items)} items, expected {n}")
    seen = set()
    for iid, name, mapped in items:
        if iid in seen: err(f"standards.md '{title}': duplicate item {iid}")
        seen.add(iid)
        ids = re.findall(r"\b(?:BS-\d{2}|[A-Z]+-\d{3})\b", mapped)
        if not ids: err(f"standards.md {iid}: maps to no vibe-check check")
        for cid in ids:
            if cid not in all_ids and cid not in bs_ids: err(f"standards.md {iid} maps to {cid}, which isn't a check ID")
for must in ["not a certification", "CC BY-SA", "Human"]:
    if must not in std_text: err(f"standards.md is missing '{must}'")
for must in ["references/standards.md", "references/live-tests.md", "Only a human can confirm", "When to run vibe-check again", "never production"]:
    if must not in skill: err(f"SKILL.md is missing '{must}' (v3.0)")
for must in ["📏 Standards", "not a certification", "Only a human can confirm", "When to run vibe-check again"]:
    if must not in tpl: err(f"report-template.md is missing '{must}' (v3.0)")
live = (REFS / "live-tests.md").read_text() if (REFS / "live-tests.md").exists() else ""
for must in ["never against production", "user's OK", "two test accounts", "zap-baseline.py", "nuclei", "exclude intrusive"]:
    if must not in live: err(f"live-tests.md is missing '{must}' (safety)")

# 17. v3.1: the code decides the profile, evidence is re-opened, re-check, receipt, fix everything
for must in ["scripts/profile.py", "never remove what the code shows", "DEAD CODE:", "Your answers vs your code",
             "ledger.d", "coverage.py --sample", "R-001", "--verify-report", "REPORT VERIFIED", "--fix-plan",
             "### Fix everything", "fresh helper that didn't do the audit", "DRAFT: needs legal review"]:
    if must not in skill: err(f"SKILL.md is missing '{must}' (v3.1)")
for must in ["Your answers vs your code", "Checked twice", "--verify-report"]:
    if must not in tpl: err(f"report-template.md is missing '{must}' (v3.1)")
cov_src2 = (SCRIPTS / "coverage.py").read_text()
for must in ["def check_evidence", "def sample_ids", "--verify-report", "--fix-plan", "ledger.d", "modules_with_evidence", "DEAD CODE:"]:
    if must not in cov_src2: err(f"coverage.py is missing '{must}' (v3.1)")
prof_src = (SCRIPTS / "profile.py").read_text() if (SCRIPTS / "profile.py").exists() else ""
for mod in ["kids-education", "fintech", "health", "ai-features", "ai-agents", "community", "mobile", "desktop-extensions", "cloud-infra", "i18n"]:
    if f'"{mod}"' not in prof_src: err(f"profile.py has no signals for the {mod} module")
    elif mod not in {f.replace(".md", "") for f in ref_files}: err(f"profile.py names {mod}, which isn't a module file")
if "LEG-036" not in all_ids: err("legal-privacy.md lost LEG-036 (real audience assessed from evidence)")

core_tbl = skill.split("**Core modules**", 1)[1].split("**Profile modules**", 1)[0] if "**Core modules**" in skill else ""
core_files = re.findall(r"`references/([a-z0-9-]+)\.md`", core_tbl)
cov_src = (SCRIPTS / "coverage.py").read_text() if (SCRIPTS / "coverage.py").exists() else ""
cov_core = re.findall(r'"([a-z-]+)"', cov_src.split("CORE = [", 1)[1].split("]", 1)[0]) if "CORE = [" in cov_src else []
if sorted(core_files) != sorted(cov_core): err(f"coverage.py CORE {sorted(cov_core)} doesn't match SKILL.md core modules {sorted(core_files)}")
tb = subprocess.run([sys.executable, str(ROOT / "tests" / "test_scripts.py")], capture_output=True, text=True)
if tb.returncode: err("test bench failed:\n" + tb.stdout[-1500:] + tb.stderr[-500:])

# 8. README
readme = (ROOT / "README.md").read_text()
n_modules = len(ref_files - support) + 1  # + blind spots
for claim, real in [(r"(\d+) AI blind[- ]spot", len(nums)), (r"for (\d+) risky patterns", n_patterns), (r"in (\d+) modules", n_modules)]:
    for m in re.finditer(claim, readme):
        if int(m.group(1)) != real: err(f"README.md says '{m.group(0)}' but the real number is {real}")
for must in ["npx skills update", "VIBE_CHECK_NO_UPDATE_CHECK", "## 🔄 Updating", "-a replit", "/vibe-check run the full audit", "Running vibe-check v",
             "https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check"]:
    if must not in readme: err(f"README.md is missing '{must}' (updating / version check)")
if re.search(r"phone home|nothing (?:is )?sent anywhere", readme, re.I) and "version check" not in readme.lower():
    err("README.md promises it never contacts anything, but doesn't mention the version check")

for f in sorted(ref_files) + ["inventory.py", "sweep.py", "coverage.py", "version_check.py", "versions.py", "profile.py", "test_scripts.py", "release.sh"]:
    if f not in readme: err(f"README.md repo layout doesn't list {f}")
for link in re.findall(r"\]\((?!https?://|#|mailto:)([^)]+)\)", readme):
    if not (ROOT / link.split("#")[0]).exists(): err(f"README.md links to missing file: {link}")

# 9. generated outputs
r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build.py"), "--check"], capture_output=True, text=True)
if r.returncode: err("generated files are out of date:\n" + r.stdout)
dist = (ROOT / "dist" / "vibe-check.md").read_text()
for f in ref_files:
    title = (REFS / f).read_text().splitlines()[0].lstrip("# ").strip()
    if title not in dist: err(f"dist/vibe-check.md is missing module '{title}'")
with zipfile.ZipFile(ROOT / "dist" / "vibe-check.zip") as z:
    zn = set(z.namelist())
    for f in ref_files | {"SKILL.md"} | {"scripts/" + s.name for s in SCRIPTS.glob("*.py")}:
        p = f"vibe-check/{f}" if f == "SKILL.md" or f.startswith("scripts/") else f"vibe-check/references/{f}"
        if p not in zn: err(f"dist/vibe-check.zip is missing {p}")
if tomllib is None:
    warn("Python < 3.11 without tomli: skipped the Gemini TOML parse check (CI runs it)")
else:
    try:
        tomllib.loads((ROOT / "adapters/gemini/.gemini/commands/vibe-check.toml").read_text())
    except Exception as e:
        err(f"Gemini TOML doesn't parse: {e}")

print(f"Modules: {len(ref_files - support)} · checks: {total} (🔴 {blockers}) · IDs: {len(all_ids)} · blind spots: {len(nums)}")
for w in warnings: print("warning:", w)
for e in errors: print("ERROR:", e)
print("OK: skill is complete and consistent." if not errors else f"{len(errors)} error(s).")
sys.exit(1 if errors else 0)
