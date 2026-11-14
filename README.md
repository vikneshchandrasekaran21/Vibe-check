<div align="center">

<img src="assets/banner.svg" alt="vibe-check: pre-launch audit for AI-built apps" width="100%">

**Find and fix what your AI coding agent misses, before real users do.**

Security · privacy · legal · reliability · launch, checked against your actual code, without changing what you built.

[![Release](https://img.shields.io/github/v/release/vikneshchandrasekaran21/Vibe-check?style=for-the-badge&color=22c55e&label=release)](https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest)
[![Checks](https://img.shields.io/badge/checks-653-18181b?style=for-the-badge)](skills/vibe-check/references)
[![Fix recipes](https://img.shields.io/badge/fix_recipes-75-18181b?style=for-the-badge)](skills/vibe-check/references/fixes.md)
[![Stars](https://img.shields.io/github/stars/vikneshchandrasekaran21/Vibe-check?style=for-the-badge&logo=github&color=18181b)](https://github.com/vikneshchandrasekaran21/Vibe-check/stargazers)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](LICENSE)
[![check](https://img.shields.io/github/actions/workflow/status/vikneshchandrasekaran21/Vibe-check/check.yml?style=for-the-badge&label=self-test)](https://github.com/vikneshchandrasekaran21/Vibe-check/actions/workflows/check.yml)

```bash
npx skills add vikneshchandrasekaran21/Vibe-check -g -a claude-code -y
```

<sub>That's for Claude Code. [Commands for other tools ↓](#quick-start-copy-one-command)</sub>

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

It works like a senior team in one command, covering what security, QA, legal and DevOps would each check. It asks a few questions about your app (who uses it, whether there are minors, payments or sensitive data) and runs only the checks that apply, and by default runs the **full check**. There's also a 🟢 **Quick** mode for small deploys and a 🔵 **Enterprise** mode for company and government apps.

## What you get

| | |
|---|---|
| 🔍 **Audit** | **19 AI blind-spot checks** plus **600+ checks** in 26 modules. It asks a few questions about your app and runs only the modules that apply |
| 📋 **Report** | A clear verdict (**🟢 SHIP / 🟡 SHIP AFTER FIXES / 🔴 DO NOT SHIP**), a **score out of 100** with a band (*Ready to scale · Ready to launch · Needs work · Not safe for real users yet*), a **totals table** (how many checks applied, passed, failed, and "checked 241 of 241") and a **scorecard per area**, all counted by a script, not written by the AI. Six symbols with one meaning each: ✅ passed · ❌ must fix · ⚠️ should fix · ❓ your answer · ➖ doesn't apply · 🔧 being fixed |
| 🛠️ **Fixes** | A **fix plan** first (what it can fix safely, what needs your decision, what only you can do), then **one fix card per fix**: before, what changed, what was checked, how to undo. If a check fails after a change, **the change is undone automatically**. Fixes go on a new branch with one commit each (or checkpoints in Lovable, Replit and Bolt). Built on a playbook of 75 fix recipes: **every 🔴 check points to one** |
| 💾 **History** | Every run is saved in `.vibe-check/` (kept out of git). The next run shows **what changed since last time**: fixed, new, and problems that **came back** after an AI tool undid a fix |
| 🗳️ **Questions as choices** | Questions show as **tap-to-choose cards** in tools that have them (Claude Code, Cursor, Gemini CLI, VS Code Copilot…) and as quick numbered choices everywhere else. It never asks what your code already answers |
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

### 🎯 Built not to make things up
- **Quote the proof:** every problem includes the exact code lines (re-read just before reporting) or the exact command output. No quote, no finding.
- **Second look:** before reporting, the agent tries to prove each finding **wrong**. Is it handled in middleware or RLS? Is the code even used? Is that "secret" actually a public key? Findings that don't survive are dropped.
- **Confidence labels:** 🔬 Confirmed (reproduced or direct proof), 🔎 Likely (strong evidence), ❓ Needs checking (becomes a question for you, never a blocker).
- **No facts from memory:** legal, policy and platform statements come only from the skill's own checklists or a source opened during the run.

### 🔍 Built not to skip anything
An AI can't promise it found every bug, but vibe-check makes sure **every check is actually done, and anything not done is labelled.**
- **Every check has a permanent ID** (`SEC-014`). Each result goes into a ledger with its evidence: passed, failed, doesn't apply, or couldn't check.
- **The coverage is counted by a script.** `coverage.py` compares the ledger with the checklist and won't let the report through if a check is missing, an ID is invented, the evidence is vague or copy-pasted, or a failure has no confidence label.
- **The code decides the profile, not the answers.** `profile.py` looks for date-of-birth fields, school or student data, payment SDKs and payment links, health, bank or ID data, AI calls, chat and more. If you say "no payments" but there's a Razorpay link in the code, the payment checks run anyway, and the report shows *Your answers vs your code*.
- **No full secrets in what you share.** The report, the chat summary and the ledger are scanned with the same secret patterns before the report is accepted; keys must be masked (`sk_l…`).
- **Evidence is re-opened, and the audit doesn't grade itself.** `coverage.py` checks that every cited `file:line` exists and every quoted line of code is really there. A fresh helper re-checks every 🔴 and a sample of passes. `--verify-report` rejects a report whose numbers don't match the ledger.
- **"Fix everything" works through the whole list:** a fix plan that survives new sessions, one decision per item, each fix re-checked by its own check ID, and a before-and-after score.
- **It lists every version the app runs.** `versions.py` finds the runtime, frameworks, CMS and plugins, Docker images and key packages with exact versions. Each one is checked against today's security releases, end-of-life dates and the actively-exploited list, with the source linked. Never from memory.
- **It lists the whole app first.** `inventory.py` lists every page, API route, function, webhook, form, button, env var, table, bucket, upload, payment, email and AI call. The report shows counts like *API routes checked: 47/47*.
- **It reads every file.** `sweep.py` searches every file, and the git history, for 60 risky patterns (leaked keys, unsafe HTML, SQL built from strings, template injection, Host-header reset links, open CORS, secrets in Docker images, Google Fonts, trackers…). Every match gets a verdict after the second look.
- **One module at a time, saved as it goes,** so a long audit on a big app resumes where it stopped instead of getting shallower.
- **The project's own tools run,** with every result recorded: package audit, type-check, lint, tests and build, including any tool that wasn't installed.
- **A test bench** of planted bugs checks the scripts on every change.

The scripts are read-only, need only Python 3, and come with the skill folder (Claude Code, Codex, the `npx skills` install and the Claude app zip). Single-file versions for other tools do the same steps by hand.

---

## Install

### Quick start: copy one command

Pick your tool, paste the line into your **Mac/PC Terminal**, and press Enter. There are no menus to answer.

| You use… | Run this |
|---|---|
| **Claude Code** | `npx skills add vikneshchandrasekaran21/Vibe-check -g -a claude-code -y` |
| **Cursor** | `npx skills add vikneshchandrasekaran21/Vibe-check -g -a cursor -y` |
| **Codex** | `npx skills add vikneshchandrasekaran21/Vibe-check -g -a codex -y` |
| **GitHub Copilot** | `npx skills add vikneshchandrasekaran21/Vibe-check -g -a github-copilot -y` |
| **Gemini CLI** | `npx skills add vikneshchandrasekaran21/Vibe-check -g -a gemini-cli -y` |
| **Several of these** | `npx skills add vikneshchandrasekaran21/Vibe-check -g -a claude-code -a cursor -a codex -y` |
| **Claude app** (desktop or claude.ai) | No terminal: [download `vibe-check.zip`](https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest/download/vibe-check.zip) → **Settings → Customize → Skills → Add → Upload skill**. Keep it zipped |
| **Replit** | In the Replit **Shell**: `npx skills add vikneshchandrasekaran21/Vibe-check -a replit -y` |
| **Lovable** | **Settings → Skills → Add → import from GitHub**, and paste `https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check` |
| **Bolt, v0, ChatGPT** | No install: copy [`dist/vibe-check-lite.md`](dist/vibe-check-lite.md) (48 KB: every blocker) and paste it into the chat. If your tool accepts long files, the full [`dist/vibe-check.md`](dist/vibe-check.md) has everything |

Then **open a new chat or session** in your app's folder and say: **"vibe check this app"** (in Replit and Lovable, type **`/vibe-check`**). That's it.

**How to tell it's really running:** the first line of the reply is *"Running vibe-check v… · Full check"*, and it starts by reading your code, not your preview. If you get a design review of your screen instead, the skill didn't load: call it with `/vibe-check`.

> **Updating:** `npx skills update` (or see [Updating](#-updating) for your tool). Already-open sessions keep the old version, so start a new one.
>
> **Tip:** use `npx skills add` instead of copying files by hand wherever your tool supports it. You get the helper scripts (deeper, counted checks) and one-command updates.

### 1. One command, with a menu to pick agents

```bash
npx skills add vikneshchandrasekaran21/Vibe-check        # this project
npx skills add vikneshchandrasekaran21/Vibe-check -g     # all your projects
```

The [skills CLI](https://github.com/vercel-labs/skills) shows a menu of agents. Use **Space** to select the ones you use (for example **Claude Code**) and **Enter** to confirm.

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

1. Download **[vibe-check.zip](https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest/download/vibe-check.zip)** (it's also in [`dist/`](dist/vibe-check.zip)).
2. In Claude, open **Settings → Customize → Skills**.
3. Click **Add → Upload skill** and pick the zip. Keep it zipped.
4. Make sure the skill is switched on. Then in any chat or project, say *"vibe check this app"*, and attach your code or connect a folder so Claude can read it.

### 5. Replit and Lovable (as a skill)

**Replit:** open the **Shell** in your Repl and run:
```bash
npx skills add vikneshchandrasekaran21/Vibe-check -a replit -y
```
It installs into the project's `.agents/skills` folder, scripts included. A workspace admin can also upload the skill folder under **Workspace settings → Customization → Skills**. Then in the Agent chat, call it by name so the agent can't improvise its own "vibe check": type `/vibe-check run the full audit on the whole codebase`, or use **+ → Use a skill → vibe-check**.

> **Tip:** a skill imported at the workspace level (**Customization → Skills → GitHub**) may give the agent only the main instructions, not the checklists and scripts. vibe-check notices, reads its checklists from GitHub and tells you, but the full audit with scripts needs the project install above. Use a full agent mode that can run Shell commands.

**Lovable:** a workspace owner or admin opens **Settings → Skills → Add**, chooses the GitHub import, and pastes:
```text
https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check
```
Then in any project chat, type `/vibe-check run the full audit on the whole codebase`. Lovable's agent may not be able to run the helper scripts; when it can't, vibe-check does the inventory, sweep and counting by hand and says so in the report.

### 6. Bolt, v0, ChatGPT (paste-in)

No install needed. Open [`dist/vibe-check-lite.md`](dist/vibe-check-lite.md) (the short version: AI blind spots and every 🔴 blocker, small enough for chat paste limits), copy everything, paste it into the chat and add. If your tool accepts very long messages or files, use the full [`dist/vibe-check.md`](dist/vibe-check.md) instead:

> Run this audit on my project. I'm not a developer, so explain each finding simply.

When the agent can't run commands, it reviews the code and config and tells you which commands to run yourself.

---

## 🔄 Updating

Installed skills don't update by themselves. **vibe-check tells you when a new version is out:** each run starts with a quick version check, and the report shows *"A newer vibe-check is out"* with the update command for your tool. Where the check can't connect (offline, or a sandbox without internet such as Codex's default), the report says so and links to the latest release. Every report shows the version it ran on.

| You installed with | To update |
|---|---|
| `npx skills add` (Claude Code, Codex, Cursor, Replit and others) | `npx skills update` (in Replit, run it in the Shell) |
| Lovable (imported from GitHub) | **Settings → Skills**: import again from `https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check` |
| Replit (folder uploaded in Workspace settings) | Upload the new folder again |
| The Claude app (zip) | Download `vibe-check.zip` from the [latest release](https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest) and upload it again |
| A copied rules or command file (Cursor, Copilot, Windsurf, Cline, Gemini CLI) | Copy the new file from [`adapters/`](adapters/) over the old one |
| Paste-in (Bolt, v0, ChatGPT) | Paste the new [`dist/vibe-check-lite.md`](dist/vibe-check-lite.md) (or the full `dist/vibe-check.md`) |

Then **start a new session**: an open session keeps the old version loaded.

**Get an email for new releases:** on GitHub, click **Watch → Custom → Releases** at the top of this repo.

**About the version check:** vibe-check itself only ever *reads* its own public files on GitHub: this version check, and its checklists if your tool didn't install them. The one exception is optional: at the end of an audit it offers, **once**, to share **anonymous counts** (version, stack type, how many checks passed or failed and which check IDs). It shows you exactly what would be sent first, sends nothing unless you say yes, and never sends code, file paths, names or URLs. Say no and it won't ask again. It reads the latest version number from this repo on GitHub and sends nothing about you: no code, no report, no project name. It gives up after 3 seconds and never blocks the audit. To turn it off, set `VIBE_CHECK_NO_UPDATE_CHECK=1`, or add `update_check: false` to `.vibe-check/config` in your project.

## Use

Just ask your agent:

| Say | What happens |
|---|---|
| *"vibe check this app"* · *"is this ready to ship?"* · *"audit my app"* | 🟡 **Full check** (default): every module that applies to your app |
| *"enterprise vibe check"* | 🔵 **Enterprise:** the full check plus enterprise and government readiness and the full policy pack |
| *"quick vibe check"* | 🟢 **Quick:** only the 19 AI blind spots and 🔴 blockers. For small, everyday deploys |
| *"fix"* · *"fix all"* · *"fix 2"* | Fixes the blockers, everything it safely can, or one item, each with a fix card |
| *"explain 2"* | The full detail and evidence for one finding |
| *"check again"* | Re-runs the audit and shows what changed since last time |
| *"continue fixing"* · *"undo fix 2"* | Picks up where fixing stopped, or reverts one fix |

### How it works

1. **Profile:** who uses the app, whether there are minors or students, money, sensitive data, regions. It works out what it can from the code and asks only what it can't.
2. **Map:** stack, data map (including things like photo GPS), entry points, database rules, env vars, live and platform default domains, known issues.
3. **Blind spots:** the 19 mistakes AI coding tools make most often.
4. **Modules:** the core modules plus only the profile modules that apply. It uses real tools where available (audit, secret and licence scanners, Playwright, Lighthouse), and falls back to reading the code when they're missing.
5. **Report:** saved to `.vibe-check/reports/` with a summary in chat. You get the verdict and score, blockers with a fix prompt, which items are safe to auto-fix, questions for you, a "needs a lawyer" list, what passed, a **coverage table** for every module, and what wasn't checked. Before replying, the agent runs a **self-check** so nothing is silently skipped.
6. **Fix (only what you approve):** prove the bug, apply a proven pattern, add a test, re-check, one issue per commit. For things only you can do (dashboard settings, rotating keys, legal decisions), it gives you exact steps.

### Example report

```text
Running vibe-check v3.5.0 · Full check

🔴 DO NOT SHIP · Score 69/100 (capped: 2 blockers open) · Needs work

Checks                       Count
Apply to this app              241   (412 ➖ don't apply)
✅ Passed                      198
❌ Must fix (blockers)           2
⚠️ Should fix                   29
❓ Need your answer             12
Checked                 241 of 241   ✅ nothing skipped

Area               Score            Passed   ❌   ⚠️   ❓
Security           ███████░░░ 74    62/80     1   11    6
Payments           █████████░ 92    11/12     —    1    —
Privacy & legal    ██████░░░░ 63    30/44     —   10    4

❌ Must fix before launch (2)
 1. Any logged-in user can open another user's invoices · app/api/invoices/[id]/route.ts:14
 2. The Stripe secret key is in the browser bundle · lib/stripe.ts:3

You can say: "fix" · "explain 1" · "fix all" · "check again"
```

And each fix comes back as a card:

```text
🔧 Fix 1 of 2 · Users could open other users' invoices (❌ blocker · SEC-015)
Before   Any logged-in user could read any invoice by changing the ID in the URL
Changed  app/api/invoices/[id]/route.ts · only the owner gets the invoice now (+3 lines)
Checked  ✅ Types  ✅ Tests: 14 passed  ✅ SEC-015 re-checked: passes
Saved    Commit a1b2c3d · undo: say "undo fix 1"
```

### 🏁 Show your score

Every report ends with a one-line **score card**, made to screenshot and share:

```text
vibe-check: 🟢 SHIP · Score 91/100 · 112/118 checks · 0 blockers · Full check · 13 Nov 2026
```

Start at 🔴? Most people do. Fix, re-run, and post your before → after score with **#vibecheck**.

Once there are no blockers, you can add your score badge to your README:

```markdown
[![vibe-check score](https://img.shields.io/badge/vibe--check-91%2F100%20·%20Ready%20to%20scale-brightgreen)](https://github.com/vikneshchandrasekaran21/Vibe-check)
```

[![vibe-check score](https://img.shields.io/badge/vibe--check-91%2F100%20·%20Ready%20to%20scale-brightgreen)](https://github.com/vikneshchandrasekaran21/Vibe-check)

The report ends with a small "Checked with vibe-check" footer. Tell your agent *"no footer"* to remove it. It never adds anything to your app.

---

## What it checks

**Core modules** (always run in the full check):

| Area | Highlights |
|---|---|
| 🧠 **AI blind spots** | Authorization and IDOR, RLS and Firebase rules, leaked secrets, mass assignment, prices from the client, unverified payments, missing timeouts, race conditions, invented or outdated packages, LLM spend caps, exposed admin and debug pages, unsafe AI features |
| 🔐 **Security & auth** | Sessions, cookies, JWTs, password reset and magic links, brute force, OAuth, roles, multi-tenancy, SQL, NoSQL, XSS and command injection, uploads, SSRF, open redirects, CORS, CSRF, headers, **encryption at rest, in transit and per field**, **data leakage** (over-sharing APIs, account enumeration, cached private pages, tokens in URLs, guessable links, data sent to third parties, exports), dependencies, rate limits |
| 🗄️ **Data, reliability & testing** | Status codes, timeouts, idempotency, webhooks, migrations, indexes, constraints, queues, scheduled cleanup jobs, caching, pooling, concurrency, **load, spike, soak and data-volume tests (on staging only)**, graceful overload, payment replay tests, test coverage of money and login paths |
| ⚙️ **DevOps & operations** | CI on every push, protected main, Dependabot, separate environments, automated deploys and **rollback**, platform default domains, **error alerts that reach a human**, uptime and **cron monitoring**, third-party outage handling, logs without personal data, **backups with a tested restore**, disaster recovery, MFA everywhere, secret rotation, bus factor, billing alerts, domain/SSL expiry, email that actually sends, incident runbook |
| 🖱️ **Functional QA** | Dead buttons and links, forms that don't save, loading, empty and error states, **clear error and success messages**, delete confirmations, payment result screens, typos, **edge cases** (money rounding, long or non-Latin text, time zones, list edges, limits), **session expiry, multiple tabs, smoke test of every journey for every role**, console errors, broken assets, phone and Safari |
| ⚖️ **Legal & privacy** | Privacy policy vs actual data, terms, cookie consent, deletion and export, OSS licenses (GPL/AGPL), **web-font licenses**, an asset register, refunds, PCI, tax, honest marketing, dark patterns |
| 📱 **UX & launch** | Accessibility (WCAG 2.2 AA), responsive design, Core Web Vitals, 404/500 pages, SEO basics, email deliverability (SPF/DKIM/DMARC), signup and SMS abuse |
| ⚖️ **Lawsuit magnets & jurisdictions** | What people actually get sued over: **Google Fonts and other IP leaks**, **pixels, session replay and chat widgets before consent** (California wiretap suits), embeds, **ADA accessibility on revenue paths** (and overlays that don't help), **auto-renewal and click-to-cancel**, marketing opt-in (CASL, TCPA), fake urgency, fair cookie banners, **Impressum**, **Quebec French**, biometrics, plus a **country table** (EU, DACH, UK, US, Canada, India, Brazil, Australia, Asia, app stores) |
| 🔗 **Supply chain & CI** | Lockfiles, typosquats, install scripts, dependency confusion, **GitHub Actions pinned to SHAs**, `pull_request_target`, token permissions, secrets in logs, third-party scripts, SRI, tag managers, secret scanning |
| 🧪 **Tests against the running app** | With your OK, on local or staging only (never production): user B tries to read, change and delete user A's data on every object type; normal users try admin functions; logged-out visitors try private routes; rate limits, error messages and uploads are tested for real; OWASP ZAP baseline and nuclei run with safe settings |
| 📏 **Standards view** | Every result is mapped to the **OWASP Top 10:2025, API Security Top 10, LLM Top 10, Mobile Top 10, ASVS 5.0 (by chapter) and the 2025 CWE Top 25**, so the report shows ✅/❌/◐ per item. A coverage view of the audit, not a certification. The report also lists what *only a human* can confirm and when to run again |
| 🎯 **Hunt mode** | After the checklists, the agent **attacks the app's own logic** to find bugs no scanner or checklist describes. It writes a threat model, then tests invariants (*credits never below zero*), abuse cases for every money, quota and invite feature, the same action across web, API, mobile and old endpoints, hidden assumptions, variants of every finding, and chains. Each idea is proven with a safe local test, disproven, or marked untested. New ones are marked 🎯 *Found by hunting* |
| 🧯 **Known vulnerabilities** | Every component the app runs, with exact versions (`versions.py`): runtime (PHP, Node, Python…), framework, CMS **and each plugin**, packages in every ecosystem, Docker images, database engines, SDKs. Checked against **today's** security releases and advisories, end-of-life dates and CISA's **actively exploited** list, with the right audit tool per ecosystem and official workarounds |
| 🧹 **Maintainability & handover** | Strict types, linting, dead and duplicated code, README and `.env.example`, architecture notes, AI rules files, **who owns every account**, credentials in a vault, due-diligence pack |
| 🧩 **Platform traps** | Supabase, Firebase, Vercel/Netlify, **Cloudflare** (TLS minimum, `workers.dev`, R2), Next.js, Lovable/Bolt/v0/Replit, Stripe/Razorpay/Paddle, Django/Rails/Express/Laravel, Expo/React Native, Docker/VPS |

**Profile modules** (run only when they apply to your app):

| Module | Runs when | Highlights |
|---|---|---|
| 🤖 **AI features** | The app uses an LLM | Keys on the server, per-user quotas, prompt injection, unsafe output rendering, agent tool permissions, RAG tenant isolation, AI disclosure |
| 🧒 **Kids & education** | Minors, students, schools | Verifiable parental consent (DPDP, COPPA, FERPA), data minimization, **retention limits for minors' data**, photo GPS stripping, no trackers, staff access, institutional requirements |
| 🏥 **Health** | Health, medical or fitness data | Explicit consent, no health data in analytics, encryption, audit logs, disclaimers, BAAs/DPAs, medical-device questions |
| 💳 **Fintech** | Payments, wallets, payouts | PCI scope, ledgers, atomic transfers, reconciliation, payout fraud, local invoice and mandate rules, licensing questions |
| 📜 **Policy pack** | Full and Enterprise | 16 documents: when each is needed, what it must contain, where to link it, and whether it matches your real data |
| 📱 **Mobile apps** | iOS, Android, Expo, Capacitor, Flutter | In-app account deletion, **permission strings (missing ones crash the app)**, privacy labels and manifest, in-app purchase verified on the server, App Tracking Transparency, SDK targets, secrets in the bundle, secure token storage, cleartext traffic, deep links, WebViews, crash reporting, forced updates |
| 👥 **Community & marketplace** | Users post, chat or trade | Report, block, moderation queue, filtering, minors and adults, appeals, **realtime/WebSocket authorization**, message limits, takedown and CSAM duties, DSA / Online Safety Act / IT Rules, seller verification, payouts, disputes, fake reviews |
| ☁️ **Cloud infrastructure** | AWS, GCP, Azure, Kubernetes, Terraform | Public buckets, encryption, wildcard IAM, long-lived keys, root account, open database ports, TLS, SSH, containers as root, secrets in images, IaC scanning, state files, backups, cost controls |
| 🖥️ **Desktop & extensions** | Electron, Tauri, browser extensions | `contextIsolation`, safe preload bridges, remote content, **code signing and notarization**, signed auto-update, extension permissions, Manifest V3, content script trust, store disclosures |
| 🌍 **Internationalisation** | Several languages or countries | Missing translations, legal text per language, plurals, scripts and fonts (Hindi, Tamil, Arabic), RTL, longer text, currency and number formats, phone and address formats, local payment methods |
| 🤖 **AI agents & MCP** | Agents take actions, or MCP servers | Least-privilege tools, acting as the user, **confirmation for risky actions**, indirect prompt injection, exfiltration paths, sandboxing, loop and cost limits, audit log, kill switch, MCP auth, honest tool descriptions |
| 🏢 **Enterprise & government** | Enterprise level | SSO/SCIM, audit logs, data residency, RPO/RTO, pentest, SBOM, SOC 2/ISO readiness, security questionnaires, bus factor, GIGW/508 |

Plus the 🛠️ **fix playbook**: patterns and tests for IDOR, RLS, Firebase rules, leaked secrets, validation, webhooks and idempotency, race conditions, timeouts, rate limits, LLM caps, XSS, uploads, headers, cookie consent and account deletion.

Every check is tagged **🔴 blocks launch**, **🟡 fix before scale or paying users**, or **🟢 recommended**. The full lists are in [`skills/vibe-check/references/`](skills/vibe-check/references).

---

## Free & open source: what's included

**Everything in this repo is free, forever (MIT):**
- ✅ All 19 blind spots, 600+ checks and 26 modules, at all three levels
- ✅ The fix playbook, fix plan and fix cards, the scope guard, and run-to-run history
- ✅ Works in every tool listed above, with your own AI subscription
- ✅ Uses free local tools when you have them (npm audit, gitleaks, Playwright, Lighthouse), with fallbacks when you don't

**What it doesn't do (scope):**
- ❌ It isn't a legal opinion or a certified security audit. It flags issues and tells you what to ask a lawyer or auditor.
- ❌ No hosted scanning, dashboard or monitoring. Everything runs inside your own AI tool, on your machine.
- ❌ It never sends your code, reports or data anywhere. It only ever reads its own public files on GitHub (an optional version check, and its checklists if your tool didn't install them), sending nothing about you (see [Updating](#-updating)).
- ❌ It never changes your app's design, features or flows (see the guarantee above).

### ⭐ vibe-check Pro

A paid **connector** you plug into Claude Code, Cursor and other agents, for the checks a text file can't do:
- 🌐 **Live site scan:** TLS, HTTPS, headers, exposed files, extra domains, SSL and domain expiry
- 🖱️ **Hosted click-through:** every button, link and form, with screenshots of what's broken
- 🗄️ **Supabase/Firebase probe:** proves whether your data is readable with the public key
- 📧 **Email deliverability check** (SPF, DKIM, DMARC)
- 📊 **Dashboard**, report history and shareable **PDF reports**
- 🔔 **Weekly monitoring and alerts**

Your code stays on your machine. Only URLs, lockfiles and summaries are sent. 👉 Sign-up link coming in the next release: click **Watch → Custom → Releases** at the top of this repo to hear first.

---

## Repo layout

```text
skills/vibe-check/          ← the skill (source of truth)
├── SKILL.md                  workflow, ground rules, AI blind spots, scope guard
├── scripts/                  read-only helpers the agent runs in the user's project (Python 3, no installs)
│   ├── profile.py            the code decides the profile: dob fields, payment SDKs and links, health, AI, chat… (answers can't remove it)
│   ├── inventory.py          lists everything in the app: pages, routes, forms, env vars, tables…
│   ├── sweep.py              searches every file and git history for risky patterns (secrets masked)
│   ├── versions.py           lists everything the app runs with exact versions (runtime, frameworks, plugins, images)
│   ├── coverage.py           counts the ledger against the checklist; fails on any gap
│   ├── share_stats.py        opt-in: shows, then (only if you say yes) shares anonymous counts
│   └── version_check.py      tells you when a newer vibe-check is out (sends nothing about you)
└── references/
    ├── blind-spots.md        step 3: the 19 AI blind spots (every level)
    ├── ledger.md             step 4: the ledger format, row types, tools and fallbacks
    ├── helper-brief.md       step 4: the brief pasted to every helper agent
    ├── reporting.md          step 5: what the report contains, saving, verifying, the chat summary
    ├── self-check.md         step 5: the checklist before replying
    ├── fixing.md             step 6: fix plan, branch or checkpoints, fix cards, undo, scope guard
    ├── updating.md           how to update vibe-check in each tool
    ├── security.md           core: security, auth, encryption, data leakage
    ├── reliability.md        core: data, reliability, load and stress, testing
    ├── devops.md             core: CI/CD, deploys, monitoring, backups, access, incidents
    ├── functional-qa.md      core: general QA: flows, messages, edge cases, sessions
    ├── legal-privacy.md      core: legal, privacy, licensing (incl. fonts)
    ├── launch-ux.md          core: accessibility, mobile, SEO, email, abuse
    ├── platforms.md          core: Supabase, Firebase, Cloudflare, Vercel, builders, ...
    ├── lawsuits.md           core: lawsuit magnets & jurisdictions
    ├── supply-chain.md       core: dependencies, CI/CD, third-party scripts
    ├── hunt.md               core: hunt mode, attacking the app's own logic to find what no checklist describes
    ├── vulnerabilities.md    core: known vulnerabilities in the runtime, frameworks, CMS, plugins, images; end-of-life; actively exploited
    ├── maintainability.md    core: code health, docs, ownership, handover
    ├── ai-features.md        profile: LLM and AI features
    ├── ai-agents.md          profile: AI agents, tools and MCP servers
    ├── kids-education.md     profile: minors, students, schools
    ├── health.md             profile: health & medical data
    ├── fintech.md            profile: payments, wallets, payouts
    ├── policies.md           profile: the policy pack
    ├── enterprise.md         profile: enterprise & government readiness
    ├── mobile.md             profile: iOS and Android apps
    ├── community.md          profile: community, chat and marketplaces
    ├── cloud-infra.md        profile: AWS, GCP, Azure, Kubernetes, Terraform
    ├── desktop-extensions.md profile: Electron, Tauri, browser extensions
    ├── live-tests.md         profile: tests against the running app on local or staging (two accounts, roles, logged out, ZAP, nuclei)
    ├── i18n.md               profile: languages, regions, formats
    ├── fixes.md              fix playbook: 75 recipes, each listing the checks it covers (every 🔴 check has one)
    ├── report-template.md    report format
    ├── standards.md          OWASP Top 10:2025, API, LLM, Mobile, ASVS 5.0 chapters and CWE Top 25, mapped to vibe-check checks
    └── sweep-patterns.md     the sweep patterns, for doing it by hand  [generated]
dist/vibe-check.md          ← everything in one file (for paste-in tools)   [generated]
dist/vibe-check-lite.md     ← short version for chat paste limits: blind spots + every 🔴 check   [generated]
dist/vibe-check.zip         ← upload-ready skill for the Claude app           [generated]
adapters/                   ← Cursor, Copilot, Windsurf, Cline, Gemini, AGENTS.md  [generated]
scripts/build.py            ← regenerates dist/ and adapters/
scripts/validate.py         ← checks the skill is complete and consistent (runs in CI)
maintainers/law-updates.md  ← weekly checklist for laws and standards (dates warned when stale)
maintainers/metrics.md      ← how to see usage: GitHub traffic, downloads, opt-in stats
SECURITY.md                 ← how to report a problem in vibe-check privately
tests/test_scripts.py       ← test bench: a small app with planted bugs the scripts must catch
scripts/release.sh          ← publishes a release (the tag always matches the version in SKILL.md)
```

## FAQ

**Does it send my code anywhere?**
No. vibe-check is instructions plus a few read-only helper scripts, running inside the AI agent you already use, under that tool's own privacy terms. vibe-check itself only reads its own public files on GitHub (the version check, and its checklists if your tool didn't install them) and sends nothing about you. You can turn it off (see [Updating](#-updating)).

**Will it break my app?**
It doesn't change anything during the audit. When fixing, it changes only what you approve, adds a test for each fix, and lists every file it touched so you can review or revert. Use git, and try fixes on a branch or staging first.

**Which stacks does it support?**
Any. The checks are stack-agnostic, with extra guidance for Supabase, Firebase, Next.js, Vercel, Stripe, Razorpay, Django, Rails, Express, Laravel, Expo and the popular AI app builders.

**Is this a replacement for a lawyer or a security audit?**
No. It catches the common, costly mistakes and tells you exactly what to take to a lawyer. For health, finance or children's data, payments at scale, or enterprise customers, also get a professional review. Treat 🟢 as "no known blockers", not a guarantee.

**Which mode should I use?**
Just say *"vibe check this app"*. That runs the full check, which is what most people need. Use *"quick vibe check"* only for small everyday deploys, and *"enterprise vibe check"* before selling to companies or government.

**Why didn't it fix things automatically?**
On purpose. It audits first so you see what's wrong. Then say *"fix the safe items"* for the invisible, easy-to-undo fixes, or name the issues you want fixed. Anything visible, or that needs a decision (like consent rules), waits for you.

## Contributing

Seen AI tools keep making a mistake that isn't covered? PRs are very welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

Edit only `skills/vibe-check/`, then run `python3 scripts/build.py` to regenerate `dist/` and `adapters/`, and `python3 scripts/validate.py` to check that every module is wired in, every check has a severity and name, nothing is duplicated, and the README, zip and adapters are complete. CI runs both.

## Changelog

See [CHANGELOG.md](CHANGELOG.md). The latest release is always on the [Releases](https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest) page.

## License

[MIT](LICENSE). Use it, fork it, ship safer. 🚀
