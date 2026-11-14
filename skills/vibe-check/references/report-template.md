# Report template

<!-- contents: kept up to date by scripts/build.py -->
## Contents
- The six symbols (everywhere: report, chat, fixes)
- While it runs (progress)
- In the chat (the one-screen summary)
- Fix plan (before anything changes)
- Fix card (one per fix)
- Finish line
- Writing tips
- Score card, badge and footer
  - Score card (always)
  - Badge (only when there are no blockers, on a Full or Enterprise check)
  - Star request (only for 🟢, once)
  - Footer (always, removable)
<!-- /contents -->

Use this structure. Keep it skimmable. Plain words first, technical details second.

````markdown
# vibe-check report: <app name>

> ⬆️ **A newer vibe-check is out** (v<latest>; this check ran on v<installed>). <update step for this tool, from SKILL.md Step 0>, then start a new session. *(Only if Step 0 found a newer version.)*

> **Update check:** couldn't connect here. Latest release: https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest · <update step for this tool>. *(Only if Step 0 couldn't connect; leave out if up to date or turned off.)*

**vibe-check:** v<installed> · **Skill files:** complete | checklists read from GitHub, scripts done by hand · **Date:** <date> · **Level:** Quick | Full | Enterprise · **Profile:** <users, minors?, payments?, sensitive data?, regions> · **Stack:** <framework, DB, auth, hosting, payments, AI>
**Modules run:** <list> · **Method notes:** <e.g. "license scan via lockfile (scanner blocked)", "click-through via Playwright on staging">

**How to read this:** ✅ passed or fixed · ❌ must fix before launch · ⚠️ fix before you scale · ❓ needs your answer · ➖ doesn't apply to this app · 🔧 being fixed. *(❗ appears only if something wasn't checked.)*

## Result

*Paste the `## Result` block exactly as `coverage.py` printed it: the verdict and score line, the "Since last check" line when there's an earlier run, the totals table and the area scorecard. Never type these numbers.*

**🔴 DO NOT SHIP · Score 69/100 (capped: 2 blockers open) · Needs work**

Since last check (2026-11-02): Score 58 → 69 (+11) · ✅ 7 fixed · 🆕 1 new · ↩️ 0 came back · ❓ 2 answered

| Checks | Count |
|---|---|
| In vibe-check | 653 |
| ➖ Don't apply to this app | 412 |
| **Apply to this app** | **241** |
| ✅ Passed | 198 |
| ❌ Must fix (blockers) | 2 |
| ⚠️ Should fix | 29 |
| ❓ Need your answer | 12 |
| **Checked** | **241 of 241** · ✅ nothing skipped |

| Area | Score | Passed | ❌ Must fix | ⚠️ Should fix | ❓ Your answer |
|---|---|---|---|---|---|
| AI blind spots | `████████░░` 84 | 16/19 | ❌ 1 | ⚠️ 1 | ❓ 1 |
| Security | `███████░░░` 74 | 62/80 | ❌ 1 | ⚠️ 11 | ❓ 6 |
| Payments | `█████████░` 92 | 11/12 | — | ⚠️ 1 | — |
| Privacy & legal | `██████░░░░` 63 | 30/44 | — | ⚠️ 10 | ❓ 4 |
| Reliability & ops | `████████░░` 81 | 39/46 | — | ⚠️ 6 | ❓ 1 |
| Launch & UX | `█████████░` 95 | 40/40 | — | — | — |
| AI features | ➖ doesn't apply | | | | |

**Why:** <one or two plain sentences. Example: "Any logged-in user can read every other user's invoices, and the Stripe secret key is in the browser bundle. Fix these two before launch.">

**Score and bands:** blocker checks count 3, should-fix checks 2, nice-to-have checks 1; checks that don't apply don't count, and a ❓ counts as not passed yet. While any ❌ blocker is open the score can't go above 69. 90–100 Ready to scale · 75–89 Ready to launch · 60–74 Needs work · 0–59 Not safe for real users yet.

## 🔀 Your answers vs your code
*Only when an answer and the code disagree (from `.vibe-check/profile.md`). The code wins: these modules ran anyway.*
- You said **no payments**, but `lib/pricing.ts:2` links to a Razorpay checkout (`rzp.io/l/pro-plan`). Payment checks ran.
- You said **no children**, but `app/signup/page.tsx:2` asks for a date of birth. The children's checks ran, and the legal question is under *Needs a lawyer*.

## ❌ Blockers: must fix before launch

### 1. <Short title> · 🔬 Confirmed | 🔎 Likely
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
- **Fix:** <the specific technical change> · **Recipe:** <the `references/fixes.md` recipe whose **Covers:** line lists this check ID> · **Safe to auto-fix:** yes / no (needs your decision)
- **Prompt to fix it:**
  > <A ready-to-paste instruction for an AI coding tool, specific to this codebase. Example: "In app/api/invoices/[id]/route.ts, only return the invoice if invoice.user_id equals the current session user's id; return 404 otherwise. Add a test proving user A cannot fetch user B's invoice.">

<repeat>

## ⚠️ Fix before scale or paying users

| # | Issue | Confidence | Where + evidence | Fix | Safe to auto-fix |
|---|---|---|---|---|---|
| 1 | | 🔬 / 🔎 | `file:line`, quoted line or command output | | |

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

| Module | Status | Checks | ✅ Pass | Failed | ➖ N/A | ❓ Can't tell | ❗ Not done |
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
| hunt | ✅ | 9 | | | | | |
| maintainability | ✅ | 16 | | | | | |
| <each profile module> | ✅ / ➖ | | | | | | |
| **Total** | | | | | | | |

**Why ◐ or ❗, and the method per module:**
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

**Checked twice:** evidence for every `file:line` and quote was re-opened by `coverage.py`; an independent re-check of <N> items (every 🔴 plus a sample of passes) confirmed <C> and overturned <O>; the numbers in this report were verified against the ledger (`--verify-report`).

**Sweep** (from `sweep.py`, every file + git history): <N> hits → <F> findings, <R> ruled out after the second look.

**🎯 Hunt** (attacking the app's own logic; `T-` rows in the ledger): <N> hypotheses using <M> methods → <P> proven (<X> new, not in any checklist), <D> disproven, <U> untested.

| Hypothesis | Method | Result |
|---|---|---|
| Two spends at once can take credits below zero | Invariant | 🎯 **Proven, found by hunting** (blocker 2) |
| `/api/v1/export` skips the owner check `/api/export` has | Path | Proven (SEC-075, blocker 3) |
| A coupon can be applied twice | Abuse | Disproven: unique constraint on order_id |
| <untested ones, with what would test them> | | Untested: <why> |

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

## 📏 Standards

*Pasted from `coverage.py`: how this audit's checks came out for each item of each standard (mapping in `references/standards.md`). A coverage view, not a certification.*

| Standard | ✅ | ❌ | ◐ | ➖ | Items that failed |
|---|---|---|---|---|---|
| OWASP Top 10:2025 | 7 | 2 | 1 | 0 | A01:2025, A06:2025 |
| OWASP API Security Top 10 (2023) | | | | | |
| OWASP Top 10 for LLM Applications (2025) | | | | | |
| OWASP Mobile Top 10 (2024) | | | | | |
| OWASP ASVS 5.0.0 (by chapter) | | | | | |
| 2025 CWE Top 25 | | | | | |

## Not checked

- <Areas or commands skipped, why, and the exact command for the user to run, e.g. "Build not run (shared folder in use): run `npm run build`".>


## 👤 Only a human can confirm
- <e.g. a penetration test before your first enterprise customer or before handling health or payment data at scale>
- <mobile binary review (obfuscation, tamper resistance) for M7, memory-safety testing for any native code>
- <legal sign-off on the policies and the "Needs a lawyer" list; a backup restore drill; the standards items marked *Human*>

## 🔁 When to run vibe-check again
Before each launch or big release; after adding payments, sign-in, uploads, AI features, a new country or a new kind of user (children, patients, companies); and at least monthly, because new vulnerabilities and rules appear all the time.
## 🏁 Score card

```text
vibe-check: 🟢 SHIP · Score 91/100 · 112/118 checks · 0 blockers · Full check · 13 Nov 2026
```

*Pasted from the `Score card:` line `coverage.py` printed.*

<only when there are no blockers: the badge snippet; only for 🟢: the ⭐ line, see below>

---
<sub>Checked with vibe-check · github.com/vikneshchandrasekaran21/Vibe-check</sub>
````

## The six symbols (everywhere: report, chat, fixes)

| Symbol | Means | Never use it for |
|---|---|---|
| ✅ | Passed, or fixed and verified | Confidence, "done reading", or anything that failed |
| ❌ | Must fix before launch (a 🔴 check that failed) | A should-fix item or a gap |
| ⚠️ | Fix before you scale (a 🟡 or 🟢 check that failed) | Warnings about the run itself |
| ❓ | Needs the user's answer or a check only they can do | Something you could have checked |
| ➖ | Doesn't apply to this app | Something you skipped |
| 🔧 | Being fixed right now | — |

❗ appears only when something wasn't checked (a gap). Confidence labels are words, never ✅: **🔬 Confirmed**, **🔎 Likely**. Severity colours (🔴 🟡 🟢) belong to the verdict and the checklists, not to individual results.

## While it runs (progress)

Post short progress lines as each step finishes, ticking them off, one line per step, never paragraphs:

```text
Running vibe-check v3.5.0 · Full check

✅ Read your project · 214 files · Next.js + Supabase + Razorpay
✅ Matched your answers to your code · 🔀 1 difference: payments found
✅ Scanned for risky code · 23 hits to review
🔧 Checking security · 41 of 83
```

In tools with a to-do or task list, use it for the same steps instead.

## In the chat (the one-screen summary)

The chat shows the summary; the full report stays in the file. Save the same text as `.vibe-check/summary.md`.

```text
Running vibe-check v3.5.0 · Full check

🔴 DO NOT SHIP · Score 69/100 (capped: 2 blockers open) · Needs work
Since last check (2 Nov): Score 58 → 69 (+11) · ✅ 7 fixed · 🆕 1 new · ↩️ 0 came back

<the totals table and the area scorecard, pasted from coverage.py>

❌ Must fix before launch (2)
 1. Any logged-in user can open another user's invoices · app/api/invoices/[id]/route.ts:12
 2. Your Supabase "order_summary" view shows every order to everyone · supabase/migrations/002_views.sql:1

⚠️ Fix before you scale (29): top 3
 1. No rate limit on password reset · app/api/reset/route.ts:4
 …
❓ Questions for you (12): asked next, as choices
✅ 198 checks passed · ➖ 412 don't apply to this app

Full report: .vibe-check/reports/2026-11-14.md
```

Each problem is **one plain sentence plus its file**. Details come on request ("explain 2"). Then ask the ❓ questions (see *Asking the user* in SKILL.md), then end with the next-step choice and the phrases:

*You can say: "fix" · "fix all" · "fix 2" · "explain 2" · "check again" · "continue fixing" · "undo fix 2"*

## Fix plan (before anything changes)

```text
Here's the plan. Nothing changes until you say go.

🤖 I can fix these safely (7) ............ one OK for all
   Add security headers · Turn off production source maps · …
🧑 Needs your decision (3) ................ asked one at a time, as choices
   Invoices: who should see an invoice?
🖥️ Only you can do these (4) .............. exact steps for each
   Turn on Supabase backups: Dashboard → Database → Backups
⚖️ Needs a lawyer (1) ..................... listed in the report

Where the changes go: a new branch, vibe-check/fixes-2026-11-14 (your main branch is untouched).
```

## Fix card (one per fix)

```text
🔧 Fix 2 of 7 · Users could open other users' invoices (❌ blocker · SEC-015)

Before   Any logged-in user could read any invoice by changing the ID in the URL
Changed  app/api/invoices/[id]/route.ts · only the owner gets the invoice now (+3 lines)
Checked  ✅ Types  ✅ Tests: 14 passed  ✅ SEC-015 re-checked: passes  ✅ User B now gets "not found"
Saved    Commit a1b2c3d · undo: say "undo fix 2"
Users    Nothing changes for real users
```

When a check after the change fails, the change is undone first, then:

```text
❌ Fix 4 of 7 · not applied: your code is back as it was
Why      The checkout test failed after the change (checkout.test.ts:31 expects the old price field)
Choice   Update the test too, or leave this one for you?
```

## Finish line

```text
Done: 6 of 7 fixed · 1 needs you

Score 69 → 86 · Needs work → Ready to launch
✅ 6 fixed and verified   ❌ 1 not applied (fix 4)   ❓ 4 steps only you can do

Your fixes are on the branch vibe-check/fixes-2026-11-14, one commit per fix.
To keep them: merge that branch (or say "merge it" and I'll show you how).
Say "check again" to re-audit everything.
```

The score here comes from re-running `coverage.py` after the ledger rows were updated, never from adding up fixes in your head.

## Writing tips

- Order blockers by severity: data leaks and account takeover first, then money loss, then legal, then outages.
- One finding per real problem. Group repeats (for example, "12 routes are missing ownership checks", with all 12 listed).
- For dependency findings, give the advisory ID, installed version and fixed version.
- Never print a full secret.
- Only 🔬 Confirmed and 🔎 Likely findings go in Blockers or Fix before scale. ❓ items are questions.
- Legal and policy statements cite the skill module or a URL opened in this run, never general memory. Show its first 4 characters and its location.
- If something is fine, don't invent a problem to look thorough.

## Score card, badge and footer

These go at the very end of the saved report **and** the chat summary.

### Score card (always)
One line, in a `text` code block, so it screenshots cleanly:

`vibe-check: <🟢 SHIP | 🟡 SHIP AFTER FIXES | 🔴 DO NOT SHIP> · Score <n>/100 · <passed>/<applicable> checks · <n> blockers · <Quick check|Full check|Enterprise check> · <D Mon YYYY>`

- `passed / applicable` counts only items marked PASS out of items that weren't N/A. CAN'T TELL counts as not passed.
- **Never include** findings, secrets, private URLs, file paths, or the app name, unless the user asks for the app name. The card is meant to be shared publicly.
- If there's an earlier run, add the change from the *Since last check* line: `· was 58`. Before-and-after posts are the most shared.

### Badge (only when there are no blockers, on a Full or Enterprise check)
Offer this snippet for the user's README. **Don't add it yourself** unless the user says yes (scope guard):

```markdown
[![vibe-check score](https://img.shields.io/badge/vibe--check-<score>%2F100%20·%20<band>-<color>)](https://github.com/vikneshchandrasekaran21/Vibe-check)
```

Replace `<score>`, `<band>` (spaces as `%20`) and `<color>`: `brightgreen` for Ready to scale, `green` for Ready to launch, `yellow` for Needs work. `%2F` is the slash. Add the date in the alt text if they want it.

### Star request (only for 🟢, once)
One line, after the badge: *"If vibe-check helped, a ⭐ on https://github.com/vikneshchandrasekaran21/Vibe-check helps others find it."* Don't repeat it in the same session, and never show it for 🟡 or 🔴.

### Footer (always, removable)
The last line of the saved report: `<sub>Checked with vibe-check v<installed> · latest: github.com/vikneshchandrasekaran21/Vibe-check/releases/latest · update: <update step for this tool></sub>`. Leave it out if the user has asked for no footer (or `.vibe-check/config` contains `footer: false`). Never add it to the user's app, pages or code, only to the report.
