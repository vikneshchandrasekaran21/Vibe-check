# Report template

Use this structure. Keep it skimmable. Plain words first, technical details second.

````markdown
# vibe-check report: <app name>

**Date:** <date> · **Level:** Quick | Launch | Enterprise · **Profile:** <users, minors?, payments?, sensitive data?, regions> · **Stack:** <framework, DB, auth, hosting, payments, AI>
**Modules run:** <list> · **Method notes:** <e.g. "license scan via lockfile (scanner blocked)", "click-through via Playwright on staging">

## Verdict: 🟢 SHIP | 🟡 SHIP AFTER FIXES | 🔴 DO NOT SHIP

<One or two sentences explaining why. Example: "Any logged-in user can read every other user's invoices, and the Stripe secret key is in the browser bundle. Fix these two before launch; the rest can follow.">

**Score:** <passed> / <applicable> checks passed · 🔴 <n> blockers · 🟡 <n> to fix before scale · ❓ <n> questions

## 🔴 Blockers: fix before launch

### 1. <Short title>
- **What could happen:** <one plain sentence about the impact on the user or their customers>
- **Where:** `path/to/file.ts:42` <and the evidence: snippet, command output or config value; secrets masked>
- **Fix:** <the specific technical change> · **Safe to auto-fix:** yes / no (needs your decision)
- **Prompt to fix it:**
  > <A ready-to-paste instruction for an AI coding tool, specific to this codebase. Example: "In app/api/invoices/[id]/route.ts, only return the invoice if invoice.user_id equals the current session user's id; return 404 otherwise. Add a test proving user A cannot fetch user B's invoice.">

<repeat>

## 🟡 Fix before scale or paying users

| # | Issue | Where | Fix | Safe to auto-fix |
|---|---|---|---|---|
| 1 | | | | |

## ❓ Questions for you

Things that can't be checked from the code. Answer these and I'll update the report.

1. <Example: "Have you ever restored a backup to check it works?">
2. <Example: "Which countries are your users in? This decides which privacy laws apply.">

## ⚖️ Needs a lawyer

| Topic | Why | What to ask |
|---|---|---|
| | | |

## ✅ What passed

- <Check>: <evidence>

## 💡 Other suggestions (not changed)

- <Improvements you noticed that aren't launch issues. Listed only; never applied without being asked.>

## Not checked

- <Areas or commands skipped, why, and the exact command for the user to run, e.g. "Build not run (shared folder in use): run `npm run build`".>
````

## Writing tips

- Order blockers by severity: data leaks and account takeover first, then money loss, then legal, then outages.
- One finding per real problem. Group repeats (for example, "12 routes are missing ownership checks", with all 12 listed).
- For dependency findings, give the advisory ID, installed version and fixed version.
- Never print a full secret. Show its first 4 characters and its location.
- If something is fine, don't invent a problem to look thorough.
