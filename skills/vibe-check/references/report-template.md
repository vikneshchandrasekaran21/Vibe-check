# Report template

Use this structure. Keep it skimmable. Plain words first, technical details second.

````markdown
# vibe-check report: <app name>

> ⬆️ **A newer vibe-check is out** (v<latest>; this check ran on v<installed>). <update step for this tool, from SKILL.md Step 0>, then start a new session. *(Only if Step 0 found a newer version.)*

> **Update check:** couldn't connect here. Latest release: https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest · <update step for this tool>. *(Only if Step 0 couldn't connect; leave out if up to date or turned off.)*

**vibe-check:** v<installed> · **Date:** <date> · **Level:** Quick | Full | Enterprise · **Profile:** <users, minors?, payments?, sensitive data?, regions> · **Stack:** <framework, DB, auth, hosting, payments, AI>
**Modules run:** <list> · **Method notes:** <e.g. "license scan via lockfile (scanner blocked)", "click-through via Playwright on staging">

## Verdict: 🟢 SHIP | 🟡 SHIP AFTER FIXES | 🔴 DO NOT SHIP

<One or two sentences explaining why. Example: "Any logged-in user can read every other user's invoices, and the Stripe secret key is in the browser bundle. Fix these two before launch; the rest can follow.">

**Score:** <passed> / <applicable> checks passed · 🔴 <n> blockers · 🟡 <n> to fix before scale · ❓ <n> questions

## 🔴 Blockers: fix before launch

### 1. <Short title> · ✅ Confirmed | 🔎 Likely
- **What could happen:** <one plain sentence about the impact on the user or their customers>
- **Where:** `path/to/file.ts:42`
- **Evidence:** <the exact proof, quoted; secrets masked>
  ```ts
  // path/to/file.ts:40-44 (re-read just before writing this report)
  const invoice = await db.invoice.findUnique({ where: { id: params.id } });
  return Response.json(invoice);
  ```
  <or: `$ curl -sI http://example.com` → `HTTP/1.1 200 OK` (no redirect to HTTPS)>
- **Ruled out:** <what the second look checked, e.g. "No ownership check in middleware.ts or the RLS policy for invoices">
- **Fix:** <the specific technical change> · **Safe to auto-fix:** yes / no (needs your decision)
- **Prompt to fix it:**
  > <A ready-to-paste instruction for an AI coding tool, specific to this codebase. Example: "In app/api/invoices/[id]/route.ts, only return the invoice if invoice.user_id equals the current session user's id; return 404 otherwise. Add a test proving user A cannot fetch user B's invoice.">

<repeat>

## 🟡 Fix before scale or paying users

| # | Issue | Confidence | Where + evidence | Fix | Safe to auto-fix |
|---|---|---|---|---|---|
| 1 | | ✅ / 🔎 | `file:line`, quoted line or command output | | |

## ❓ Questions for you

Includes every ❓ **Needs checking** item: what we couldn't confirm, why, and exactly how to check it.

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

## 🧭 Coverage

*Pasted from `coverage.py` (counted from the ledger, not estimated). Ledger: `.vibe-check/reports/YYYY-MM-DD-ledger.md`.*

| Module | Status | Checks | ✅ Pass | ❌ Fail | ➖ N/A | ❓ Can't tell | Not done |
|---|---|---|---|---|---|---|---|
| blind-spots | ✅ | 18 | 15 | 2 | 1 | 0 | 0 |
| security | ✅ | 64 | | | | | |
| reliability | ✅ | 51 | | | | | |
| devops | ◐ | 40 | | | | | |
| functional-qa | ◐ | 40 | | | | | |
| legal-privacy | ✅ | 35 | | | | | |
| launch-ux | ✅ | 29 | | | | | |
| platforms | ✅ | 51 | | | | | |
| lawsuits | ✅ | 14 | | | | | |
| supply-chain | ✅ | 22 | | | | | |
| vulnerabilities | ✅ | 15 | | | | | |
| maintainability | ✅ | 16 | | | | | |
| <each profile module> | ✅ / ➖ | | | | | | |
| **Total** | | | | | | | |

**Why ◐ or ❌, and the method per module:**
- devops ◐: <e.g. "backups, MFA and billing alerts are dashboard settings: see questions">
- functional-qa ◐: <e.g. "static review of every handler; no browser run: `npx playwright test` to complete">
- <profile module> ➖: <reason, e.g. "no health data">

**Inventory** (from `inventory.py`, plus anything added by hand):

| Category | Checked / found |
|---|---|
| Pages and screens | 23/23 |
| API routes and endpoints | 47/47 |
| Server actions · functions · webhooks · cron | |
| Forms · buttons and links | |
| Env vars · tables · storage buckets · file uploads | |
| Payments · email · AI calls · third-party scripts | |

**Sweep** (from `sweep.py`, every file + git history): <N> hits → <F> findings, <R> ruled out after the second look.

**Known vulnerabilities** (from `versions.py` and the audit tools; every verdict links the source opened in this run):

| Component | Version | Status | Advisory / end-of-life | Fixed in / workaround | Source |
|---|---|---|---|---|---|
| PHP (Dockerfile:3) | 8.3.35 | 🔴 VULNERABLE · ⚠️ actively exploited | CVE-… (on CISA KEV) | 8.3.36; workaround quoted from the advisory | <URL opened today> |
| Node.js (.nvmrc) | 16 | 🔴 EOL | end-of-life since <date> | move to a supported LTS | <endoflife.date URL> |
| next (package-lock.json) | 13.4.1 | 🟡 OUTDATED | GHSA-… (high, not reachable: <why>) | 14.x | `npm audit --omit=dev` |
| <every other component> | | ✅ CURRENT | | | <URL or tool> |

**Tools run:**

| Tool | Command | Result |
|---|---|---|
| Package audit | `npm audit --omit=dev` | 2 high (see 🔴 2) |
| Type-check | `npx tsc --noEmit` | 0 errors |
| Lint · tests · build | `npm run lint` · `npm test` · `npm run build` | <result, or "no test script"> |
| Secret scanner | `gitleaks detect` | not installed: used `sweep.py --history` |

## Not checked

- <Areas or commands skipped, why, and the exact command for the user to run, e.g. "Build not run (shared folder in use): run `npm run build`".>

## 🏁 Score card

```text
vibe-check: 🟢 SHIP · 112/118 checks · 0 blockers · Full check · 13 Nov 2026
```

*The numbers come from `coverage.py`'s score line: passed / applicable checks, and 🔴 FAILs as blockers.*

<only if 🟢: the badge snippet and the ⭐ line, see below>

---
<sub>Checked with vibe-check · github.com/vikneshchandrasekaran21/Vibe-check</sub>
````

## Writing tips

- Order blockers by severity: data leaks and account takeover first, then money loss, then legal, then outages.
- One finding per real problem. Group repeats (for example, "12 routes are missing ownership checks", with all 12 listed).
- For dependency findings, give the advisory ID, installed version and fixed version.
- Never print a full secret.
- Only ✅ Confirmed and 🔎 Likely findings go in Blockers or Fix before scale. ❓ items are questions.
- Legal and policy statements cite the skill module or a URL opened in this run, never general memory. Show its first 4 characters and its location.
- If something is fine, don't invent a problem to look thorough.

## Score card, badge and footer

These go at the very end of the saved report **and** the chat summary.

### Score card (always)
One line, in a `text` code block, so it screenshots cleanly:

`vibe-check: <🟢 SHIP | 🟡 SHIP AFTER FIXES | 🔴 DO NOT SHIP> · <passed>/<applicable> checks · <n> blockers · <Quick check|Full check|Enterprise check> · <D Mon YYYY>`

- `passed / applicable` counts only items marked PASS out of items that weren't N/A. CAN'T TELL counts as not passed.
- **Never include** findings, secrets, private URLs, file paths, or the app name, unless the user asks for the app name. The card is meant to be shared publicly.
- If the score improved since the last report in `.vibe-check/reports/`, add the change: `· was 🔴 71/118`. Before-and-after posts are the most shared.

### Badge (only for 🟢 SHIP on a Full or Enterprise check)
Offer this snippet for the user's README. **Don't add it yourself** unless the user says yes (scope guard):

```markdown
[![vibe-checked](https://img.shields.io/badge/vibe--checked-%E2%9C%85%20SHIP%20<passed>%2F<applicable>-brightgreen)](https://github.com/vikneshchandrasekaran21/Vibe-check)
```

Replace `<passed>` and `<applicable>` with the numbers (`%2F` is the slash).

### Star request (only for 🟢, once)
One line, after the badge: *"If vibe-check helped, a ⭐ on https://github.com/vikneshchandrasekaran21/Vibe-check helps others find it."* Don't repeat it in the same session, and never show it for 🟡 or 🔴.

### Footer (always, removable)
The last line of the saved report: `<sub>Checked with vibe-check v<installed> · latest: github.com/vikneshchandrasekaran21/Vibe-check/releases/latest · update: <update step for this tool></sub>`. Leave it out if the user has asked for no footer (or `.vibe-check/config` contains `footer: false`). Never add it to the user's app, pages or code, only to the report.
