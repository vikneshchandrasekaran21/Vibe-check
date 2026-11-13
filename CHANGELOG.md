# Changelog

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
