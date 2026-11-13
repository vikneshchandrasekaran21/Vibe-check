# Changelog

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
