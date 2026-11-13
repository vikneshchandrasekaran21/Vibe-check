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
- 🧯 No timeouts, no backups, no error tracking. You find out it's broken from an angry user
- ⚖️ A copy-pasted privacy policy that doesn't match the app, and analytics that run before cookie consent

`vibe-check` is an open **[Agent Skill](https://agentskills.io)**. It turns your coding agent into a strict pre-launch reviewer that **finds** these problems, **explains** them in plain words and **fixes** the ones you approve, while leaving your design, features and use case alone.

## What you get

| | |
|---|---|
| 🔍 **Audit** | **17 AI blind-spot checks** plus **250+ checks** across security, data, reliability, cost, AI features, legal and privacy, UX and platform-specific traps |
| 📋 **Report** | A clear verdict (**🟢 SHIP / 🟡 SHIP AFTER FIXES / 🔴 DO NOT SHIP**), each problem in plain words with evidence (`file:line`), questions for you, and a "needs a lawyer" list |
| 🛠️ **Fixes** | A built-in **fix playbook** with proven patterns, so the agent fixes problems properly instead of guessing. Each fix gets a test and a re-check |
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
| *"vibe check this app"* | **Quick mode:** the 17 AI blind spots plus every 🔴 launch blocker |
| *"run a full vibe-check before launch"* | **Full mode:** every area that applies to your app |
| *"is this ready to ship?"* · *"what did the AI miss?"* · *"security audit"* | Quick mode, or full if you're launching or taking payments |
| *"fix the blockers"* · *"fix #1 and #3"* | Fixes only those issues, using the fix playbook |

### How it works

1. **Map:** your stack, the personal data you collect, every entry point, database rules and env vars. It asks about your users and business where that affects legal checks.
2. **Blind spots first:** the 17 mistakes AI coding tools make most often.
3. **Area checklists:** only the ones that apply to your stack.
4. **Report:** the verdict, blockers with plain-language impact and a fix prompt, questions for you, the "needs a lawyer" list, what passed, and other suggestions.
5. **Fix (only what you approve):** prove the bug, apply a proven pattern adapted to your stack, add a test, re-check, one issue per commit. For things only you can do (rotating a leaked key, DNS, legal decisions), it gives you exact steps.

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

---

## What it checks

| Area | Highlights |
|---|---|
| 🧠 **AI blind spots** | Authorization and IDOR, RLS and Firebase rules, leaked secrets, mass assignment, prices from the client, unverified payments, missing timeouts, race conditions, invented or outdated packages, LLM spend caps, exposed admin and debug pages, unsafe AI features |
| 🔐 **Security & auth** | Sessions, cookies, JWTs, password reset and magic links, brute force, OAuth, roles, multi-tenancy, SQL, NoSQL, XSS and command injection, uploads, SSRF, open redirects, CORS, CSRF, headers, hashing vs encryption, dependencies, rate limits |
| 🗄️ **Data & reliability** | Migrations, indexes, constraints, backups and restore tests, idempotency, webhooks, queues, cron, caching, pooling, CI/CD, staging, rollback, disaster recovery, cost alerts, logging, error tracking, uptime |
| 🤖 **AI features** | Keys on the server, per-user quotas, prompt injection, unsafe rendering of model output, agent tool permissions, RAG tenant isolation, provider data terms, moderation, AI disclosure |
| ⚖️ **Legal & privacy** | Privacy policy vs actual data, terms, cookie consent, deletion and export, OSS licenses (GPL/AGPL), asset licensing, refunds, PCI, tax, age limits, honest marketing, dark patterns. GDPR, CCPA, India DPDP and COPPA items flagged for a lawyer |
| 📱 **UX & launch** | Accessibility (WCAG 2.2 AA), mobile, Core Web Vitals, 404/500 pages, SEO basics, email deliverability (SPF/DKIM/DMARC), signup and SMS abuse, app store rules |
| 🧩 **Platform traps** | Supabase, Firebase, Vercel/Netlify, Next.js, Lovable/Bolt/v0/Replit, Stripe/Razorpay/Paddle, Django/Rails/Express/Laravel, Expo/React Native, Docker/VPS |
| 🛠️ **Fix playbook** | Patterns and tests for IDOR, RLS, Firebase rules, leaked secrets, validation, webhooks and idempotency, race conditions, timeouts, rate limits, LLM caps, XSS, uploads, headers, cookie consent, account deletion |

Every check is tagged **🔴 blocks launch**, **🟡 fix before scale or paying users**, or **🟢 recommended**. The full lists are in [`skills/vibe-check/references/`](skills/vibe-check/references).

---

## Repo layout

```text
skills/vibe-check/          ← the skill (source of truth)
├── SKILL.md                  workflow, ground rules, AI blind spots, scope guard
└── references/
    ├── security.md           security & authentication
    ├── reliability.md        data, reliability, infra, observability, testing
    ├── ai-features.md        LLM and AI-specific risks
    ├── legal-privacy.md      legal, privacy, licensing, payments
    ├── launch-ux.md          accessibility, mobile, SEO, email, abuse, app stores
    ├── platforms.md          Supabase, Firebase, Vercel, Next.js, builders, Stripe, ...
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

**Quick or full?**
Quick for everyday checks before deploys. Full before a public launch, before taking payments, or when you handle sensitive data.

## Contributing

Seen AI tools keep making a mistake that isn't covered? PRs are very welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

Edit only `skills/vibe-check/`, then run `python3 scripts/build.py` to regenerate `dist/` and `adapters/`. CI checks that they're in sync.

## License

[MIT](LICENSE). Use it, fork it, ship safer. 🚀
