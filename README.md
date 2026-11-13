<div align="center">

# ✅ vibe-check

### The pre-launch audit for AI-built apps

Before you ship, have your AI coding agent find and fix what it usually misses, without changing what you built.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-blue.svg)](https://agentskills.io)
[![check](https://github.com/vikneshchandrasekaran21/vibe-check/actions/workflows/check.yml/badge.svg)](https://github.com/vikneshchandrasekaran21/vibe-check/actions/workflows/check.yml)

```bash
npx skills add vikneshchandrasekaran21/vibe-check
```

Works with **Claude Code · Codex · Cursor · GitHub Copilot · Gemini CLI · Windsurf · Cline · Roo · Goose · OpenCode · Amp · Junie · Kiro**, plus **Lovable · Bolt · v0 · Replit · ChatGPT** by copy-paste.

</div>

---

## Why

AI coding tools are great at writing code that **works in the demo**. They often miss what only shows up with **real users, real attackers and real money**:

- 🔓 Any logged-in user can open someone else's data by changing an ID in the URL
- 🗝️ Database rules left open (Supabase RLS off, Firebase in test mode) or secret keys sitting in the browser
- 💸 Orders marked "paid" from a redirect page, prices taken from the browser, no spending cap on the AI API
- 🖱️ Buttons that do nothing, links to pages that don't exist, forms that never save
- 📧 Password-reset and verification emails that never arrive
- 🧒 Students' or children's data collected with a tick-box "consent" and kept forever
- 🔤 Paid fonts and stock images used without a web licence
- 🧯 No timeouts, no backups, no CI, no error tracking. You find out it's broken from an angry user
- ⚖️ A copy-pasted privacy policy that doesn't match the app, and analytics that run before cookie consent

`vibe-check` is an open **[Agent Skill](https://agentskills.io)**. It turns your coding agent into a strict pre-launch reviewer that **finds** these problems, **explains** them in plain words and **fixes** the ones you approve, while leaving your design, features and use case alone.

It works like a senior team in one command, covering what security, QA, legal and DevOps would each check. It asks a few questions about your app (who uses it, whether there are minors, payments or sensitive data) and runs only the checks that apply, at three depths: 🟢 **Quick**, 🟡 **Launch** and 🔵 **Enterprise**.

## What you get

| | |
|---|---|
| 🔍 **Audit** | **18 AI blind-spot checks** plus **360+ checks** in 13 modules. It asks a few questions about your app and runs only the modules that apply |
| 📋 **Report** | A clear verdict (**🟢 SHIP / 🟡 SHIP AFTER FIXES / 🔴 DO NOT SHIP**), each problem in plain words with evidence (`file:line`), questions for you, and a "needs a lawyer" list |
| 🛠️ **Fixes** | A built-in **fix playbook** with proven patterns. **"Fix safe items"** applies the invisible, easy-to-undo fixes in one go, and everything else waits for your OK |
| 💾 **History** | Reports are saved in your project (`.vibe-check/reports/`, kept out of git), so the next session knows what was found and fixed |
| 🧑‍💻 **For everyone** | Written for non-developers too. Every finding comes with a **copy-paste prompt** you can give any AI tool to fix it |

## 🛡️ It won't change what you built

vibe-check fixes **only the issues it finds**. Your product stays your product:

- **Design, features, flows, copy and tech choices stay the same.** No redesigns, refactors, renames, reformatting or surprise upgrades.
- **Smallest possible change.** Fixes only change behaviour for attackers, bad input or failures. Your real users won't notice anything.
- **It asks before anything visible.** If a fix has to add something users will see (a cookie banner, a "Delete account" button, a CAPTCHA), the agent explains why and waits for your OK.
- **New pieces match your design.** Anything it adds uses your existing components, colours and tone.
- **No side quests.** Other ideas go under "Other suggestions (not changed)" and are never applied without asking.
- **Your data is safe.** It never deletes or rewrites existing user data, and database changes are tested on staging first.
- **Easy to review.** After each fix, it lists the files changed and what users will (or won't) notice.

It also **never changes code during the audit**, **never marks something as passed without evidence**, and **never prints your secrets in full**.

---

## Install

### Quick start: pick your tool

| You use… | Do this |
|---|---|
| **Claude app** (desktop or claude.ai) | [Download `vibe-check.zip`](https://github.com/vikneshchandrasekaran21/vibe-check/releases/latest/download/vibe-check.zip), then **Settings → Customize → Skills → Add → Upload skill** and pick the zip. Don't unzip it |
| **Claude Code, Codex, Cursor, Copilot, Gemini CLI** and other agents | In your Mac/PC terminal: `npx skills add vikneshchandrasekaran21/vibe-check`. Or just ask your agent to run that command for you |
| **Lovable, Bolt, v0, Replit, ChatGPT** | Copy [`dist/vibe-check.md`](dist/vibe-check.md) and paste it into the chat |

Then say **"vibe check this app"**. That's it. More options below.

### 1. One command (recommended for coding agents)

```bash
npx skills add vikneshchandrasekaran21/vibe-check        # this project
npx skills add vikneshchandrasekaran21/vibe-check -g     # all your projects
```

The [skills CLI](https://github.com/vercel-labs/skills) detects which agents you have installed and sets the skill up for each one.

### 2. Copy the folder

Copy [`skills/vibe-check/`](skills/vibe-check) into your agent's skills folder:

| Agent | This project | All projects |
|---|---|---|
| Claude Code | `.claude/skills/vibe-check/` | `~/.claude/skills/vibe-check/` |
| OpenAI Codex | `.agents/skills/vibe-check/` | `~/.codex/skills/vibe-check/` |
| GitHub Copilot | `.github/skills/vibe-check/` | `~/.copilot/skills/vibe-check/` |
| Cursor | `.cursor/skills/vibe-check/` | `~/.cursor/skills/vibe-check/` |
| Gemini CLI | `.gemini/skills/vibe-check/` | `~/.gemini/skills/vibe-check/` |
| Other Agent Skills tools | check your tool's docs (often `.agents/skills/`) | |

### 3. Tools that use rules or commands

Ready-made versions are in [`adapters/`](adapters). Copy the folder for your tool into your project root:

| Tool | Copy this | Then |
|---|---|---|
| Cursor (rules) | `adapters/cursor/.cursor/` | ask *"run vibe-check"* |
| GitHub Copilot (prompt file) | `adapters/copilot/.github/` | `/vibe-check` in Copilot Chat |
| Windsurf | `adapters/windsurf/.windsurf/` | `/vibe-check` |
| Cline / Roo | `adapters/cline/.clinerules/` | `/vibe-check.md` |
| Gemini CLI (command) | `adapters/gemini/.gemini/` | `/vibe-check` |
| Anything that reads `AGENTS.md` | the snippet in [`adapters/AGENTS.md`](adapters/AGENTS.md) | ask *"run vibe-check"* |

### 4. Claude app (desktop or claude.ai)

1. Download **[vibe-check.zip](https://github.com/vikneshchandrasekaran21/vibe-check/releases/latest/download/vibe-check.zip)** (it's also in [`dist/`](dist/vibe-check.zip)).
2. In Claude, open **Settings → Customize → Skills**.
3. Click **Add → Upload skill** and pick the zip. Keep it zipped.
4. Make sure the skill is switched on. Then in any chat or project, say *"vibe check this app"*, and attach your code or connect a folder so Claude can read it.

### 5. Lovable, Bolt, v0, Replit, ChatGPT

No install needed. Open [`dist/vibe-check.md`](dist/vibe-check.md), copy everything, paste it into the chat and add:

> Run this audit on my project. I'm not a developer, so explain each finding simply.

When the agent can't run commands, it reviews the code and config and tells you which commands to run yourself.

---

## Use

Just ask your agent:

| Say | What happens |
|---|---|
| *"quick vibe check"* | 🟢 **Quick:** the 18 AI blind spots plus every 🔴 blocker. Good before any deploy |
| *"vibe check this app"* · *"is this ready to ship?"* | 🟡 **Launch** (default): every module that applies to your app |
| *"enterprise vibe check"* | 🔵 **Enterprise:** Launch plus enterprise and government readiness and the full policy pack |
| *"fix the safe items"* | Applies only the fixes that are invisible to users and easy to undo |
| *"fix the vibe-check blockers"* · *"fix #1 and #3"* | Fixes only those issues, using the fix playbook and the scope guard |

### How it works

1. **Profile:** who uses the app, whether there are minors or students, money, sensitive data, regions. It works out what it can from the code and asks only what it can't.
2. **Map:** stack, data map (including things like photo GPS), entry points, database rules, env vars, live and platform default domains, known issues.
3. **Blind spots:** the 18 mistakes AI coding tools make most often.
4. **Modules:** the core modules plus only the profile modules that apply. It uses real tools where available (audit, secret and licence scanners, Playwright, Lighthouse), and falls back to reading the code when they're missing.
5. **Report:** saved to `.vibe-check/reports/` with a summary in chat. You get the verdict and score, blockers with a fix prompt, which items are safe to auto-fix, questions for you, a "needs a lawyer" list, what passed, and what wasn't checked.
6. **Fix (only what you approve):** prove the bug, apply a proven pattern, add a test, re-check, one issue per commit. For things only you can do (dashboard settings, rotating keys, legal decisions), it gives you exact steps.

### Example report

```text
Verdict: 🔴 DO NOT SHIP
Any logged-in user can read every other user's invoices, and the Stripe secret key
is in the browser bundle. Fix these two before launch; the rest can follow.

Score: 96 / 121 checks passed · 🔴 2 blockers · 🟡 9 to fix before scale · ❓ 5 questions

🔴 1. Users can see each other's invoices
   What could happen: anyone with an account can download every customer's invoices.
   Where: app/api/invoices/[id]/route.ts:14 (query filters by id only)
   Fix: scope the query to the logged-in user and return 404 otherwise.
   Prompt to fix it: "In app/api/invoices/[id]/route.ts, only return the invoice if
   invoice.userId equals the session user's id, else 404. Add a test proving user A
   can't fetch user B's invoice. Don't change anything else."
```

### 🏁 Show your score

Every report ends with a one-line **score card**, made to screenshot and share:

```text
vibe-check: 🟢 SHIP · 112/118 checks · 0 blockers · Launch level · 13 Nov 2026
```

Start at 🔴? Most people do. Fix, re-run, and post your 🔴 → 🟢 with **#vibecheck**.

If you reach 🟢 at Launch level or above, add the badge to your README:

```markdown
[![vibe-checked](https://img.shields.io/badge/vibe--checked-%E2%9C%85%20SHIP%20112%2F118-brightgreen)](https://github.com/vikneshchandrasekaran21/vibe-check)
```

[![vibe-checked](https://img.shields.io/badge/vibe--checked-%E2%9C%85%20SHIP%20112%2F118-brightgreen)](https://github.com/vikneshchandrasekaran21/vibe-check)

The report ends with a small "Checked with vibe-check" footer. Tell your agent *"no footer"* to remove it. It never adds anything to your app.

---

## What it checks

**Core modules** (always run at Launch level and above):

| Area | Highlights |
|---|---|
| 🧠 **AI blind spots** | Authorization and IDOR, RLS and Firebase rules, leaked secrets, mass assignment, prices from the client, unverified payments, missing timeouts, race conditions, invented or outdated packages, LLM spend caps, exposed admin and debug pages, unsafe AI features |
| 🔐 **Security & auth** | Sessions, cookies, JWTs, password reset and magic links, brute force, OAuth, roles, multi-tenancy, SQL, NoSQL, XSS and command injection, uploads, SSRF, open redirects, CORS, CSRF, headers, hashing vs encryption, dependencies, rate limits |
| 🗄️ **Data & reliability** | Migrations, indexes, constraints, backups and restore tests, idempotency, webhooks, queues, cron, caching, pooling, CI/CD, staging, rollback, disaster recovery, cost alerts, logging, error tracking, uptime |
| 🖱️ **Functional QA** | Dead buttons and links, forms that don't save, missing loading, empty and error states, leftover placeholder content, console errors, broken assets, phone and Safari journeys |
| ⚖️ **Legal & privacy** | Privacy policy vs actual data, terms, cookie consent, deletion and export, OSS licenses (GPL/AGPL), **web-font licenses**, an asset register, refunds, PCI, tax, honest marketing, dark patterns |
| 📱 **UX & launch** | Accessibility (WCAG 2.2 AA), mobile, Core Web Vitals, 404/500 pages, SEO basics, email deliverability (SPF/DKIM/DMARC), signup and SMS abuse, app store rules |
| 🧩 **Platform traps** | Supabase, Firebase, Vercel/Netlify, **Cloudflare** (TLS minimum, `workers.dev`, R2), Next.js, Lovable/Bolt/v0/Replit, Stripe/Razorpay/Paddle, Django/Rails/Express/Laravel, Expo/React Native, Docker/VPS |

**Profile modules** (run only when they apply to your app):

| Module | Runs when | Highlights |
|---|---|---|
| 🤖 **AI features** | The app uses an LLM | Keys on the server, per-user quotas, prompt injection, unsafe output rendering, agent tool permissions, RAG tenant isolation, AI disclosure |
| 🧒 **Kids & education** | Minors, students, schools | Verifiable parental consent (DPDP, COPPA, FERPA), data minimization, **retention limits for minors' data**, photo GPS stripping, no trackers, staff access, institutional requirements |
| 🏥 **Health** | Health, medical or fitness data | Explicit consent, no health data in analytics, encryption, audit logs, disclaimers, BAAs/DPAs, medical-device questions |
| 💳 **Fintech** | Payments, wallets, payouts | PCI scope, ledgers, atomic transfers, reconciliation, payout fraud, local invoice and mandate rules, licensing questions |
| 📜 **Policy pack** | Launch and above | 16 documents: when each is needed, what it must contain, where to link it, and whether it matches your real data |
| 🏢 **Enterprise & government** | Enterprise level | SSO/SCIM, audit logs, data residency, RPO/RTO, pentest, SBOM, SOC 2/ISO readiness, security questionnaires, bus factor, GIGW/508 |

Plus the 🛠️ **fix playbook**: patterns and tests for IDOR, RLS, Firebase rules, leaked secrets, validation, webhooks and idempotency, race conditions, timeouts, rate limits, LLM caps, XSS, uploads, headers, cookie consent and account deletion.

Every check is tagged **🔴 blocks launch**, **🟡 fix before scale or paying users**, or **🟢 recommended**. The full lists are in [`skills/vibe-check/references/`](skills/vibe-check/references).

---

## Free & open source: what's included

**Everything in this repo is free, forever (MIT):**
- ✅ All 18 blind spots, 360+ checks and 13 modules, at all three levels
- ✅ The fix playbook, "fix safe items", the scope guard and report history
- ✅ Works in every tool listed above, with your own AI subscription
- ✅ Uses free local tools when you have them (npm audit, gitleaks, Playwright, Lighthouse), with fallbacks when you don't

**What it doesn't do (scope):**
- ❌ It isn't a legal opinion or a certified security audit. It flags issues and tells you what to ask a lawyer or auditor.
- ❌ No hosted scanning, dashboard or monitoring. Everything runs inside your own AI tool, on your machine.
- ❌ It doesn't send your code anywhere and doesn't phone home.
- ❌ It never changes your app's design, features or flows (see the guarantee above).

### ⭐ vibe-check Pro (coming soon)

A paid **connector** you plug into Claude Code, Cursor and other agents, for the checks a text file can't do:
- 🌐 **Live site scan:** TLS, HTTPS, headers, exposed files, extra domains, SSL and domain expiry
- 🖱️ **Hosted click-through:** every button, link and form, with screenshots of what's broken
- 🗄️ **Supabase/Firebase probe:** proves whether your data is readable with the public key
- 📧 **Email deliverability check** (SPF, DKIM, DMARC)
- 📊 **Dashboard**, report history and shareable **PDF reports**
- 🔔 **Weekly monitoring and alerts**

Your code stays on your machine. Only URLs, lockfiles and summaries are sent. 👉 **[Join the waitlist](https://github.com/vikneshchandrasekaran21/vibe-check/issues/new?title=Pro%20waitlist&labels=pro-waitlist&body=Interested%20in%20vibe-check%20Pro.%20I%20build%20with%3A%20)**

---

## Repo layout

```text
skills/vibe-check/          ← the skill (source of truth)
├── SKILL.md                  workflow, ground rules, AI blind spots, scope guard
└── references/
    ├── security.md           core: security & authentication
    ├── reliability.md        core: data, reliability, infra, observability, CI
    ├── functional-qa.md      core: broken buttons, links, forms, states
    ├── legal-privacy.md      core: legal, privacy, licensing (incl. fonts)
    ├── launch-ux.md          core: accessibility, mobile, SEO, email, abuse
    ├── platforms.md          core: Supabase, Firebase, Cloudflare, Vercel, builders, ...
    ├── ai-features.md        profile: LLM and AI features
    ├── kids-education.md     profile: minors, students, schools
    ├── health.md             profile: health & medical data
    ├── fintech.md            profile: payments, wallets, payouts
    ├── policies.md           profile: the policy pack
    ├── enterprise.md         profile: enterprise & government readiness
    ├── fixes.md              fix playbook
    └── report-template.md    report format
dist/vibe-check.md          ← everything in one file (for paste-in tools)   [generated]
dist/vibe-check.zip         ← upload-ready skill for the Claude app           [generated]
adapters/                   ← Cursor, Copilot, Windsurf, Cline, Gemini, AGENTS.md  [generated]
scripts/build.py            ← regenerates dist/ and adapters/
```

## FAQ

**Does it send my code anywhere?**
No. vibe-check is just instructions. It runs inside the AI agent you already use, under that tool's own privacy terms.

**Will it break my app?**
It doesn't change anything during the audit. When fixing, it changes only what you approve, adds a test for each fix, and lists every file it touched so you can review or revert. Use git, and try fixes on a branch or staging first.

**Which stacks does it support?**
Any. The checks are stack-agnostic, with extra guidance for Supabase, Firebase, Next.js, Vercel, Stripe, Razorpay, Django, Rails, Express, Laravel, Expo and the popular AI app builders.

**Is this a replacement for a lawyer or a security audit?**
No. It catches the common, costly mistakes and tells you exactly what to take to a lawyer. For health, finance or children's data, payments at scale, or enterprise customers, also get a professional review. Treat 🟢 as "no known blockers", not a guarantee.

**Quick, Launch or Enterprise?**
Quick before everyday deploys. Launch before going public, taking payments or handling personal data. Enterprise before selling to companies or government, or handling regulated data.

**Why didn't it fix things automatically?**
On purpose. It audits first so you see what's wrong. Then say *"fix the safe items"* for the invisible, easy-to-undo fixes, or name the issues you want fixed. Anything visible, or that needs a decision (like consent rules), waits for you.

## Contributing

Seen AI tools keep making a mistake that isn't covered? PRs are very welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

Edit only `skills/vibe-check/`, then run `python3 scripts/build.py` to regenerate `dist/` and `adapters/`. CI checks that they're in sync.

## 🏆 Hall of 🟢

Projects that passed vibe-check at **Launch level or above** and asked to be listed.

| Project | Level | Score | Checked |
|---|---|---|---|
| *Yours could be first* | | | |

**Get listed:** reach 🟢 SHIP at Launch or Enterprise level, then **[submit your project](https://github.com/vikneshchandrasekaran21/vibe-check/issues/new?title=Hall%20of%20Green%3A%20%3Cproject%3E&labels=hall-of-green&body=Project%20URL%3A%0AScore%20card%3A%0ALevel%3A%0ADate%3A)** with your score card. Scores are self-reported, and listings are removed if a project is reported as no longer passing.

## Changelog

See [CHANGELOG.md](CHANGELOG.md). The latest release is always on the [Releases](https://github.com/vikneshchandrasekaran21/vibe-check/releases/latest) page.

## License

[MIT](LICENSE). Use it, fork it, ship safer. 🚀
