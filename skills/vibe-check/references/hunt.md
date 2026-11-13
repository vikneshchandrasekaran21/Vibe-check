# Hunt: find what no checklist describes

Load this file for every Full and Enterprise check (Step 4a). The other modules **check** known problems. This one **discovers** new ones: the bugs in *this* app's own logic that no scanner rule or checklist line can name, like a credit balance that two requests can spend twice, or an old endpoint that skips the ownership check the new one has. Think like an attacker who wants the app's money, data or admin powers, then prove or disprove each idea.

## Safety rules for hunting (on top of the ground rules)
- **Only the user's own app,** in this project, run **locally or on their staging** with test data. Never production, never anyone else's system.
- **Prove with the smallest safe proof:** a failing test, a script against a local server and database, or the exact quoted code path. Put proof files in `.vibe-check/proofs/` (gitignored), never in the user's code during the audit.
- **No working exploits:** no payloads meant to be reused, no instructions for attacking other people's apps.
- **Suspected bug in someone else's software** (a library, framework, runtime or SaaS API): write *"possible new vulnerability in <project>: report it privately"* with the project's security contact or `SECURITY.md`. Never publish details or build an attack.
- **Can't run anything?** Hunt by reading code: a hypothesis proven only by code reading is at most 🔎 Likely, with the code path quoted.

## The method
- [ ] 🔴 HUNT-001 **Threat model written down:** from the inventory, list the app's **assets** (money, credits, quotas, private data, accounts, admin powers, the AI bill), its **actors** (visitor, user, other user, team member, admin, webhook sender, the AI model's output), its **trust boundaries** (browser → API, API → database, app → third parties, AI output → tools) and its **entry points** (every route, action, webhook, job, upload, realtime channel). Write it in the ledger under `## Threat model`.
- [ ] 🔴 HUNT-002 **Invariants attacked:** for every asset, write the rules that must always hold (*"credits never go below zero"*, *"a user only sees their own rows"*, *"scans never exceed the plan"*, *"an order ships only after it's paid"*, *"one invite gives one seat"*). Attack each one: **two requests at once**, the same request **twice**, **out of order**, at the **edges** (0, −1, huge, decimals, empty, Unicode), and across **time** (midnight, month end, time zones, plan changes).
- [ ] 🔴 HUNT-003 **Abuse cases per feature:** for every money, credit, quota, invite, coupon, referral, vote, reward, upload, sharing, export, account-change and AI feature in the inventory, write how a greedy or malicious user would abuse it (free credits, stacked discounts, unlimited trials, fake referrals, vote stuffing, other people's files, a huge AI bill) and test it.
- [ ] 🟡 HUNT-004 **Same action, every path:** compare each sensitive action across the web app, API, mobile app, old versions (`/v1/`), admin routes, server actions, webhooks, background jobs and imports. Any path with **less** checking (auth, ownership, validation, limits, payment state) than the others is a finding.
- [ ] 🟡 HUNT-005 **Assumptions questioned:** list what the code silently trusts (*"only Stripe calls this"*, *"IDs can't be guessed"*, *"the client sends the right price, role or user ID"*, *"this runs once"*, *"the email is verified"*, *"the AI returns valid JSON"*, *"the file is really an image"*) and break each one.
- [ ] 🔴 HUNT-006 **Variants of every confirmed finding:** turn each confirmed FAIL (from any module) into a pattern and search the whole codebase for siblings. One missing ownership check usually means more.
- [ ] 🟡 HUNT-007 **Chains:** combine findings, including 🟡 and 🟢 ones, into attack paths (for example an open redirect plus a sign-in callback that keeps the token: account takeover). Report a chain at the severity of its worst outcome.
- [ ] 🟡 HUNT-008 **Every hunt finding has a proof and a variant search:** a failing test or local script in `.vibe-check/proofs/`, or the quoted code path for 🔎 Likely, plus the variant search (HUNT-006) for it.
- [ ] 🟡 HUNT-009 **Nothing silently skipped:** every hypothesis gets a row, including disproven and untested ones (with why), so the user sees what was tried.

## Recording hypotheses
Each hypothesis is a `T-` row in the ledger, under `## Hunt`:

```markdown
## Threat model
- Assets: credits (users.credits), Pro plan, private notes, admin panel, OpenAI bill
- Actors: visitor, user, other user, team admin, Stripe webhook, AI output
- Boundaries: browser → /api, /api → Supabase (service role in server only), app → OpenAI
- Entry points: 23 pages, 47 API routes, 3 webhooks, 2 cron jobs (inventory)

## Hunt
| ID | Hypothesis | Method | Result | Evidence |
|---|---|---|---|---|
| T-001 | Two spends at once can take credits below zero | INVARIANT | PROVEN NEW | .vibe-check/proofs/credits-race.test.ts: 2 parallel calls, balance 10 → -10; api/spend.ts:14-19 read-then-write without a transaction |
| T-002 | Coupon can be applied twice to one order | ABUSE | DISPROVEN | api/coupon.ts:22 unique (order_id) constraint, insert fails on the second call |
| T-003 | /api/v1/export skips the owner check that /api/export has | PATH | PROVEN SEC-075 | api/v1/export.ts:9 queries by id only; proof: user B exports user A's data |
| T-004 | Plan change mid-month resets the scan counter | INVARIANT | UNTESTED | needs a Stripe test-mode subscription; question for the user |
```

- **Method:** `THREAT`, `INVARIANT`, `ABUSE`, `PATH`, `ASSUMPTION`, `VARIANT` or `CHAIN`.
- **Result:** `PROVEN NEW` (no checklist line describes it), `PROVEN <check ID>` (it's a finding under that check), `DISPROVEN` (with what stopped it) or `UNTESTED` (with why, and what would test it).
- `coverage.py` counts them. A Full check needs **at least 12 hypotheses** using **at least 4 different methods** (including `INVARIANT` and `ABUSE`); Enterprise needs **at least 25** using **at least 6**. Any confirmed FAIL needs at least one `VARIANT` row (ideally one per finding), and two or more FAILs need a `CHAIN` row. These are minimums: keep going while hypotheses are still turning up bugs.

## Where hunt findings go in the report
Proven hunt findings go through the second look (Step 4b) like any other finding, then into 🔴 or 🟡 with the usual fields. `PROVEN NEW` ones are marked **🎯 Found by hunting** (no checklist line describes it). The report's *Hunt* section lists how many hypotheses were tried, proven, disproven and untested, and the most interesting disproven ones (they show the user what's already solid).
