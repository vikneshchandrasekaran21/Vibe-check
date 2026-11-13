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

## 🏁 Score card

```text
vibe-check: 🟢 SHIP · 112/118 checks · 0 blockers · Launch level · 13 Nov 2026
```

<only if 🟢: the badge snippet and the ⭐ line, see below>

---
<sub>Checked with vibe-check · github.com/vikneshchandrasekaran21/vibe-check</sub>
````

## Writing tips

- Order blockers by severity: data leaks and account takeover first, then money loss, then legal, then outages.
- One finding per real problem. Group repeats (for example, "12 routes are missing ownership checks", with all 12 listed).
- For dependency findings, give the advisory ID, installed version and fixed version.
- Never print a full secret. Show its first 4 characters and its location.
- If something is fine, don't invent a problem to look thorough.

## Score card, badge and footer

These go at the very end of the saved report **and** the chat summary.

### Score card (always)
One line, in a `text` code block, so it screenshots cleanly:

`vibe-check: <🟢 SHIP | 🟡 SHIP AFTER FIXES | 🔴 DO NOT SHIP> · <passed>/<applicable> checks · <n> blockers · <Quick|Launch|Enterprise> level · <D Mon YYYY>`

- `passed / applicable` counts only items marked PASS out of items that weren't N/A. CAN'T TELL counts as not passed.
- **Never include** findings, secrets, private URLs, file paths, or the app name, unless the user asks for the app name. The card is meant to be shared publicly.
- If the score improved since the last report in `.vibe-check/reports/`, add the change: `· was 🔴 71/118`. Before-and-after posts are the most shared.

### Badge (only for 🟢 SHIP at Launch or Enterprise level)
Offer this snippet for the user's README. **Don't add it yourself** unless the user says yes (scope guard):

```markdown
[![vibe-checked](https://img.shields.io/badge/vibe--checked-%E2%9C%85%20SHIP%20<passed>%2F<applicable>-brightgreen)](https://github.com/vikneshchandrasekaran21/vibe-check)
```

Replace `<passed>` and `<applicable>` with the numbers (`%2F` is the slash).

### Star request (only for 🟢, once)
One line, after the badge: *"If vibe-check helped, a ⭐ on https://github.com/vikneshchandrasekaran21/vibe-check helps others find it."* Don't repeat it in the same session, and never show it for 🟡 or 🔴.

### Footer (always, removable)
The last line of the saved report: `<sub>Checked with vibe-check · github.com/vikneshchandrasekaran21/vibe-check</sub>`. Leave it out if the user has asked for no footer (or `.vibe-check/config` contains `footer: false`). Never add it to the user's app, pages or code, only to the report.
