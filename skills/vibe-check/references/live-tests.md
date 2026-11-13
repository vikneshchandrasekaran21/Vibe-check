# Tests against the running app (staging or local only)

Load this file when the app can run locally or the user has a **staging or preview URL**, at the Full and Enterprise levels. Reading code shows what *should* happen; these tests show what *does* happen when someone actually tries. Each test is quick, safe and repeatable.

## The rules for live tests
- **Only with the user's OK, and never against production.** Ask once: *"Can I run safe tests against <local or staging URL> with two test accounts? Nothing touches production."* Without a yes, mark the tests `CAN'T TELL` with the exact command for the user. Production stays **read-only** (ground rule 6): GET and HEAD requests only.
- **Test accounts and test data only.** Create or ask for two normal users (A and B) and, if there are roles, one of each. Use payment test modes (Stripe test keys, Razorpay test mode). Never real cards, real people's data or real emails.
- **Scanners use safe settings only:** passive or baseline modes, no denial-of-service, brute-force or fuzzing templates, low request rates, and stop as soon as anything looks unstable.
- **Save what you ran:** every command and its result goes in the ledger's *Tools run* table, and test scripts go in `.vibe-check/proofs/` (gitignored).

## Checks
- [ ] 🔴 LIVE-001 **The target is safe to test:** the user said yes, the URL is local or staging (not production: check the domain, the environment variables and the database it points at), payments are in test mode, and the data can be reset.
- [ ] 🔴 LIVE-002 **User B can't touch user A's things:** for every object type in the inventory (notes, orders, files, invoices, projects, messages…), user B tries to **read, list, update, delete and export** user A's item by its ID, through every API path including old versions. Every attempt must fail (403 or 404) and leave A's data unchanged.
- [ ] 🔴 LIVE-003 **Normal users can't use higher roles' functions:** a normal user calls every admin, staff, owner and internal endpoint and action. All are refused, including hidden ones that aren't linked in the UI.
- [ ] 🔴 LIVE-004 **Logged-out visitors are refused:** every non-public page and API route returns 401 or a redirect to sign-in with no data, including server actions, file URLs and realtime channels.
- [ ] 🟡 LIVE-005 **Hunt proofs re-run against the running app:** the race, replay and limit hypotheses from the hunt (Step 4a) are re-run as real parallel requests against the local or staging server, and the invariants hold.
- [ ] 🟡 LIVE-006 **Rate limits actually trigger:** repeated sign-in, sign-up, reset, OTP and expensive (AI, export, upload) requests get 429s at the documented limits, per user and per IP.
- [ ] 🟡 LIVE-007 **Errors stay quiet:** malformed JSON, wrong types, huge inputs, unknown routes and forced server errors return a friendly message, never a stack trace, SQL error, file path or framework debug page.
- [ ] 🟡 LIVE-008 **Uploads are really checked:** an SVG with a script, an HTML file renamed to `.jpg`, an oversized file and a ZIP with `../` paths are each rejected or made harmless, and uploaded files are served from a separate domain or with `Content-Disposition: attachment`.
- [ ] 🟡 LIVE-009 **OWASP ZAP baseline scan:** run ZAP's baseline (passive) scan against the staging URL, for example `docker run -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t <staging URL>`, and review each warning with the second look. If Docker or ZAP isn't available, say so in *Tools run*.
- [ ] 🟡 LIVE-010 **Known-issue templates (nuclei):** if `nuclei` is installed, run it against the staging URL with safe settings (exclude intrusive, DoS and fuzzing templates; low rate). Its community templates are updated as new vulnerabilities and misconfigurations are published. Review every match with the second look.
- [ ] 🟢 LIVE-011 **The tests can be re-run:** the two-account, role and logged-out tests are saved as scripts (in `.vibe-check/proofs/`), and offered to the user as permanent tests in their suite (only with their OK, under the scope guard).
