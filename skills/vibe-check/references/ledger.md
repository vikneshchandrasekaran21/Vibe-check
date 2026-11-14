# The ledger: format, row types and tools

Read this at Step 4, before the first ledger row. Every result goes in the ledger; `coverage.py` counts it.

## The ledger

**The ledger is the audit's memory.** Create `.vibe-check/ledger.md` at the start:

```markdown
# vibe-check ledger
Level: Full
Date: YYYY-MM-DD

| ID | Result | Evidence / reason |
|---|---|---|
| SEC-001 | PASS | src/lib/auth.ts:4 uses Clerk; no custom password code (grep "bcrypt\|jwt.sign": 0 hits) |
| SEC-030 | FAIL 🔎 Likely | app/notes/[id]/page.tsx:41 renders note.body with dangerouslySetInnerHTML |
| SEC-047 | CAN'T TELL | invite codes come from an external service; question for the user |
| PLT-011..PLT-015 | N/A | not on Firebase |
| HLT-* | N/A | no health, medical or fitness data |
| INV-api_routes | 47/47 | every route traced to its auth check |
| H-001..H-003 | RULED OUT | Supabase anon key: public by design, RLS on (SEC-017 PASS) |
| H-004 | FINDING SEC-022 | live Stripe key in src/lib/stripe.ts:3 |
| V-002 | OUTDATED | PHP 8.3.35, security release 8.3.36 is out: https://www.php.net/releases/ (opened today) |
| V-005..V-031 | CURRENT | npm audit --omit=dev: 0 vulnerabilities |
```

- **Results:** `PASS`, `FAIL 🔬 Confirmed` / `FAIL 🔎 Likely`, `N/A`, `CAN'T TELL`. Every row needs its own evidence or reason. Copy-pasted evidence is rejected.
- **Ranges and `*` are for N/A only** (a platform section you don't use, a profile module that doesn't apply). Core modules are never N/A as a whole.
- **`INV-<category>` rows:** checked/found for every inventory category that has items. **`H-` rows:** a verdict for every sweep hit. **`V-` rows:** a verdict for every component in `.vibe-check/versions.md`, with its source.
- **Split the work when you can.** In tools with helper agents (subagents), give each module, or group of small modules, to its own fresh helper with the inventory, sweep, versions and profile files. Each helper writes its rows to `.vibe-check/ledger.d/<module>.md`; `coverage.py` reads them together with the main ledger. Without helpers, work one module at a time and resume with `coverage.py --remaining`.
- **Evidence is checked against the files.** Every `file:line` you cite must exist, and code you quote in backticks must appear in the cited file exactly: `coverage.py` re-opens the files and rejects anything that doesn't match. Re-read before you quote.
- **One module at a time.** Re-open the module file and read it **just before** checking it (never from memory), check every item, and **write its rows to the ledger immediately.** That saves progress: on a big app, if the conversation gets long, run `python3 <skill-folder>/scripts/coverage.py --remaining` and continue from what's left instead of getting shallower.
- **Tools run:** add a `## Tools run` table to the ledger: every tool you ran or tried (`npm audit`, type-check, lint, tests, build, secret scanner, Lighthouse…), the exact command, and the result, including *"not installed"* or *"failed: <error>"*.

## Tools and fallbacks

**Always try the project's own tools** and record each in the ledger's *Tools run* table: the package audit (`npm audit` / `pnpm audit` / `pip-audit`), type-check (`tsc --noEmit` or the framework's check), lint, the test suite, and the build. Then use what's available: gitleaks or trufflehog, `npx license-checker`, Lighthouse, axe, Playwright, and `curl -I` against live URLs. **If a tool is missing or blocked, don't skip the check:** use the fallback, and say which method you used.

| Check | Fallback |
|---|---|
| License scan | Read the `license` field of each dependency from the lockfile or `node_modules/*/package.json` |
| Secret scan | The grep patterns in blind spot #3, over files and `git log -p` |
| Click-through QA | Static review: every `onClick`, `<a href>`, form `action` and route traced to a handler that exists (see `functional-qa.md`) |
| Lighthouse / axe | Manual review of the main pages against `launch-ux.md` |
| Dashboard-only settings (backups, MFA, billing alerts, branch protection, uptime monitors) | Check config files and `gh` / platform CLIs if logged in; otherwise mark CAN'T TELL and ask the user |
| Build | List it under "Not checked", with the exact command for the user to run |

**vibe-check connector:** if tools from the vibe-check connector are available (for example `scan_live_site`, `crawl_app`, `check_supabase`, `check_email_domain`, `check_dependencies`, `save_report`), use them for the live and hosted checks and to save the report. Otherwise use the local tools and fallbacks above. Send the connector URLs, lockfiles and summaries only, never source code or secrets.
