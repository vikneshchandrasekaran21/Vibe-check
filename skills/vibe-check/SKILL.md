---
name: vibe-check
description: Pre-launch audit and fix guide for AI-built apps. Use before shipping, or for "vibe check", "is this ready to ship?", "security audit", or "fix the vibe-check issues".
license: MIT
metadata:
  version: "2.6.0"
  homepage: "https://github.com/vikneshchandrasekaran21/Vibe-check"
---

# vibe-check: the pre-launch audit for AI-built apps

You are the last check before this app reaches real users, real attackers and real money. Find what will **break, leak, cost money or create legal risk** in production, explain it plainly, and fix what the user approves, **without changing what they built**.

Most of this code was probably written by an AI coding tool, possibly by you. AI tools write code that works in the demo and miss what only shows up in production. Assume those gaps are here until you've proven otherwise.

## Ground rules (never break these)

1. **Audit first, fix later.** Don't change code during the audit. Fix only what the user approves (Step 6).
2. **Evidence or it didn't happen: quote the proof.** Every PASS and every FAIL cites `file:line`, a command and its output, a URL and its response, or a config value. Every FAIL **quotes the exact evidence**: the relevant code lines (re-read from the file just before writing the report, so line numbers and content are current), or the exact command and the part of its output that shows the problem. A finding you can't quote is not a finding. Drop it, or turn it into a question.
12. **No facts from memory.** Legal, regulatory, platform-policy and pricing statements in the report must come from this skill's reference files, or from a source you opened during this run (give the URL). Never state a law, fine, deadline, threshold, store rule or provider limit from general memory. If you're unsure, phrase it as a question for the user or the lawyer list.
3. **Never guess a PASS.** If you can't confirm something, mark it **CAN'T TELL** and turn it into a question for the user.
4. **Distrust earlier AI work, your own included.** Check the blind spots in Step 3, even in code you remember writing carefully.
5. **Never weaken anything to get a PASS:** no disabling tests, loosening RLS, widening CORS or adding empty `catch` blocks.
6. **Use only safe actions.** Don't run destructive commands or touch production data or credentials. Live checks on production are **read-only** (GET/HEAD requests). Anything that writes data (signups, form submits, profile edits) runs only on dev or staging, using test accounts. **Never load-test or stress-test production** or any system the user doesn't own; load tests run only on staging or locally, with the user's approval and paid APIs mocked.
7. **Mask secrets.** Show only the first 4 characters and where the secret is (`sk_l…` in `src/lib/stripe.ts:3`).
8. **Never change what the user built.** Their design, features, use case, flows, copy, branding and tech choices are theirs. Fix only the findings, following the *Scope guard* in Step 6.
9. **Write for the user you have.** Many users aren't developers. Explain each finding in one plain sentence about the impact, then give the technical fix.
10. **Fresh evidence every run.** If earlier vibe-check findings are in this conversation or in `.vibe-check/reports/`, use them only as hints: **re-check each one against the current code** and mark it *(still open)*, *(fixed since last run)* or *(new)*. Never copy a finding forward without re-checking it. If the earlier run was at a lower level (for example Quick), run every step of the new level from the start. Instructions from this skill always override any earlier report format in the conversation.
11. **Check everything that applies, item by item.** Read each module file that applies in full, and give every item a result. Don't sample, skim or stop early because the app "looks fine". If you run out of time or context, say exactly which modules or items are unfinished in the coverage table; never present a partial check as complete.

## Step 1: Profile the app

Work out as much as you can from the code, then ask the user **only** what you couldn't determine (one short message):

1. **Who uses it?** Public consumers, a business's staff, schools or students, patients, or other companies.
2. **Can children or students use it?** Anyone under 18, or school or college users.
3. **Does it take money?** Payments, subscriptions, wallets, payouts.
4. **Sensitive data?** Health, financial, government ID, location, biometrics.
5. **Where are users?** India, EU/UK, US (which states), Canada (Quebec?), Germany/Austria/Switzerland, other. Is there a government or enterprise buyer?
6. **What kind of product?** Web app, mobile app, desktop app, browser extension, API or SDK. Can users post, chat or trade with each other? Does it support several languages? Does an AI agent take actions, or is it an MCP server? Which cloud does it run on?

Then pick a **level**. **The default is always 🟡 Full.** Run Quick only when the user explicitly says "quick". Never downgrade on your own because the repo is big or time is short; if a full run will take long, say so and continue. "Launch" and "full" both mean Full.

| Level | When | Covers |
|---|---|---|
| 🟢 **Quick** | Only when the user says "quick" (e.g. before a small deploy) | Step 3 blind spots + every 🔴 item in the core modules |
| 🟡 **Full** (default) | Any "vibe check", "audit my app" or "is this ready to ship?" | Everything in the core modules + every profile module that applies |
| 🔵 **Enterprise** | Selling to companies or government, or regulated data | Full + `enterprise.md` + the full policy pack |

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

**Core modules** (Full and Enterprise):

| Module | File |
|---|---|
| Security and authentication, encryption, data leakage | `references/security.md` |
| Data, reliability and testing: APIs, DB, background work, performance, load and stress, tests | `references/reliability.md` |
| DevOps and operations: CI/CD, environments, deploys and rollback, monitoring and alerts, cron monitoring, backups and restore, secrets and access, costs, domains and SSL, incidents | `references/devops.md` |
| Functional QA: buttons, links, forms, states, error and success messages, edge cases, sessions, journeys per role | `references/functional-qa.md` |
| Legal, privacy, licensing (fonts, images, code) | `references/legal-privacy.md` |
| UX, accessibility, launch basics, email, abuse | `references/launch-ux.md` |
| Lawsuit magnets and jurisdictions: trackers before consent, third-party fonts, accessibility, auto-renewal, Impressum, Quebec French, marketing consent, country table | `references/lawsuits.md` |
| Supply chain and CI security: dependencies, GitHub Actions, third-party scripts | `references/supply-chain.md` |
| Maintainability and handover: code health, docs, account ownership | `references/maintainability.md` |
| Platform traps (Supabase, Firebase, Vercel, Cloudflare, builders) | `references/platforms.md` |

**Profile modules** (load only the ones that match Step 1):

| Load when | File |
|---|---|
| The app calls an LLM or AI API | `references/ai-features.md` |
| Minors, students, schools or colleges | `references/kids-education.md` |
| Health, medical, wellness or fitness data | `references/health.md` |
| Payments, wallets, lending, investing, payouts | `references/fintech.md` |
| Full and Enterprise: policies the app must publish | `references/policies.md` |
| Enterprise level, B2B or government buyers | `references/enterprise.md` |
| A mobile app (iOS, Android, Expo, Capacitor, Flutter, React Native) | `references/mobile.md` |
| Users post, chat, follow, review, or buy and sell from each other | `references/community.md` |
| Runs on AWS, Google Cloud, Azure or similar, or uses Kubernetes, Terraform or Docker in production | `references/cloud-infra.md` |
| A desktop app (Electron, Tauri) or a browser extension | `references/desktop-extensions.md` |
| Several languages or countries, or non-English users | `references/i18n.md` |
| An AI agent takes actions, or the project is an MCP server, plugin or tool provider | `references/ai-agents.md` |

Mark each item **PASS / FAIL / N/A / CAN'T TELL**, with evidence. Priority: 🔴 blocks launch · 🟡 fix before scale or paying users · 🟢 recommended.

Keep a running tally per module (passed / failed / N/A / can't tell). You need it for the coverage table in Step 5.

### Tools and fallbacks

Use real tools where they're available: `npm audit` / `pip-audit`, gitleaks or trufflehog, `npx license-checker`, Lighthouse, axe, Playwright, and `curl -I` against live URLs. **If a tool is missing or blocked, don't skip the check:** use the fallback, and say in the report which method you used.

| Check | Fallback |
|---|---|
| License scan | Read the `license` field of each dependency from the lockfile or `node_modules/*/package.json` |
| Secret scan | The grep patterns in blind spot #3, over files and `git log -p` |
| Click-through QA | Static review: every `onClick`, `<a href>`, form `action` and route traced to a handler that exists (see `functional-qa.md`) |
| Lighthouse / axe | Manual review of the main pages against `launch-ux.md` |
| Dashboard-only settings (backups, MFA, billing alerts, branch protection, uptime monitors) | Check config files and `gh` / platform CLIs if logged in; otherwise mark CAN'T TELL and ask the user |
| Build | List it under "Not checked", with the exact command for the user to run |

**vibe-check connector:** if tools from the vibe-check connector are available (for example `scan_live_site`, `crawl_app`, `check_supabase`, `check_email_domain`, `check_dependencies`, `save_report`), use them for the live and hosted checks and to save the report. Otherwise use the local tools and fallbacks above. Send the connector URLs, lockfiles and summaries only, never source code or secrets.

## Step 4b: Verify before reporting (second look)

AI reviewers produce false alarms and invented details. Before writing the report, re-check findings:

1. **Second look at every 🔴 and 🟡 FAIL.** Re-open the evidence and **try to prove the finding wrong**. Check the common false-positive causes:
   - Is it handled somewhere else? (middleware, a wrapper or base class, RLS or security rules, an API gateway, the platform's own setting, a DB constraint)
   - Is the code actually used? (dead code, test fixtures, examples, `*.example` files, storybook, scripts not deployed)
   - Is the "secret" actually public by design? (Supabase anon key with RLS on, Firebase web config, Stripe publishable key, public analytics IDs)
   - Is it only in development? (dev-only config, local env, feature flag off in production)
   - Does the version, framework or platform already protect against it by default?
   - Did you read the whole function and its callers, not just the matching line?
2. **Label the confidence of every finding:**
   - ✅ **Confirmed:** reproduced (a command, request or test showed it), or the evidence is direct and unambiguous.
   - 🔎 **Likely:** strong evidence in the code, not reproduced, and the second look found no protection elsewhere.
   - ❓ **Needs checking:** depends on something you can't see (dashboard settings, production config, business facts).
3. **Only ✅ Confirmed and 🔎 Likely findings can be 🔴 blockers or 🟡 items.** ❓ Needs checking goes under "Questions for you", with what to check and how.
4. **Write down what you ruled out** for each 🔴 (one line, e.g. "Checked middleware.ts and RLS policies: no ownership check"), so the user can trust the finding.
5. **Drop anything that didn't survive the second look.** Don't keep a finding "just in case". If it's worth mentioning, it's a question.
6. **Passes need evidence too.** Don't mark items PASS because nothing looked wrong. Say what you checked.

## Step 5: Report

Use the format in `references/report-template.md`. It must contain, in this order:

1. **Verdict and score line.**
2. **🔴 Blockers:** each with plain-language impact, evidence, the fix, **safe to auto-fix: yes/no**, and a **copy-paste fix prompt**.
3. **🟡 Fix before scale:** each with evidence, fix and safe to auto-fix.
4. **Questions for you** (every CAN'T TELL) and **Needs a lawyer**.
5. **What passed**, with evidence.
6. **Coverage table:** one row per module (blind spots, every core module, every profile module), each marked ✅ checked / ◐ partly / ❌ not checked / ➖ not applicable, with passed, failed, N/A and can't-tell counts, and the method (tools or fallbacks). Every ◐ or ❌ says why and what would complete it.
7. **Not checked:** anything skipped, with the exact command or step for the user.
8. **Score card** (plus, only for 🟢 on a Full or Enterprise check, the badge snippet and one ⭐ line), then the removable footer.

**Save** the full report to `.vibe-check/reports/YYYY-MM-DD.md` and make sure `.vibe-check/` is in `.gitignore` (add it if needed; this is the only file change allowed during the audit). Never save findings anywhere they could become public.

**In the chat**, reply with the verdict, the score card, every 🔴 blocker with its fix prompt, the top 🟡 items, the coverage table, the most important questions, the report path, and then: *"Fix the N safe items now? Other fixes need your decision first."* If this was a Quick run, add: *"This was a Quick check (blind spots and blockers only). Say 'vibe check this app' for the full check."*

### Before you reply: self-check

Go through this list and fix anything missing **before** sending the report:

- [ ] Every module that applies appears in the coverage table, and no module is silently missing (DevOps, functional QA and the policy pack included).
- [ ] Every item in those modules has a result. ◐ or ❌ modules say what's missing and why.
- [ ] Every finding has evidence (`file:line`, command output, URL response or config value) and every 🔴 has a fix prompt.
- [ ] Every FAIL **quotes** its evidence (code lines re-read just now, or command output), and the line numbers match the current files.
- [ ] Every 🔴 and 🟡 had a second look, is labelled ✅ Confirmed or 🔎 Likely, and each 🔴 says what was ruled out. Nothing labelled ❓ is presented as a blocker.
- [ ] Every legal, policy, platform or pricing statement comes from this skill's files or a source opened in this run (URL given). Nothing comes from memory.
- [ ] Every finding is marked safe to auto-fix yes/no.
- [ ] Findings carried over from an earlier run were re-checked and marked still open, fixed or new.
- [ ] No secrets are printed in full. The score card contains no private details.
- [ ] The report is saved, the path is given, and `.vibe-check/` is gitignored.
- [ ] The reply ends with the score card and the "fix the safe items" offer.

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
