# Fixing: the plan, fix cards, undo and the scope guard

Read this at Step 6, before the first fix, and follow it for every fix. The formats (fix plan, fix card, finish line) are in `report-template.md`.

Fix only what the user approves ("fix", "fix all", "fix 2", "fix the blockers"…). In a new session, read `.vibe-check/fix-plan.md`, `.vibe-check/fix-log.md` and the latest report first; "continue fixing" picks up where the log stopped.

## 1. The plan, before anything changes
Run `coverage.py --fix-plan` (writes `.vibe-check/fix-plan.md`: every FAIL, CAN'T TELL and 🎯 hunt finding in priority order, statuses kept between sessions). Show it in the chat as the **Fix plan** from `references/report-template.md`, grouped as **🤖 I can fix these safely** (one OK for all), **🧑 Needs your decision** (asked one at a time, as choices), **🖥️ Only you can do these** (dashboard settings, key rotation, DNS: exact steps), and **⚖️ Needs a lawyer**. Say where the changes will go (next point). Nothing changes until the user says go.

## 2. Where the changes go: branch or checkpoints
- **Code tools with git** (Claude Code, Cursor, Codex, Windsurf, Cline, Copilot, Gemini CLI…): create a branch `vibe-check/fixes-YYYY-MM-DD` and tell the user. **One commit per fix** (`vibe-check: fix <ID> <short title>`). Never push, merge or force anything; the user does that.
- **App builders that work only on the main branch** (Lovable, Replit, Bolt, v0, Base44 and similar): **no branch.** Before each fix, make the tool's own checkpoint or version if it has one, and save a copy of each file you'll change in `.vibe-check/backup/<fix number>/`.
- **No git at all:** the same file copies in `.vibe-check/backup/`, so "undo fix N" can restore them.
- **Unsaved changes already in the project** (`git status` not clean): stop and ask once, as a choice: *"You have unsaved changes. Save them in their own commit first (Recommended) · Fix on top of them · Stop"*. Never mix the user's work into a fix commit.
- Record the branch (or checkpoint method) at the top of `.vibe-check/fix-log.md`.

## 3. One fix at a time, each with a fix card
For each item, top down: mark it `IN PROGRESS`, post `🔧 Fix N of M · <title>`, apply the recipe (below), then **check it**: types and lint, the tests, a test for this bug, and **the same check ID re-run** (plus its hunt variants). Then show the **fix card** from `references/report-template.md` (Before · Changed · Checked · Saved · Users) and append it to `.vibe-check/fix-log.md`.
- **If any check fails after the change, undo it first** (restore the files or reset to the commit before it), then show the ❌ *not applied* card with the reason and a choice. Never leave a half-applied fix, and never mark it done to keep going.
- A fix is `DONE` only when its check ID re-runs as PASS, and the card says how it was verified. Decisions are asked as choices, one at a time, least disruptive option first. Items that change what users see still need a yes (scope guard).
- **Things code can't finish:** legal pages become drafts marked *"DRAFT: needs legal review"*; dashboard settings, key rotation and DNS get exact steps and a question to confirm they're done. None is marked `DONE` on your word alone.
- **"undo fix N"** reverts that fix's commit (or restores its backup copy), sets it back to `TODO`, and says so with a card.

## 4. The finish line
Update the ledger rows for everything fixed or answered, run `coverage.py`, `--verify-report` and `--save`, and show the **Finish line** from `references/report-template.md`: fixed, not applied, only-you steps, the score and band before and after (from `coverage.py`, never added up by hand), and **where the fixes are and how to keep them** (*"merge the branch vibe-check/fixes-2026-11-14"*). Offer "check again".

## Recipes

Follow `fixes.md`: **every 🔴 check ID is listed on the `Covers:` line of a recipe**. Use that recipe's safe fix, avoid its trap, and do its verify step. Then: prove the bug, apply the recipe adapted to the stack, add a test, re-run the check, and commit one issue at a time. If a fix needs the user (a dashboard setting, rotating a key, DNS, a legal decision), give exact step-by-step instructions.

## Scope guard: fix the issue, keep the product

- **Touch only what the finding needs.** Keep diffs as small as possible. Don't edit unrelated files, lines, styles or formatting. Leave existing patterns, naming and structure alone.
- **Legitimate users shouldn't notice.** A correct fix changes behaviour only for attackers, bad input or failure cases. Pages, layouts, features and flows stay as they were.
- **Ask before visible changes.** A consent screen, a "Delete account" button, a CAPTCHA, a rate-limit message, a login wall, or removing a feature all need an explanation, the least disruptive option, and the user's yes.
- **New UI matches the existing design:** the project's own components, styles, fonts, colours and tone.
- **No side quests.** No package upgrades beyond what a fix needs, no migrations, no refactors, no "clean up". Put other ideas under "Other suggestions (not changed)".
- **Keep data safe.** Never delete or rewrite existing user data. Schema changes are additive migrations, tried in staging first.
- **Report what changed:** the files changed and what users will (or won't) notice, after each fix.
- Before writing a fix, read the official docs for the version actually installed. If a fix breaks something, reproduce the problem and read the full error before changing more code.

Never call the audit complete while a 🔴 item is FAIL or an unresolved CAN'T TELL, unless the user explicitly accepts the risk. Record that acceptance in the report.
