# Changelog

## v2.8.1 (2026-11-14)

**Can't be mistaken for a design review.**
- **A first line on every run:** `Running vibe-check v<version> · <level> check`, so you can see the skill loaded. A run that only reviews the preview isn't vibe-check.
- **Step 0a, "Make sure you have the whole skill":** if a tool hands the agent only SKILL.md (for example a Replit workspace import), the agent says so, reads the checklists from this repo **at the exact installed version tag** (a plain read, nothing sent), does the script steps by hand (it never downloads and runs scripts), and gives the one-line project install for the full audit. It never falls back to a screenshot review. The report header records which way it ran.
- **A clearer description** for agents choosing a skill: *"Full code audit… Not a design review."*
- **README:** call it with `/vibe-check` in Replit and Lovable, prefer the project install for full audits, and how to tell it's really running.
- Ground rule 13 now names both public GitHub reads (the version check and missing checklists).
- **Fixed:** the Cursor rule file's header had an unquoted `:` that strict YAML parsers reject (an older bug). All generated headers are now quoted, and the validator parses every header with a real YAML parser.
- **`release.sh` keeps old tags** (it still removes old release pages), so older installs can always read their own checklists from their version tag.

## v2.8.0 (2026-11-14)

**Known vulnerabilities, and the checks developers and testers miss.**
- **New core module `vulnerabilities.md` (15 checks, `VUL-`):** every component the app runs is checked against **today's** security releases and advisories: the runtime (PHP, Node, Python, Ruby, Go, Java, .NET), framework, CMS **and each plugin or theme**, packages in every ecosystem, web server, Docker image, database engine and mobile SDK. It also covers end-of-life software, CISA's actively-exploited (KEV) list, which production version is really running, official workarounds when an upgrade can't happen today, version disclosure, and staying patched. It includes an audit tool for each ecosystem (npm, Composer, pip, Bundler, Go, Cargo, Maven/Gradle, .NET, Docker, WordPress) and a severity table.
- **`scripts/versions.py`** lists everything the app runs with exact versions, from lockfiles, `composer.json`, `.nvmrc`/`.python-version`/`.tool-versions`, Dockerfiles and compose files, WordPress core, plugins and themes, Gradle/Podfile SDK targets and Workers compatibility dates. Each component needs a ledger verdict (`CURRENT`, `OUTDATED`, `EOL`, `VULNERABLE`, `CAN'T TELL`) with the source URL opened during the run or the audit tool that checked it. `coverage.py` enforces it, so no version is judged from memory.
- **18 new security checks for what's often missed (SEC-065 to SEC-082):** template injection, XXE, prototype pollution, header/CRLF injection, **Host-header poisoning of reset links**, cache poisoning and deception and request smuggling, **re-authentication for email and password changes**, constant-time comparisons, Unicode-normalized identifiers, GraphQL lockdown, object- and function-level access on every API endpoint (BOLA/BFLA), WebSocket auth, zip slip, file processors (SVG, PDF renderers, image libraries), **exposed `/.git`, `.env` and backups**, default credentials and open admin tools, **subdomain takeover**, and static analysis (Semgrep, CodeQL…).
- **Container checks (OPS-041 to OPS-043):** non-root user, no secrets in image layers, slim pinned images.
- **New blind spot BS-19, "Versions from training data":** AI tools pin the versions they remember.
- **The sweep goes from 37 to 51 patterns:** template injection, XXE, prototype pollution, header injection, Host-header use, timing-unsafe secret comparisons, open GraphQL, archive extraction, unsafe PHP (`unserialize`/`extract`/`include` on request data), `phpinfo()`, version disclosure, secrets in Docker `ENV`/`ARG`, default passwords, and containers running as root.
- **The validator checks** that every sweep pattern points at a real check ID, and that the README's numbers (blind spots, patterns, modules) match reality.

## v2.7.2 (2026-11-14)

**Update notices everywhere.**
- **Replit and Lovable install as skills:** Replit with `npx skills add … -a replit` (scripts included), Lovable by importing `…/tree/main/skills/vibe-check` from GitHub. Bolt, v0 and ChatGPT stay paste-in.
- **Step 0 works without the script:** single-file versions and builders read the version line from GitHub with the tool's own web fetch or one `curl -s --max-time 3`. Still only that one URL, still sending nothing.
- **When the check can't connect** (offline, or Codex's default sandbox), the report says so with the latest-release link, instead of saying nothing.
- **Update steps for each tool** are in the skill, so the notice tells people exactly what to do in Claude Code, Codex, Cursor, Replit, Lovable, the Claude app, copied files and paste-in.
- The README recommends `npx skills add` over copying files wherever a tool supports it, for the scripts and one-command updates.

## v2.7.1 (2026-11-14)

**Know when to update.**
- **Version check (Step 0):** `scripts/version_check.py` reads the latest release number from GitHub, then the report says *"A newer vibe-check is out"* with the update command. It sends nothing about the user, gives up after 3 seconds, never blocks the audit, and can be turned off (`VIBE_CHECK_NO_UPDATE_CHECK=1` or `update_check: false` in `.vibe-check/config`).
- **The version is shown in every report:** in the header and the footer, with the update command.
- **New ground rule 13:** never send the user's code or data anywhere. The validator enforces it: only `version_check.py` may use the network, only to read two fixed GitHub URLs, and only with plain GET requests that carry no data.
- **README "🔄 Updating" section:** how to update for each install method, plus *Watch → Releases* for email notices.
- **`scripts/release.sh`:** one command to publish. The release tag always comes from SKILL.md, so the version check and GitHub can't disagree.
- **Fixed:** the build check compares the files inside the zip, not its bytes, so it passes on both Mac and Linux.
- The test bench adds 6 version-check cases: update available, up to date, older, opted out by env, opted out by config, and offline.

## v2.7.0 (2026-11-13)

**Depth: built not to skip anything.**
- **Permanent check IDs** on all 587 checks (`SEC-001`, `LAW-002`…) and the 18 blind spots (`BS-01`…).
- **The ledger** (`.vibe-check/ledger.md`): one row per check with its result and evidence, written module by module as the audit goes. It saves progress so long audits can resume.
- **`scripts/inventory.py`** lists everything in the app before checking: pages, API routes, server actions, functions, webhooks, cron, admin areas, forms, buttons and links, env vars (flagging browser-public ones), tables, buckets, uploads, payments, email, AI calls and third-party scripts. The report shows checked/found for each.
- **`scripts/sweep.py`** searches every file, and the git history, for 37 risky patterns, with secrets masked. Every hit needs a verdict (FINDING or RULED OUT).
- **`scripts/coverage.py`** counts the ledger against the checklist. It fails on missing checks, invented IDs, vague or copy-pasted evidence, FAILs without a confidence label, unreviewed sweep hits and unaccounted inventory. The report's coverage table and score line are pasted from its output.
- **One module at a time:** each module file is re-read just before it is checked, never from memory.
- **Tools run table:** package audit, type-check, lint, tests, build and secret scanners are always tried, and every result is recorded, including "not installed".
- **Test bench** (`tests/test_scripts.py`): a small app with 18 planted problems. The scripts must catch every one, with no false alarms in a clean file, and `coverage.py` must reject 11 kinds of sloppy ledger. It runs in CI through the validator.
- **The validator** now checks IDs (unique, one prefix per module), the scripts, and the new rules in SKILL.md, the self-check and the report template.

## v2.6.0 (2026-11-13)

**Accuracy: built not to make things up.**
- **Quote the proof:** every finding quotes the exact code lines (re-read just before reporting, so line numbers are current) or the exact command output. A finding that can't be quoted is dropped or becomes a question.
- **New Step 4b, the second look:**
  - Every 🔴 and 🟡 is re-checked by trying to prove it wrong.
  - The common false-alarm causes it checks: handled in middleware or RLS, dead or dev-only code, public-by-design keys, framework defaults, not reading the whole function.
  - Each blocker says what was ruled out.
- **Confidence labels:** ✅ Confirmed, 🔎 Likely, ❓ Needs checking. Only Confirmed and Likely can be blockers. ❓ goes to Questions.
- **No facts from memory:** legal, regulatory, store-policy and pricing statements must come from the skill's modules or a source opened during the run, with its URL.
- **Passes need evidence too.**
- **The self-check and the validator** now enforce all of the above.

## v2.5.0 (2026-11-13)

**Nine new modules.** The profile now also asks what kind of product it is (web, mobile, desktop, extension, API), whether users interact or trade, which languages it supports, whether AI agents take actions, and which cloud it runs on.

**New core modules (run for every Full check):**
- **⚖️ Lawsuit magnets & jurisdictions:**
  - The checks are traps that can be detected in the code and that people actually get sued or sent demand letters over.
  - Fonts and trackers: self-host fonts instead of loading them from Google, keep pixels, session replay, chat widgets and embeds off until consent, and mask chat and replay inputs.
  - Accessibility: ADA on revenue paths, and no overlay widgets used instead of real fixes.
  - Money and marketing: auto-renewal and click-to-cancel, marketing opt-in, no fake urgency or hidden fees, fair cookie banners with GPC.
  - Regional basics: Impressum, Quebec French, biometrics, video data sent to pixels.
  - A country table: EU, DACH, UK, US, Canada, India, Brazil, Australia, Asia and the app stores.
- **🔗 Supply chain & CI:**
  - Dependencies: lockfiles, typosquats, install scripts, dependency confusion.
  - CI: GitHub Actions pinned to SHAs, safe triggers, token permissions, no secrets in logs.
  - Browser: third-party scripts, SRI and tag managers.
  - Repository: secret scanning, CODEOWNERS and SBOM.
- **🧹 Maintainability & handover:**
  - Code health: types, linting, dead and duplicated code.
  - Docs: README and `.env.example`, architecture notes, AI rules files.
  - Ownership: who owns every account, credentials in a vault, a due-diligence pack.

**New profile modules (run when they apply):**
- **📱 Mobile:** account deletion, permission strings, privacy labels and manifest, server-side purchase checks, App Tracking Transparency, SDK targets, secure storage, cleartext traffic, deep links, WebViews, crash reporting, forced updates, device testing.
- **👥 Community & marketplace:** reporting, blocking, moderation and filtering, minors, appeals, realtime authorization, message limits, takedown and CSAM duties, DSA / Online Safety Act / IT Rules, seller verification, disputes, fake reviews.
- **☁️ Cloud infrastructure:** public buckets, IAM wildcards and keys, root account, open ports, TLS, SSH, container security, secrets in images, IaC scanning, state files, cost controls.
- **🖥️ Desktop & browser extensions:** Electron isolation and preload bridges, code signing and notarization, signed auto-update, Tauri allow-lists, extension permissions, Manifest V3, content script trust, store disclosures.
- **🌍 Internationalisation:** missing translations, legal text per language, plurals, non-Latin scripts, RTL, text length, currency and number formats, phone and address formats, local payment methods.
- **🤖 AI agents & MCP:** least-privilege tools, acting as the user, confirmation for risky actions, indirect prompt injection, exfiltration, sandboxing, loop and cost limits, audit log, kill switch, MCP authentication, honest tool descriptions.

**Also changed:** the mobile checks moved out of the UX module into the new mobile module.

## v2.4.0 (2026-11-13)

- **🔐 Encryption:** at rest, in transit and per field are now 🔴 for apps with children's, health, financial or ID data.
- **🕳️ New "Data leakage" section (10 checks):**
  - APIs returning hidden fields, account enumeration, private pages cached for others
  - tokens in URLs and referrers, guessable share links
  - data sent to analytics, session replay and error tracking
  - internals in client bundles
  - exports (including CSV formula injection), sensitive email subjects
  - deleted data that isn't really gone
- **📈 New "Load and stress" section (8 checks):** load, spike, data-volume, concurrency and soak tests, graceful overload and platform limits. **Never against production.** Only staging or local, with approval and paid APIs mocked.
- **🖱️ General QA, 3 new sections (19 checks):**
  - **Messages and microcopy:** clear error messages, success confirmations, delete confirmations with undo, payment result screens, consistent wording, typos, empty states, toasts.
  - **Edge cases:** money rounding, unusual text (emoji, Hindi and Tamil, apostrophes), time zones and DST, list edges, limits, file edges.
  - **Sessions and journeys:** a smoke test of every journey for every role, session expiry mid-task, multiple tabs and devices, role changes taking effect, notifications per journey.
- **🛠️ Fix playbook:** new recipes for over-sharing APIs, account enumeration and private data in shared caches.

## v2.3.0 (2026-11-13)

From a real full run on a live app, where DevOps coverage was thin and parts of the report format were skipped.

- **New core module: ⚙️ DevOps & operations** (40 checks):
  - CI on every push, protected main, Dependabot
  - separate environments, automated deploys and rollback, platform default domains
  - error alerts that reach a human, uptime and **cron monitoring**, third-party outage handling
  - logs without personal data
  - backups with a tested restore, disaster recovery
  - MFA everywhere, secret rotation, bus factor
  - billing alerts, domain and SSL expiry, email that actually sends, incident runbook
- **The reliability module is now "Data, reliability & testing":** infrastructure moved to DevOps. It adds scheduled cleanup jobs and payment **replay tests**.
- **🧭 Coverage table in every report:** each module marked ✅ checked / ◐ partly / ❌ not checked / ➖ not applicable, with counts and method, so you can see exactly what was checked.
- **"Before you reply" self-check:** the agent confirms coverage, evidence, fix prompts, safe-to-fix marks, the saved report and the score card before answering.
- **Fresh evidence every run:** findings from earlier runs are re-checked and marked still open, fixed or new, never copied forward. A new level starts every step from the beginning.
- **Check everything that applies, item by item.** No sampling. Unfinished modules must be shown as unfinished.
- **`scripts/validate.py`:** an automated check that every module is wired into the skill, build, zip, adapters and README, that every check has a severity and a name, and that there are no duplicates. It runs in CI.

## v2.2.0 (2026-11-13)

- **The full check is now always the default.** "vibe check this app" runs everything that applies. Quick runs only when you say "quick", and it ends by suggesting the full check.
- Levels renamed for clarity: 🟢 Quick, 🟡 **Full** (was "Launch"), 🔵 Enterprise. "Launch" still works.
- **Simpler install:** one copy-paste command per tool, with no menus (`-a <agent> -y`), plus clear update steps.

## v2.1.0 (2026-11-13)

- **🏁 Score card:** every report ends with a one-line, screenshot-friendly score (`vibe-check: 🟢 SHIP · 112/118 checks · 0 blockers · Launch level · date`), including the change since the last report.
- **"vibe-checked" badge** offered for README files when an app reaches 🟢 at Launch level or above (never added without asking).
- A small, removable "Checked with vibe-check" footer on saved reports (never added to the app).
- A one-time ⭐ request, shown only on 🟢 reports.

## v2.0.0 (2026-11-13)

**One skill that adapts to your app.**

- **Profiles and levels:** the skill works out who uses the app (minors? payments? health data? which countries?) and asks only what it can't tell from the code. Then it runs at 🟢 Quick, 🟡 Launch (default) or 🔵 Enterprise depth.
- **6 new modules:**
  - **Functional QA:** dead buttons and links, forms that don't save, missing states, placeholder content, console errors.
  - **Kids & education:** verifiable parental consent, data minimization, retention limits for minors' data, photo GPS stripping, no trackers.
  - **Policy pack:** 16 documents, when each is needed and what it must contain.
  - **Enterprise & government:** SSO/SCIM, audit logs, data residency, RPO/RTO, pentest, SBOM, SOC 2/ISO readiness.
  - **Health:** explicit consent, no health data in analytics, BAAs/DPAs, medical-device questions.
  - **Fintech:** PCI scope, ledgers, atomic transfers, reconciliation, licensing questions.
- **Deeper checks:**
  - Web-font and image licensing, with an asset register.
  - Cloudflare (minimum TLS version, `workers.dev`, R2).
  - "Does email actually send?" as an AI blind spot.
  - Platform default domains (`*.workers.dev`, `*.vercel.app` and so on).
- **"Fix the safe items":** applies invisible, easy-to-undo fixes in one go. Everything else waits for approval.
- **Reports saved in your project** (`.vibe-check/reports/`, kept out of git), so later sessions can continue fixing.
- **Fallbacks when a tool is blocked or missing:** licence scans read the lockfile, and click-through QA traces handlers in the code.
- **Better evidence:** dependency findings include the advisory ID and the version that fixes them. Anything skipped is listed with the command to run it.
- **Pro-ready:** uses the vibe-check connector's tools when connected, and local checks otherwise.
- **Claude app support:** upload `vibe-check.zip` from the release.
- Now 18 AI blind spots plus 360+ checks across 13 modules.

## v1.0.0 (2026-11-13)

- First release: an audit across security, data and reliability, AI features, legal and privacy, UX and platform traps, with a fix playbook.
- The scope guard: never change what the user built.
- Adapters for Cursor, Copilot, Windsurf, Cline, Gemini CLI and `AGENTS.md`, plus a single-file version for paste-in tools.
