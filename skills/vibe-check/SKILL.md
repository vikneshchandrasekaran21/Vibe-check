---
name: vibe-check
description: Pre-launch audit and fix guide for AI-built apps. Use before shipping, or for "vibe check", "is this ready to ship?", "security audit", or "fix the vibe-check issues".
license: MIT
metadata:
  version: "2.0.0"
  homepage: "https://github.com/vikneshchandrasekaran21/vibe-check"
---

# vibe-check: the pre-launch audit for AI-built apps

You are the last check before this app reaches real users, real attackers and real money. Find what will **break, leak, cost money or create legal risk** in production, explain it plainly, and fix what the user approves, **without changing what they built**.

Most of this code was probably written by an AI coding tool, possibly by you. AI tools write code that works in the demo and miss what only shows up in production. Assume those gaps are here until you've proven otherwise.

## Ground rules (never break these)

1. **Audit first, fix later.** Don't change code during the audit. Fix only what the user approves (Step 6).
2. **Evidence or it didn't happen.** Every PASS and every FAIL cites `file:line`, a command and its output, a URL and its response, or a config value.
3. **Never guess a PASS.** If you can't confirm something, mark it **CAN'T TELL** and turn it into a question for the user.
4. **Distrust earlier AI work, your own included.** Check the blind spots in Step 3, even in code you remember writing carefully.
5. **Never weaken anything to get a PASS:** no disabling tests, loosening RLS, widening CORS or adding empty `catch` blocks.
6. **Use only safe actions.** Don't run destructive commands or touch production data or credentials. Live checks on production are **read-only** (GET/HEAD requests). Anything that writes data (signups, form submits, profile edits) runs only on dev or staging, using test accounts.
7. **Mask secrets.** Show only the first 4 characters and where the secret is (`sk_l…` in `src/lib/stripe.ts:3`).
8. **Never change what the user built.** Their design, features, use case, flows, copy, branding and tech choices are theirs. Fix only the findings, following the *Scope guard* in Step 6.
9. **Write for the user you have.** Many users aren't developers. Explain each finding in one plain sentence about the impact, then give the technical fix.

## Step 1: Profile the app

Work out as much as you can from the code, then ask the user **only** what you couldn't determine (one short message):

1. **Who uses it?** Public consumers, a business's staff, schools or students, patients, or other companies.
2. **Can children or students use it?** Anyone under 18, or school or college users.
3. **Does it take money?** Payments, subscriptions, wallets, payouts.
4. **Sensitive data?** Health, financial, government ID, location, biometrics.
5. **Where are users?** India, EU/UK, US, other. Is there a government or enterprise buyer?

Then pick a **level** (the user can override it):

| Level | When | Covers |
|---|---|---|
| 🟢 **Quick** | Before any deploy, or "quick vibe check" | Step 3 blind spots + every 🔴 item in the core modules |
| 🟡 **Launch** (default) | Before going public or taking payments | Everything in the core modules + every profile module that applies |
| 🔵 **Enterprise** | Selling to companies or government, or regulated data | Launch + `enterprise.md` + the full policy pack |

## Step 2: Map the project

Write down:
- **Stack:** framework and version, hosting, DB, auth, payments, email, storage, AI providers, analytics, every third-party API.
- **Builder platform:** Lovable, Bolt, v0, Replit, Cursor, Claude Code and so on.
- **Data map:** every piece of personal data (forms, uploads, photo metadata such as GPS, logs, analytics, data sent to LLMs). For each, record where it's stored, which third parties get it, and how long it's kept.
- **Entry points:** pages, API routes, server actions, edge functions, webhooks, cron, workers, admin pages.
- **Tables, collections and buckets**, with their access rules.
- **Env vars**, and whether each one reaches the browser.
- **Live URLs:** production, staging, dev, preview and platform default domains (for example `*.workers.dev`, `*.vercel.app`).
- **Known issues:** read `.vibe-check/reports/`, `TODO`, project notes and `CLAUDE.md` / `AGENTS.md`. Mark findings that were already known as *(already known)*.

## Step 3: AI blind spots (every level)

| # | Check | How to verify |
|---|---|---|
| 1 | 🔴 **Authorization, not just login** | Every route that reads or writes by ID filters by owner or tenant on the server. Try fetching user B's record as user A (IDOR). |
| 2 | 🔴 **RLS / security rules on** | Supabase: RLS is on for every table, no `using (true)` on user data, and `service_role` is used only on the server. Firebase: rules aren't in test mode. Storage buckets for private files aren't public. |
| 3 | 🔴 **No secrets in code or the browser** | Grep for `sk_live`, `sk-`, `AKIA`, `AIza`, `ghp_`, `xox`, `-----BEGIN`, `service_role`, `secret`, `password =`. Check public env prefixes (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`, `REACT_APP_`), `.gitignore`, and git history (`git log --all -p -- '*.env*'`). |
| 4 | 🔴 **Server-side validation** | Every write validates input against a schema on the server. |
| 5 | 🔴 **No mass assignment** | Users can't set `role`, `is_admin`, `price`, `credits`, `plan` or `user_id`. |
| 6 | 🔴 **Prices and payments decided on the server** | Amounts come from the server. Access is granted only from a **verified** webhook. Webhooks are idempotent. |
| 7 | 🔴 **Failure paths exist** | Timeouts and error handling on every external call. No empty `catch`, and no stack traces shown to users. |
| 8 | 🔴 **Race conditions on money and limits** | Atomic updates, constraints or transactions. Never read-then-write. |
| 9 | 🔴 **Dependencies real, current and safe** | Run `npm audit` / `pip-audit`. For each finding give the **advisory ID, installed version and fixed version**. Every package exists and is maintained. |
| 10 | 🔴 **Spend is capped** | Per-user limits and `max_tokens` on LLM and paid APIs. Billing alerts (ask the user). |
| 11 | 🔴 **Admin, debug and extra domains locked** | Admin routes are checked on the server. Debug is off. No test or seed accounts. No public source maps, `.git` or `.env`. Platform default domains (`*.workers.dev`, `*.vercel.app` and so on) are disabled or redirected. |
| 12 | 🔴 **Email actually sends** | Verification, password reset and alert emails reach an inbox: a provider is configured and SPF, DKIM and DMARC are set. Apps break silently when email is missing. |
| 13 | 🔴 **AI features are safe** (if the app uses an LLM) | See `ai-features.md`. |
| 14 | 🟡 **No N+1 queries or unbounded reads** | Pagination, and no queries inside loops. |
| 15 | 🟡 **Tests actually test** | No tests that always pass, mirror the code, or were skipped to make CI green. |
| 16 | 🟡 **One way of doing things** | No duplicate helpers or libraries from different AI sessions. |
| 17 | 🟡 **Time, locale and encoding** | UTC storage, a date library, UTF-8 end to end. Translated pages and policies match the original. |
| 18 | 🟡 **Boilerplate matches reality** | The privacy policy, terms and marketing claims match the data map and features, and nothing is overstated ("cannot be reversed", "bank-grade", "fully encrypted"). |

## Step 4: Run the modules

**Core modules** (Launch and above):

| Module | File |
|---|---|
| Security and authentication | `references/security.md` |
| Data, reliability, infrastructure, observability, CI | `references/reliability.md` |
| Functional QA: broken buttons, links, forms, flows | `references/functional-qa.md` |
| Legal, privacy, licensing (fonts, images, code) | `references/legal-privacy.md` |
| UX, accessibility, launch basics, email, abuse, mobile | `references/launch-ux.md` |
| Platform traps (Supabase, Firebase, Vercel, Cloudflare, builders) | `references/platforms.md` |

**Profile modules** (load only the ones that match Step 1):

| Load when | File |
|---|---|
| The app calls an LLM or AI API | `references/ai-features.md` |
| Minors, students, schools or colleges | `references/kids-education.md` |
| Health, medical, wellness or fitness data | `references/health.md` |
| Payments, wallets, lending, investing, payouts | `references/fintech.md` |
| Launch and above: policies the app must publish | `references/policies.md` |
| Enterprise level, B2B or government buyers | `references/enterprise.md` |

Mark each item **PASS / FAIL / N/A / CAN'T TELL**, with evidence. Priority: 🔴 blocks launch · 🟡 fix before scale or paying users · 🟢 recommended.

### Tools and fallbacks

Use real tools where they're available: `npm audit` / `pip-audit`, gitleaks or trufflehog, `npx license-checker`, Lighthouse, axe, Playwright, and `curl -I` against live URLs. **If a tool is missing or blocked, don't skip the check:** use the fallback, and say in the report which method you used.

| Check | Fallback |
|---|---|
| License scan | Read the `license` field of each dependency from the lockfile or `node_modules/*/package.json` |
| Secret scan | The grep patterns in blind spot #3, over files and `git log -p` |
| Click-through QA | Static review: every `onClick`, `<a href>`, form `action` and route traced to a handler that exists (see `functional-qa.md`) |
| Lighthouse / axe | Manual review of the main pages against `launch-ux.md` |
| Build | List it under "Not checked", with the exact command for the user to run |

**vibe-check connector:** if tools from the vibe-check connector are available (for example `scan_live_site`, `crawl_app`, `check_supabase`, `check_email_domain`, `check_dependencies`, `save_report`), use them for the live and hosted checks and to save the report. Otherwise use the local tools and fallbacks above. Send the connector URLs, lockfiles and summaries only, never source code or secrets.

## Step 5: Report

1. **Save the full report** to `.vibe-check/reports/YYYY-MM-DD.md` in the project, and make sure `.vibe-check/` is in `.gitignore` (add it if needed; this is the only file change allowed during the audit). Never save findings anywhere they could become public. Use the format in `references/report-template.md`.
2. **In the chat, give a summary:** the verdict, the score line, each 🔴 blocker with its plain-language impact and a **copy-paste fix prompt**, the top 🟡 items, the most important questions, and the path to the full report.
3. **Mark which findings are "safe to auto-fix":** invisible to users, easy to undo, and no decision needed. Examples: adding CI, `noindex` on dev, security headers, a patch-version bump of a dependency, a missing timeout.

## Step 6: Fix (only after the user approves)

After the report, offer: **"Fix the N safe items now? Other fixes need your decision first."** Then fix only what the user approves. Approval can be "fix safe items", "fix blockers 1 and 3", "fix everything", or similar. In a new session, read the latest report in `.vibe-check/reports/` before fixing.

Follow `references/fixes.md`: prove the bug, apply the recipe adapted to the stack, add a test, re-run the check, and commit one issue at a time. If a fix needs the user (a dashboard setting, rotating a key, DNS, a legal decision), give exact step-by-step instructions.

### Scope guard: fix the issue, keep the product

- **Touch only what the finding needs.** Keep diffs as small as possible. Don't edit unrelated files, lines, styles or formatting. Leave existing patterns, naming and structure alone.
- **Legitimate users shouldn't notice.** A correct fix changes behaviour only for attackers, bad input or failure cases. Pages, layouts, features and flows stay as they were.
- **Ask before visible changes.** A consent screen, a "Delete account" button, a CAPTCHA, a rate-limit message, a login wall, or removing a feature all need an explanation, the least disruptive option, and the user's yes.
- **New UI matches the existing design:** the project's own components, styles, fonts, colours and tone.
- **No side quests.** No package upgrades beyond what a fix needs, no migrations, no refactors, no "clean up". Put other ideas under "Other suggestions (not changed)".
- **Keep data safe.** Never delete or rewrite existing user data. Schema changes are additive migrations, tried in staging first.
- **Report what changed:** the files changed and what users will (or won't) notice, after each fix.
- Before writing a fix, read the official docs for the version actually installed. If a fix breaks something, reproduce the problem and read the full error before changing more code.

Never call the audit complete while a 🔴 item is FAIL or an unresolved CAN'T TELL, unless the user explicitly accepts the risk. Record that acceptance in the report.
