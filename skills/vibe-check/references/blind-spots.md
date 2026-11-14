# AI blind spots (every level)

The mistakes AI coding tools make most often. Check every one at every level, Quick included, and record each `BS-` ID in the ledger.

| ID | Check | How to verify |
|---|---|---|
| BS-01 | 🔴 **Authorization, not just login** | Every route that reads or writes by ID filters by owner or tenant on the server. Try fetching user B's record as user A (IDOR). |
| BS-02 | 🔴 **RLS / security rules on** | Supabase: RLS is on for every table, no `using (true)` on user data, and `service_role` is used only on the server. Firebase: rules aren't in test mode. Storage buckets for private files aren't public. |
| BS-03 | 🔴 **No secrets in code or the browser** | Grep for `sk_live`, `sk-`, `AKIA`, `AIza`, `ghp_`, `xox`, `-----BEGIN`, `service_role`, `secret`, `password =`. Check public env prefixes (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`, `REACT_APP_`), `.gitignore`, and git history (`git log --all -p -- '*.env*'`). |
| BS-04 | 🔴 **Server-side validation** | Every write validates input against a schema on the server. |
| BS-05 | 🔴 **No mass assignment** | Users can't set `role`, `is_admin`, `price`, `credits`, `plan` or `user_id`. |
| BS-06 | 🔴 **Prices and payments decided on the server** | Amounts come from the server. Access is granted only from a **verified** webhook. Webhooks are idempotent. |
| BS-07 | 🔴 **Failure paths exist** | Timeouts and error handling on every external call. No empty `catch`, and no stack traces shown to users. |
| BS-08 | 🔴 **Race conditions on money and limits** | Atomic updates, constraints or transactions. Never read-then-write. |
| BS-09 | 🔴 **Dependencies real, current and safe** | Run `npm audit` / `pip-audit`. For each finding give the **advisory ID, installed version and fixed version**. Every package exists and is maintained. |
| BS-10 | 🔴 **Spend is capped** | Per-user limits and `max_tokens` on LLM and paid APIs. Billing alerts (ask the user). |
| BS-11 | 🔴 **Admin, debug and extra domains locked** | Admin routes are checked on the server. Debug is off. No test or seed accounts. No public source maps, `.git` or `.env`. Platform default domains (`*.workers.dev`, `*.vercel.app` and so on) are disabled or redirected. |
| BS-12 | 🔴 **Email actually sends** | Verification, password reset and alert emails reach an inbox: a provider is configured and SPF, DKIM and DMARC are set. Apps break silently when email is missing. |
| BS-13 | 🔴 **AI features are safe** (if the app uses an LLM) | See `ai-features.md`. |
| BS-14 | 🟡 **No N+1 queries or unbounded reads** | Pagination, and no queries inside loops. |
| BS-15 | 🟡 **Tests actually test** | No tests that always pass, mirror the code, or were skipped to make CI green. |
| BS-16 | 🟡 **One way of doing things** | No duplicate helpers or libraries from different AI sessions. |
| BS-17 | 🟡 **Time, locale and encoding** | UTC storage, a date library, UTF-8 end to end. Translated pages and policies match the original. |
| BS-18 | 🟡 **Boilerplate matches reality** | The privacy policy, terms and marketing claims match the data map and features, and nothing is overstated ("cannot be reversed", "bank-grade", "fully encrypted"). |
| BS-19 | 🔴 **Versions from training data** | AI tools pin the versions they remember: old runtimes, framework majors, Docker tags and plugin versions, sometimes already end-of-life or with published security fixes. Run `scripts/versions.py` and check each component against today's release pages (`references/vulnerabilities.md`). |
