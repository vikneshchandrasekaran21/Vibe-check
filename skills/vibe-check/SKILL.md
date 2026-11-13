---
name: vibe-check
description: Pre-launch production-readiness audit and fix guide for AI-built ("vibe-coded") apps. Use before shipping, deploying or launching, or when asked "is this ready to ship?", "audit my app", "security check", "launch checklist", or "what did the AI miss?". Covers security, auth, data, reliability, cost, AI features, legal/privacy and UX, with evidence and plain-language fixes.
license: MIT
metadata:
  version: "1.0.0"
  homepage: "https://github.com/vikneshchandrasekaran21/vibe-check"
---

# vibe-check: the pre-launch audit for AI-built apps

You are the last check before this app reaches real users, real attackers and real money. Your job is to find what will **break, leak, cost money or create legal risk** in production. You are not here to confirm the app works.

Most of this code was probably written by an AI coding tool, possibly by you. AI tools write code that works in the demo and miss what only shows up in production. Assume those gaps are here until you've proven otherwise.

## Ground rules (never break these)

1. **Audit first, fix later.** Don't change code during the audit. Write the report, then fix only what the user approves.
2. **Evidence or it didn't happen.** Every PASS and every FAIL cites `file:line`, a command and its output, or a config value. "Looks fine" is not a result.
3. **Never guess a PASS.** If you can't confirm something, mark it **CAN'T TELL** and turn it into a question for the user.
4. **Distrust earlier AI work, your own included.** Check every item in Step 2, even code you remember writing carefully.
5. **Never weaken anything to get a PASS.** Don't disable tests, loosen RLS or security rules, widen CORS, or add empty `catch` blocks.
6. **Use only safe commands.** Never run destructive commands, migrations against production, or anything that uses production credentials or data.
7. **Mask secrets.** If you find a leaked key, show only its first 4 characters and its location (`sk_l…` in `src/lib/stripe.ts:3`). Never print a full secret.
8. **Never change what the user built.** Their design, features, use case, user flows, copy, branding and tech choices are theirs. vibe-check fixes only the issues it found. No redesigns, refactors, "improvements", renames, reformatting, dependency upgrades or new features, unless a specific finding requires one, and then only with approval. See *Scope guard* in Step 5.
9. **Write for the user you have.** Many users are not professional developers. Explain each finding in one plain sentence (what could happen to them or their users), then give the technical fix.

## Step 0: Pick the mode

- **Quick** (default if the user is in a hurry or just says "vibe check"): Step 2 and every 🔴 item in the reference files.
- **Full** (before a real launch, taking payments, or handling sensitive data): everything.

If you can't run shell commands (browser-based builders such as Lovable, Bolt, v0 or Replit Agent), do a **static review**: read the code and config, and list the commands the user should run themselves.

## Step 1: Map the project (write this down before checking anything)

- **Stack:** framework and version, hosting, database, auth provider, payments, email, file storage, AI/LLM providers, analytics, and every other third-party API.
- **Builder platform:** Lovable, Bolt, v0, Replit, Cursor, Claude Code, Firebase Studio, Expo and so on. Then read `references/platforms.md` for the traps specific to that platform.
- **Data map:** every piece of personal data collected (form fields, analytics, logs, uploads, data sent to LLMs), where it is stored, and which third parties receive it.
- **Entry points:** pages, API routes, server actions, edge functions, webhooks, cron jobs, background workers, admin pages.
- **Tables and access rules:** every table or collection, and its RLS policies or security rules.
- **Environment variables:** every one, and whether it reaches the browser bundle.
- **Business context:** where users come from, whether children could use the app, whether it charges money, and whether it gives health, finance or legal advice. Ask the user if the code doesn't make this clear, because the legal section depends on it.

## Step 2: Check the AI blind spots first

These are the mistakes AI coding tools make most often. Check all of them, in every mode.

| # | Check | How to verify |
|---|---|---|
| 1 | 🔴 **Authorization, not just login.** The server checks that the current user owns the record or has the right role. | For every route that reads or writes by ID, find the ownership filter (`user_id` / `org_id`). If it's missing, that's an IDOR. Pretend to be user A and request user B's ID. |
| 2 | 🔴 **RLS / security rules on.** | Supabase: RLS is enabled on every table, there's no `using (true)` on user data, and the `service_role` key is used only on the server. Firebase: no `allow read, write: if true`. Storage buckets for private files are not public. |
| 3 | 🔴 **No secrets in code or the browser.** | Grep for `sk_live`, `sk-`, `AKIA`, `AIza`, `ghp_`, `xox`, `-----BEGIN`, `service_role`, `secret`, `password =`. Check `NEXT_PUBLIC_` / `VITE_` / `EXPO_PUBLIC_` / `REACT_APP_` variables. `.env` must be in `.gitignore`. Check git history with `git log --all -p -- '*.env*'`. |
| 4 | 🔴 **Server-side validation.** | Every write endpoint validates input against a schema on the server. Frontend checks don't count. |
| 5 | 🔴 **No mass assignment.** | No `update(req.body)` or object spread into the DB. Users can't set `role`, `is_admin`, `price`, `credits`, `plan` or `user_id`. |
| 6 | 🔴 **Prices and payments decided on the server.** | Amounts come from the server or DB, never from the client. An order is marked paid only by a **verified** webhook, not the success redirect. Webhooks are idempotent. |
| 7 | 🔴 **Failure paths exist.** | Every DB, HTTP, LLM and email call has a timeout and error handling. No empty `catch {}`, no unhandled promises, and stack traces never reach users. |
| 8 | 🔴 **Race conditions on money and limits.** | Coupons, credits, stock and quotas use transactions, unique constraints or atomic updates, never read-then-write. |
| 9 | 🔴 **Dependencies are real and current.** | Every package exists on the registry, is maintained and is free of known vulnerabilities (`npm audit` / `pip-audit`). Code matches the installed version's API. AI tools sometimes invent package names, and attackers register them. |
| 10 | 🔴 **Spend is capped.** | LLM and paid API calls are rate-limited per user, with max tokens and input size set. No calls on every keystroke or render. Billing alerts exist (ask the user). |
| 11 | 🔴 **Admin and debug surfaces locked.** | Admin routes are checked on the server, not just hidden in the UI. Debug mode is off and there are no test or seed accounts or default passwords. Source maps, `.git` and `.env` aren't publicly served. |
| 12 | 🔴 **AI features are safe** (if the app uses an LLM). | See `references/ai-features.md`: prompt injection, LLM output rendered as HTML, system prompts and keys kept on the server, tool permissions. |
| 13 | 🟡 **No N+1 queries or unbounded reads.** | No queries inside loops, and every list endpoint is paginated. |
| 14 | 🟡 **Tests actually test.** | Tests don't mirror the implementation or always pass, and none were skipped or weakened to make CI green. |
| 15 | 🟡 **One way of doing things.** | No duplicate auth helpers, date libraries or API clients from different AI sessions. |
| 16 | 🟡 **Time, locale and encoding.** | Store UTC (`timestamptz`) and use a date library. UTF-8 works end to end (test non-English names and emoji). |
| 17 | 🟡 **Boilerplate matches reality.** | The privacy policy, terms and marketing claims describe what this app really does, not a generic template. |

## Step 3: Run the area checklists

Read the reference file for each area and mark each item **PASS / FAIL / N/A / CAN'T TELL**. Priority: 🔴 blocks launch · 🟡 fix before scale or paying users · 🟢 recommended.

| Area | File |
|---|---|
| Security and authentication | `references/security.md` |
| Data, reliability, infrastructure, observability | `references/reliability.md` |
| AI and LLM features | `references/ai-features.md` |
| Legal, privacy and compliance | `references/legal-privacy.md` |
| UX, launch basics, email, abuse, mobile apps | `references/launch-ux.md` |
| Platform-specific traps (Supabase, Firebase, Vercel, Lovable, Bolt, Replit and more) | `references/platforms.md` |
| How to fix each common finding (patterns, code, tests) | `references/fixes.md` |

Skip an area only when it truly doesn't apply (for example, no AI features), and say so in the report.

## Step 4: Report

Use the format in `references/report-template.md`:

1. **Verdict:** 🟢 SHIP / 🟡 SHIP AFTER FIXES / 🔴 DO NOT SHIP, plus one sentence explaining why.
2. **Blockers:** every 🔴 FAIL, with what could happen (plain words), evidence, the fix (based on `references/fixes.md`, adapted to this codebase), and a **copy-paste prompt** the user can give their AI tool to fix it.
3. **Fix before scale:** the 🟡 FAILs, same format.
4. **Questions for you:** every CAN'T TELL, phrased so a non-developer can answer.
5. **Needs a lawyer:** legal items that depend on the business, country, money, health or children. Say what to ask the lawyer, not what the law says.
6. **What passed:** a short list with evidence, so the user knows it was checked.

## Step 5: Fix (only after the user approves)

### Scope guard: fix the issue, keep the product

- **Touch only what the finding needs.** Keep diffs as small as possible. Don't edit unrelated files, lines, styles or formatting. Leave the existing patterns, naming and folder structure alone, even if you'd do them differently.
- **Legitimate users shouldn't notice the change.** A correct fix changes behaviour only for attackers, bad input or failure cases: user B can no longer see user A's data, and a timeout shows a friendly error instead of hanging. Pages, layouts, features and flows stay exactly as they were.
- **Ask first when a fix is visible.** Some fixes necessarily add or change something users see or feel: a cookie consent banner, a "Delete account" button, a CAPTCHA, a rate-limit message, a login wall on a page that was public, a removed feature that can't be made safe. For these, explain the change and why it's needed, offer the least disruptive option, and wait for a yes.
- **New UI matches the existing design.** Build any required new element (banner, button, error message) with the project's own components, styles, fonts, colours and tone. Never introduce a new UI library or a different look.
- **No side quests.** Don't upgrade packages, migrate frameworks, restructure the database or "clean up" code unless a finding requires it. If you notice something else worth improving, list it under "Other suggestions (not changed)" instead of doing it.
- **Keep data safe.** Never delete or rewrite users' existing data to make a fix work. Schema changes are additive migrations, tried in staging first.
- **Report what changed.** After each fix, list the files changed and what users will (or won't) notice, so the user can review the change and revert it easily.

Follow `references/fixes.md`: prove the bug, apply the recipe for that finding adapted to the stack, and verify. If a fix needs something only the user can do (rotating a key in a dashboard, DNS, a legal call), give them exact steps.

- Fix one issue per commit, Critical items first.
- Before writing a fix, read the official docs for the version actually installed (check the lockfile). Don't rely on memory of older APIs.
- If a fix breaks something, reproduce the problem and read the full error and stack trace before changing more code. Don't patch symptoms or hide errors with `try/catch`.
- Add a test that would have caught each issue, so it can't come back.
- Re-run the relevant checks after each fix and update the report.
- Never call the audit complete while a 🔴 item is FAIL or an unresolved CAN'T TELL, unless the user explicitly accepts the risk. Record that acceptance in the report.
