# Fix playbook

<!-- contents: kept up to date by scripts/build.py -->
## Contents
- How to fix (applies to every recipe)
- Access control
  - Missing authorization / IDOR
  - Supabase RLS
  - Firebase rules
  - Mass assignment
- Secrets
  - Leaked secret (in code, the client bundle or git history)
- Data leakage
  - API returns too much data
  - Account enumeration
  - Private data in shared caches
- Input and injection
  - Server-side validation
  - SQL / NoSQL injection
  - XSS
  - File uploads
  - Open redirect
  - SSRF
- Money
  - Prices from the client / payments trusted from the redirect
  - Webhook verification and idempotency
  - Race conditions (credits, coupons, stock)
- Reliability
  - Timeouts and error handling
  - Retries
  - Indexes and migrations
  - Backups and restore test
  - Error tracking and uptime (quickest path)
- Abuse and cost
  - Rate limiting
  - LLM spend caps
- Headers and transport
  - Security headers (Next.js example)
  - Cookies
- AI features
  - Prompt injection and unsafe output
- Legal and privacy
  - Privacy policy that doesn't match the app
  - Analytics before consent
  - Account and data deletion
  - GPL/AGPL dependency in closed-source code
  - Outdated, end-of-life or vulnerable runtime, framework or plugin
  - Reset and magic links built from the Host header
  - Email, password or 2FA changes without re-authentication
  - Secrets compared with ==
  - Sensitive files reachable on the live site
  - Container runs as root or has secrets baked in
- More recipes (every 🔴 check points to one)
  - Sign-in, sessions and password storage
  - Keys for your own API and MCP endpoints
  - HTTPS everywhere
  - Encryption at rest and very sensitive fields
  - Command injection, template injection and XML entities
  - Secrets in URLs and guessable links
  - GraphQL and real-time channels
  - Admin tools, debug modes, default passwords and extra domains
  - Subdomain takeover
  - Supply chain: packages, CI and third-party scripts
  - Environments, deploys and rollback
  - Accounts, access and spending
  - Logs without secrets or personal data
  - Card data and payment rules
  - Broken journeys, buttons, forms and messages
  - Accessibility basics
  - Email that arrives, and consent to marketing
  - Legal pages and honest selling
  - Fonts, images and code you don't own
  - Chat widgets, session replay and embeds
  - Children's data
  - Health data
  - Community safety
  - AI data, tools and agents
  - Mobile store requirements and secure storage
  - Desktop apps and browser extensions
  - Languages and countries
  - Enterprise readiness
  - Logic bugs found by hunting
  - A safe target for live tests
  - Handover: running the app
  - Hidden instructions for AI tools
  - Views and database functions that skip row-level security
  - Checks that fail open
  - SAML single sign-on
  - Client IP, one-time codes and password hashing limits
  - Authenticated encryption
  - Security alerts
<!-- /contents -->

Use these patterns when fixing findings (Step 5), and for the **Fix** and **Prompt to fix it** lines in the report. Adapt each one to the project's stack and the versions actually installed. Check the official docs for that version before writing code.

## How to fix (applies to every recipe)

1. **Prove the bug first.** Write a failing test, or a reproducible request (curl, script), that shows the problem.
2. **Make the smallest correct change, and keep the product as it is.** Don't change the design, features, flows or copy (see *Scope guard* in SKILL.md). If the fix must add something users will see, get approval and build it with the project's existing components and styles. Fix the root cause in one place (a shared helper, a policy or a middleware) rather than patching every caller differently.
3. **Don't add dependencies casually.** Use what the project already has. If you need a new package, check it's real, maintained and widely used, and tell the user.
4. **Verify.** The test from step 1 now passes, the other tests still pass, and the original check from the audit is re-run and marked PASS with new evidence.
5. **One issue per commit**, with a message that says what was wrong and how it was fixed.
6. **If the fix needs the user** (rotating a key in a dashboard, changing DNS, a legal decision), stop and give them exact step-by-step instructions instead of guessing.

---

## Access control

### Missing authorization / IDOR
**Covers:** BS-01, SEC-014, SEC-015, SEC-016, SEC-019, SEC-020, SEC-075, PLT-027, LIVE-002, LIVE-003, LIVE-004, HLT-004, KID-013
**Pattern:** every read or write of a record is scoped to the current user or tenant on the server. Return **404** (not 403) for records the user doesn't own, so IDs can't be discovered.
```ts
// before: db.invoice.findUnique({ where: { id } })
const invoice = await db.invoice.findFirst({ where: { id, userId: session.user.id } });
if (!invoice) return new Response("Not found", { status: 404 });
```
- Put the check in one helper (`requireOwner`, `getUserScopedQuery`) and use it everywhere. Search for every other query on the same table.
- Admin-only routes call a server-side `requireRole("admin")`. Hiding a button is not access control.
- **Test:** create users A and B. A requests B's record by ID and gets 404, for read, update and delete.

### Supabase RLS
**Covers:** BS-02, SEC-017, PLT-001, PLT-002, PLT-003, PLT-004, PLT-005, PLT-006, PLT-032
```sql
alter table public.notes enable row level security;

create policy "own rows: select" on public.notes for select using (auth.uid() = user_id);
create policy "own rows: insert" on public.notes for insert with check (auth.uid() = user_id);
create policy "own rows: update" on public.notes for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "own rows: delete" on public.notes for delete using (auth.uid() = user_id);
```
- Write it as a migration (`supabase migration new rls_notes`), not in the dashboard.
- For teams, check membership: `using (exists (select 1 from members m where m.org_id = notes.org_id and m.user_id = auth.uid()))`.
- Remove any `using (true)` policy on user data. Move code that needs `service_role` into a server route or edge function.
- Storage: make the bucket private and add policies on `storage.objects` that check `auth.uid()` against the path or owner.
- **Test:** with the anon key and user B's session, try to read user A's rows. You should get an empty result.

### Firebase rules
**Covers:** PLT-011, PLT-012
```
match /notes/{noteId} {
  allow read, delete: if request.auth != null && resource.data.ownerId == request.auth.uid;
  allow create: if request.auth != null && request.resource.data.ownerId == request.auth.uid
                && request.resource.data.keys().hasOnly(['ownerId','title','body','createdAt']);
  allow update: if request.auth != null && resource.data.ownerId == request.auth.uid
                && request.resource.data.ownerId == resource.data.ownerId;
}
```
Test with the Firebase emulator's rules unit tests.

### Mass assignment
**Covers:** BS-05, SEC-018
Allow-list fields with a schema. Never write the raw body.
```ts
const UpdateProfile = z.object({ name: z.string().min(1).max(80), bio: z.string().max(500).optional() }).strict();
const data = UpdateProfile.parse(await req.json());   // role, credits, userId are rejected
await db.user.update({ where: { id: session.user.id }, data });
```

## Secrets

### Leaked secret (in code, the client bundle or git history)
**Covers:** BS-03, SEC-022, SEC-023, PLT-022, PLT-028, PLT-033, MOB-011, AIF-001, OPS-030
Do these in order. **Rotating the key is the fix.** Deleting the line is not.
1. **Rotate now** in the provider dashboard (Stripe, OpenAI, Supabase and so on). Give the user exact steps; you usually can't do this yourself.
2. Move the new value into server-only env vars (not `NEXT_PUBLIC_` / `VITE_` / `EXPO_PUBLIC_`), and into the hosting provider's env settings for each environment.
3. If the browser needed it, put a server route in between that calls the provider.
4. Add `.env*` (except `.env.example`) to `.gitignore`. Turn on GitHub secret scanning and push protection, or gitleaks in CI.
5. Rewriting git history (git filter-repo) is optional once the key is rotated. Tell the user it's a destructive, team-wide operation.

## Data leakage

### API returns too much data
**Covers:** SEC-055, PLT-029, KID-014
Send a response shape that lists exactly the fields the screen needs (a DTO or `select`), never the raw row:
```ts
const user = await db.user.findUnique({ where: { id }, select: { id: true, name: true, avatarUrl: true } });
```
For server-rendered frameworks, pass only those fields to client components. **Test:** the response for another user's public profile contains no email, phone, password hash or internal flags.

### Account enumeration
**Covers:** SEC-056
Return the same message, with similar timing, whether or not the account exists: *"If an account exists for that email, we've sent a link."* For signup, send a "you already have an account" **email** instead of showing it on screen. Rate-limit these endpoints.

### Private data in shared caches
**Covers:** SEC-057
Add `Cache-Control: private, no-store` to authenticated responses, and make sure CDN or framework caching (e.g. `revalidate`, edge cache rules) is off for personalised routes. **Test:** two users fetch the same URL and each sees only their own data.

## Input and injection

### Server-side validation
**Covers:** BS-04, SEC-027
One schema per endpoint, parsed on the server, and shared with the form for UX. Reject with 400 or 422 and field errors. Limit string lengths, array sizes and numbers.

### SQL / NoSQL injection
**Covers:** SEC-028, SEC-029
Parameterized queries only: `` sql`select * from users where email = ${email}` `` (tagged template), `$1` placeholders, or ORM methods. For Mongo, validate that inputs are primitives (`z.string()`) so `{ "$gt": "" }` can't get through.

### XSS
**Covers:** SEC-030
- Render user content as text by default (React escapes it automatically).
- If HTML or markdown must render: `DOMPurify.sanitize(html)`, or a markdown renderer with raw HTML disabled (`react-markdown` without `rehype-raw`).
- Validate user URLs: allow only `http:` and `https:` (blocks `javascript:`).

### File uploads
**Covers:** SEC-032
Accept uploads through **signed upload URLs** to a **private** bucket. On the server: check size, check the real type (magic bytes, e.g. the `file-type` package), generate a random filename, and serve files via short-lived signed URLs with `Content-Disposition: attachment` for anything not shown as an image. Don't serve SVG or HTML uploads inline from your main domain.

### Open redirect
**Covers:** SEC-035
`const next = url.startsWith("/") && !url.startsWith("//") ? url : "/";`

### SSRF
**Covers:** SEC-034
Resolve the hostname and block private, loopback, link-local and metadata ranges before fetching. Better still, fetch only from an allow-list of domains. Turn off redirects or re-check after each one.

## Money

### Prices from the client / payments trusted from the redirect
**Covers:** BS-06, PLT-034, PLT-039, PLT-040
- The client sends a **product or price ID**. The server looks up the amount and creates the checkout session.
- Access is granted only in the **verified webhook** handler. The success page just shows "processing…" and polls your DB.

### Webhook verification and idempotency
**Covers:** PLT-038, FIN-003, REL-004
```ts
const raw = await req.text();                       // raw body, not parsed JSON
const event = stripe.webhooks.constructEvent(raw, req.headers.get("stripe-signature")!, process.env.STRIPE_WEBHOOK_SECRET!);
// idempotency: a processed_events table with a UNIQUE event_id
const inserted = await db.$executeRaw`insert into processed_events (id) values (${event.id}) on conflict do nothing`;
if (inserted === 0) return new Response("ok");      // already handled
// handle the event (or enqueue it), then return 200 quickly
```
Razorpay: verify `X-Razorpay-Signature` with HMAC-SHA256 of the raw body. Paddle and Lemon Squeezy have the same pattern with their own signature headers.

### Race conditions (credits, coupons, stock)
**Covers:** BS-08, FIN-009
Use a single atomic statement or a constraint, never read-then-write:
```sql
update accounts set credits = credits - 1 where id = $1 and credits > 0 returning credits;  -- 0 rows → insufficient
create unique index one_redemption_per_user on coupon_redemptions (coupon_id, user_id);
```
For multi-step changes, use a transaction with `select … for update`.

## Reliability

### Timeouts and error handling
**Covers:** BS-07, REL-002, REL-003
```ts
const res = await fetch(url, { signal: AbortSignal.timeout(10_000) });
```
- Set timeouts on DB clients, LLM SDKs (`timeout`, `maxRetries`) and serverless functions.
- One error handler per layer: it logs the full error with a request ID to the error tracker, and returns a generic message plus the right status code to the client. Add a React error boundary or `error.tsx` for the UI.
- Replace every empty `catch {}` with handling, or rethrow.

### Retries
**Covers:** REL-005
Retry only idempotent operations, with exponential backoff and jitter (e.g. 0.5s, 1s, 2s ± random), at most 3–5 times. Prefer the SDK's built-in retry option.

### Indexes and migrations
**Covers:** REL-010, REL-011
Create a migration (Prisma, Drizzle, Supabase or Rails) that adds the index, e.g. `create index concurrently if not exists idx_orders_user_created on orders (user_id, created_at desc);`. Confirm it's used with `EXPLAIN ANALYZE`.

### Backups and restore test
**Covers:** OPS-026, OPS-027, OPS-028
Turn on automated backups and point-in-time recovery in the DB provider. Then help the user **restore into a new staging DB** and check that row counts and a few records match. Record the date and the time it took.

### Error tracking and uptime (quickest path)
**Covers:** OPS-014, OPS-015, OPS-016, MOB-018
Install the framework's official Sentry or PostHog wizard (`npx @sentry/wizard@latest -i nextjs`), set DSNs per environment, and filter personal data out before sending. Add an external uptime check on `/` and `/api/health` with alerts to email, Slack or phone.

## Abuse and cost

### Rate limiting
**Covers:** SEC-007, SEC-053, REL-044, COM-010, UX-025
Use the platform's built-in limiter or a shared store (Upstash Ratelimit, Redis, Cloudflare rules), keyed by user ID, and by IP for anonymous traffic. Apply it to auth, OTP and SMS, email sending, uploads and AI endpoints. Return 429 with `Retry-After`. In-memory limiters don't work on serverless.

### LLM spend caps
**Covers:** BS-10, AIF-002, AIF-003, AIF-004, AGT-008
- Calls go only through your server, with `max_tokens` and an input length limit.
- A `usage` table (user_id, period, tokens or cost). Check and increment it atomically before each call, and refuse with a friendly "limit reached" message.
- Set a monthly budget and alert in the provider dashboard (give the user the steps).

## Headers and transport

### Security headers (Next.js example)
**Covers:** SEC-046
```js
// next.config.js → async headers()
{ source: "/(.*)", headers: [
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  { key: "Content-Security-Policy-Report-Only", value: "default-src 'self'; frame-ancestors 'none'; ..." },
]}
```
Start CSP in report-only mode, fix the violations, then enforce it. Express: `helmet()`. Other platforms: use their headers config.

### Cookies
**Covers:** SEC-003, PLT-045
`Set-Cookie: session=…; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=…`. Move tokens out of `localStorage`, using the auth library's cookie mode.

## AI features

### Prompt injection and unsafe output
**Covers:** BS-13, AIF-008, AIF-009, AIF-010, AGT-004, AGT-005
- Treat model output like user input: sanitize before rendering, and validate with a schema before using it.
- Tools run with the end user's permissions. Destructive tools need a confirmation step in the UI.
- Scope RAG retrieval by `user_id` / `org_id` in the query itself.
- Strip or restrict external images and links in rendered output.

## Legal and privacy

### Privacy policy that doesn't match the app
**Covers:** LEG-001, LEG-007, LEG-008, POL-002, AIF-015, MOB-003
Generate a draft **from the data map** in Step 1 (each field, purpose, processor, retention, user rights, contact), not from a generic template. Mark it "DRAFT – needs legal review" and put it on the "Needs a lawyer" list.

### Analytics before consent
**Covers:** LAW-002, LEG-003, KID-010, HLT-002
Load analytics, ads pixels and session replay only after consent: keep the consent state, and initialize the scripts in a callback (or use the tool's consent mode, e.g. Google Consent Mode v2 or PostHog `opt_out_capturing_by_default`). Essential cookies stay on.

### Account and data deletion
**Covers:** LEG-009, MOB-001
- Add a "Delete account" button in settings (required in mobile apps). Re-authenticate, then confirm.
- A server job deletes or anonymizes the user's rows (FK `on delete cascade` or explicit deletes), storage files, and third-party records (payment customer, email list contact, analytics person, AI provider data where possible). Revoke sessions.
- Keep only what the law requires (invoices), documented in the privacy policy.
- **Test:** after deletion, the user's data can't be found anywhere in the DB or storage.

### GPL/AGPL dependency in closed-source code
**Covers:** LEG-015
Replace the package with a permissively licensed alternative, or isolate it. Put the license question on the "Needs a lawyer" list. Don't decide this yourself.

### Outdated, end-of-life or vulnerable runtime, framework or plugin
**Covers:** BS-19, SEC-048, VUL-001, VUL-002, VUL-003, VUL-004, VUL-005, VUL-006, VUL-007, VUL-008
1. Find the fixed version on the official advisory or release page opened during this run, and quote it. Never pick a version from memory.
2. Prefer the smallest safe step: a patch release on the same line (for example 8.3.35 → 8.3.36) before a major upgrade.
3. Update every place the version lives: the Docker `FROM` tag, `.nvmrc`/`.python-version`/`.tool-versions`, `engines`, `composer.json` `config.platform`, the hosting dashboard, and the lockfile (`npm install next@<fixed>`, `composer update vendor/package`). Then run the tests and the build.
4. If the upgrade can't ship today, apply the advisory's official workaround (quoted), add a dated follow-up to the report, and ask the user to schedule the upgrade.
5. Major upgrades (a new framework major, an end-of-life runtime) change behavior: **don't do them as an auto-fix**. Give the user a migration plan and do it on a branch with their OK.

### Reset and magic links built from the Host header
**Covers:** SEC-069
Build every emailed link from one configured base URL (`APP_URL`, `NEXT_PUBLIC_SITE_URL`, `config('app.url')`), never from the request's Host header. Add a test that sends a reset request with `Host: evil.example` and checks that the email link still uses the real domain.

### Email, password or 2FA changes without re-authentication
**Covers:** SEC-071
Require the current password (or a fresh login within the last few minutes) for email, password, 2FA, payout and linked-login changes. On an email change, notify the **old** address with an "undo / this wasn't me" link and confirm the new one before switching. On a password change, end all other sessions. Add tests for each.

### Secrets compared with ==
**Covers:** SEC-072
Use the platform's constant-time compare: `crypto.timingSafeEqual(Buffer.from(a), Buffer.from(b))` after checking the lengths match (Node), `hmac.compare_digest` (Python), `hash_equals` (PHP), `ActiveSupport::SecurityUtils.secure_compare` (Rails), or the provider SDK's own webhook verify function.

### Sensitive files reachable on the live site
**Covers:** SEC-079
Block them at the server or host: deny `/.git`, `/.env*`, backups and `phpinfo` in the web server or platform config, keep them out of the deploy (`.dockerignore`, `.vercelignore`, build output folder only), then re-check each URL returns 404. If `.git` or `.env` was ever public, treat every secret in them as leaked: rotate.

### Container runs as root or has secrets baked in
**Covers:** OPS-041, OPS-042, CLD-014, CLD-015, PLT-049
Add a non-root user (`RUN adduser -D app` / `USER app`, or the image's built-in `node`/`www-data` user), move secrets from `ENV`/`ARG` to runtime platform secrets, add `.env` and `.git` to `.dockerignore`, rebuild, and confirm with `docker history` that no layer contains them. Rotate any secret that was in an image that was ever pushed.

---

## More recipes (every 🔴 check points to one)

Each recipe: **Safe fix** (the approach), **Trap** (how AI fixes usually go wrong), **Verify** (how to prove it, then re-run the check ID).

### Sign-in, sessions and password storage
**Covers:** SEC-001, SEC-002, SEC-004, SEC-005, SEC-006, SEC-041, ENT-001, ENT-003
**Safe fix:** use the auth the stack already has (Supabase Auth, Clerk, Auth.js, Firebase Auth, Django/Rails/Laravel built-ins) instead of hand-written login. Passwords are hashed with Argon2id or bcrypt by that library. JWTs are verified with the library's verify call (signature, `exp`, `iss`, `aud`, fixed algorithm). Reset and magic links are single-use, short-lived, hashed at rest and invalidated after a password change. Email is verified before it unlocks anything sensitive. Enterprise SSO and MFA use the provider's built-in options.
**Trap:** `jwt.decode` instead of `verify`; reset tokens stored in plain text or reusable; "logout" that only deletes the cookie while the session stays valid on the server.
**Verify:** a tampered or expired token is refused; a used reset link fails the second time; after logout, the old session cookie gets 401.

### Keys for your own API and MCP endpoints
**Covers:** SEC-024, AGT-015
**Safe fix:** issue random keys (32+ bytes) shown once, store only a hash, scope each key (read/write, which resources), let users revoke and rotate them, and rate-limit per key. Remote MCP endpoints require OAuth or per-user tokens and check the user on every tool call.
**Trap:** one shared key for every customer, keys stored in plain text, or MCP servers that trust any caller on the network.
**Verify:** a revoked key gets 401 immediately; a read-only key can't write; an MCP call without a token is refused.

### HTTPS everywhere
**Covers:** SEC-040, SEC-045, PLT-020, CLD-011, MOB-013
**Safe fix:** turn on the host's "always HTTPS" redirect and HSTS (start with a short max-age, raise it later), use TLS 1.2+, and make every API, webhook, image and font URL `https://`. Mobile apps keep the platform defaults (no cleartext exceptions).
**Trap:** fixing the main site but leaving an `http://` API URL, webhook or CDN asset; adding HSTS `preload` before every subdomain supports HTTPS.
**Verify:** `curl -sI http://<domain>` redirects to `https://`; the sweep shows no `HTTP-URL` hits left; the mobile app's network config has no cleartext allowances.

### Encryption at rest and very sensitive fields
**Covers:** SEC-043, SEC-044, CLD-002, HLT-003, ENT-010
**Safe fix:** confirm the database, storage and backups use the provider's encryption at rest (usually on by default: check, don't assume). Encrypt very sensitive fields (government IDs, health notes, bank details, API tokens you store for users) in the application with a vetted library and keys held in a key manager, not in the code.
**Trap:** writing your own crypto, keeping the key next to the data, or encrypting fields you also need to search on without planning how.
**Verify:** a raw database row shows ciphertext for those fields; the key isn't in the repo or the client; backups are encrypted (dashboard setting confirmed by the user).

### Command injection, template injection and XML entities
**Covers:** SEC-031, SEC-065, SEC-066
**Safe fix:** call programs with an argument array (`execFile`, `subprocess.run([...])`, no shell), never a string with user input. Render user text as **data** in a fixed template. Turn off external entities and DTDs in every XML parser (or use a safe parser such as `defusedxml`).
**Trap:** "escaping" user input and keeping `shell=True`; sanitizing template syntax instead of not compiling user text; fixing one XML parser while SAML or DOCX import uses another.
**Verify:** inputs like `; ls`, `{{7*7}}` and an XML file with an external entity are treated as plain data in a test.

### Secrets in URLs and guessable links
**Covers:** SEC-058, SEC-059
**Safe fix:** tokens go in headers or POST bodies, not query strings. Share and file links use long random IDs (128 bits) or signed, expiring URLs, and private files are fetched through an access check.
**Trap:** switching to UUIDs but keeping the old sequential IDs working, or signed URLs that never expire.
**Verify:** old guessable URLs return 404; signed links stop working after expiry; server and analytics logs show no tokens in URLs.

### GraphQL and real-time channels
**Covers:** SEC-074, SEC-076, COM-009
**Safe fix:** in production, turn off introspection and the playground, and add depth, complexity and batching limits. Check authorization in every resolver (or a shared field-level layer). For WebSocket, Socket.IO, SSE or Realtime: authenticate on connect, check permission for every channel or room join, check `Origin`, and take the user ID from the session, never from the message.
**Trap:** checking auth only on the top-level query or at connect time, then trusting nested resolvers or room joins.
**Verify:** an introspection query fails in production; a deep nested query is rejected; user B can't join user A's room or receive their events.

### Admin tools, debug modes, default passwords and extra domains
**Covers:** BS-11, SEC-080, PLT-016, PLT-021, PLT-043, PLT-044, PLT-048, CLD-010
**Safe fix:** debug off in production; strong, unique framework secrets per environment; admin panels and database tools behind auth (better: VPN or IP allow-list), never public; seeded or default admin passwords removed; preview deployments protected; extra platform domains (`*.workers.dev`, `*.pages.dev`, `*.vercel.app`) disabled or redirected; database, Redis and admin ports closed to the internet.
**Trap:** hiding the admin link but leaving the route open, or disabling the extra domain that the mobile app still calls.
**Verify:** each admin and debug URL returns 401/404 when logged out; the extra domains redirect or 404; a port scan of your own server shows only 80/443.

### Subdomain takeover
**Covers:** SEC-081
**Safe fix:** list every DNS record. For each CNAME pointing at a hosting service, confirm you still own the target (project, bucket, app). Delete records for anything you no longer use.
**Trap:** deleting the hosting project first and the DNS record "later".
**Verify:** each subdomain either serves your content or no longer resolves; nothing shows the provider's "no such app" page.

### Supply chain: packages, CI and third-party scripts
**Covers:** BS-09, SEC-049, SUP-001, SUP-002, SUP-007, SUP-008, SUP-009, SUP-010, SUP-014, SUP-019
**Safe fix:** commit the lockfile and install with `npm ci` (or the equivalent); remove packages you can't identify or that nothing imports; pin GitHub Actions to full commit SHAs; avoid `pull_request_target` with untrusted code; give CI tokens the least permissions (`permissions:` block); turn on secret scanning and push protection; keep only third-party scripts you know and need.
**Trap:** "fixing" a suspicious package by upgrading it instead of asking whether it's real; pinning actions to tags (tags can move).
**Verify:** CI uses the frozen lockfile; every action reference is a 40-character SHA; the repo's security settings show secret scanning on (user confirms).

### Environments, deploys and rollback
**Covers:** OPS-001, OPS-002, OPS-006, OPS-007, OPS-008, PLT-017, PLT-041, FIN-004
**Safe fix:** CI runs lint, type-check, tests and build on every push and PR; `main` is protected; dev, staging and production use separate databases, keys and payment modes (test keys outside production); deploys happen from CI and are traceable to a commit; rollback is one documented command or click.
**Trap:** staging pointing at the production database, or live payment keys in preview deployments.
**Verify:** environment variables differ per environment (user confirms in the dashboard); a test rollback works on staging.

### Accounts, access and spending
**Covers:** OPS-031, OPS-035, MNT-012, MNT-013, CLD-001, CLD-005, CLD-006, CLD-007, PLT-023, PLT-035
**Safe fix:** the business (not one person's personal account) owns the domain, hosting, database, app-store, payment and email accounts; MFA everywhere, with credentials in a password manager; billing alerts and caps on every paid service; no public buckets with private data; no wildcard cloud permissions or long-lived access keys (use roles and OIDC in CI); the repo is private if it holds anything sensitive.
**Trap:** making a bucket "private" while old public URLs or a CDN still serve it.
**Verify:** each item is confirmed by the user in the dashboards (vibe-check can't see them), and public URLs to private files now fail.

### Logs without secrets or personal data
**Covers:** OPS-023
**Safe fix:** log IDs and events, not bodies, headers, tokens, passwords, card or health data; add a redaction step in the logger for known sensitive keys; set log retention to match the privacy policy.
**Trap:** removing one `console.log` while an error tracker still captures full request bodies.
**Verify:** the sweep's `LOG-SENSITIVE` hits are gone, and a test request with a fake token doesn't show it in logs or the error tracker.

### Card data and payment rules
**Covers:** FIN-001, FIN-002, FIN-008, FIN-010, FIN-012, LEG-024, LEG-025, MOB-005, COM-018
**Safe fix:** card details only ever go into the provider's hosted fields or checkout (never your server or logs); amounts are integers in the smallest unit with an explicit currency; a ledger of transactions instead of a single editable balance; payouts go through the provider's connected-accounts features; prices show taxes and renewals clearly; digital goods in mobile apps follow the store's purchase rules. Licensing and money-flow questions go to a lawyer.
**Trap:** floats for money; adjusting a balance column directly; building payouts by hand.
**Verify:** no card fields in your forms or database; a test of rounding and currency conversion passes; balances can be rebuilt from the ledger.

### Broken journeys, buttons, forms and messages
**Covers:** QA-001, QA-002, QA-003, QA-007, QA-008, QA-012, QA-016, QA-020, QA-022, QA-023, QA-024, QA-030, QA-036, UX-012, UX-013, REL-001, REL-036
**Safe fix:** fix the smallest broken piece (the link target, the handler, the API status code), reusing the app's existing components for loading, empty, error and success states and confirmation dialogs. Add an end-to-end test (Playwright or the project's tool) for each main journey and role.
**Trap:** catching the error and showing nothing (now it fails silently), or redesigning the screen while fixing it.
**Verify:** the end-to-end test clicks through the journey on desktop and phone sizes with no console errors and the right success message.

### Accessibility basics
**Covers:** UX-001, UX-002, UX-003, UX-008, LAW-005
**Safe fix:** real `<button>` and `<a>` elements (not clickable `div`s), visible focus, labels on every input, alt text on meaningful images, enough contrast, and layouts that work on a phone. Fix inside the existing design system.
**Trap:** adding ARIA attributes on top of fake controls instead of using real ones.
**Verify:** keyboard-only run-through of the main journeys; `axe` or Lighthouse accessibility shows no serious issues on those pages.

### Email that arrives, and consent to marketing
**Covers:** BS-12, UX-014, UX-020, UX-021, UX-022, UX-026, LAW-007
**Safe fix:** a real email provider with SPF, DKIM and DMARC on the sending domain; transactional and marketing email separated; marketing only with recorded opt-in and a working unsubscribe; OTP and SMS endpoints rate-limited per phone, IP and country; a visible support contact.
**Trap:** testing email only with your own inbox, or letting OTP endpoints send to any number unlimited times.
**Verify:** a test email passes SPF, DKIM and DMARC (from its headers); repeated OTP requests are throttled; unsubscribe works end to end.

### Legal pages and honest selling
**Covers:** LEG-002, LEG-004, LEG-014, LEG-023, LEG-035, LAW-006, LAW-008, LEG-033, LEG-034, POL-001, POL-003
**Safe fix:** draft the missing documents from what the app actually does (data map, providers, retention, refunds, renewals), marked **"DRAFT: needs legal review"**, and link them where users need them. Remove fake urgency, fake reviews, hidden fees and claims the app can't back up. Make cancelling as easy as signing up.
**Trap:** copying a template that promises things the app doesn't do, or deciding a legal question yourself.
**Verify:** each document is linked from signup, checkout and the footer; every claim on the marketing site has evidence; the open legal questions are on the *Needs a lawyer* list.

### Fonts, images and code you don't own
**Covers:** LAW-001, LEG-015, LEG-016, LEG-017
**Safe fix:** self-host fonts whose licence allows it (most open fonts do), replace assets you can't show a licence for, and list open-source licences (replace or isolate GPL/AGPL code in closed-source apps after checking with the user).
**Trap:** downloading a font file but keeping the Google Fonts link in one layout.
**Verify:** the sweep shows no `GOOGLE-FONTS` hits; a licence list exists for fonts, images and packages.

### Chat widgets, session replay and embeds
**Covers:** LAW-003, LAW-004
**Safe fix:** load embeds (video, maps, chat, social) only after consent, or with a click-to-load placeholder; mask all inputs and sensitive screens in session replay, or don't record those pages at all.
**Trap:** masking the password field but recording the card, health or message fields.
**Verify:** with consent declined, the network tab shows no requests to those providers; a replay of a test session shows masked fields.

### Children's data
**Covers:** LEG-036, KID-001, KID-002, KID-003, KID-006, KID-007, KID-008, KID-011, COM-005
**Safe fix:** decide the audience from evidence (`.vibe-check/profile.md`, store rating, reviews), then: a neutral age screen; parental or guardian consent that is verifiable and recorded; collect only what's needed; retention limits enforced by a scheduled job; no trackers, ad pixels or behavioural profiling for minors; nicknames instead of real names in public; separate minors from adult strangers in chat. The consent method and legal basis go to a lawyer.
**Trap:** a "Are you over 18? Yes" checkbox treated as consent, or relying on the terms to say kids aren't allowed.
**Verify:** a test account flagged as a minor sends no analytics, can't be found or messaged by strangers, and has a consent record; old data is deleted on schedule.

### Health data
**Covers:** HLT-001, HLT-005, HLT-006
**Safe fix:** separate, explicit consent before collecting health data; a clear medical disclaimer where advice appears; AI features that touch health show sources, avoid diagnosis and route emergencies to real help. Sharing health data with any third party goes to a lawyer first.
**Trap:** bundling health consent into the general terms, or sending symptoms to an analytics or AI provider without telling the user.
**Verify:** consent is recorded separately; the network tab shows no health data going to analytics; the disclaimer shows where advice appears.

### Community safety
**Covers:** COM-001, COM-002, COM-003, COM-004, COM-013, COM-014, COM-017
**Safe fix:** report, block and mute on every piece of user content and every profile; a moderation queue for staff; automatic filtering for the worst content (including image hash-matching for child abuse material through an approved provider); a notice-and-takedown contact and process; verification for sellers or creators who get paid. Reporting duties go to a lawyer.
**Trap:** a report button that only sends an email nobody reads, or deleting reported abuse material instead of preserving and reporting it as the law requires.
**Verify:** a test report reaches the queue; blocking hides content both ways; the takedown contact works.

### AI data, tools and agents
**Covers:** AIF-011, AIF-016, AGT-001, AGT-002, AGT-003, AGT-011, AGT-016, AGT-017
**Safe fix:** every AI call carries only the current user's data (scope retrieval and memory per user and tenant); strip what the model doesn't need; tools run with the end user's permissions, not admin; risky actions (sending, paying, deleting, publishing) need human confirmation; every agent action is logged; local MCP servers get only the folders and commands they need; tool descriptions say exactly what they do.
**Trap:** one shared vector index or conversation memory across users, or an agent with a service-role key.
**Verify:** user B's question can't retrieve user A's documents; a risky tool call waits for confirmation; the audit log shows who, what and when.

### Mobile store requirements and secure storage
**Covers:** MOB-002, MOB-004, MOB-006, MOB-012
**Safe fix:** a purpose string for every permission the app can trigger (camera, photos, location…); Apple's privacy manifest declaring data and required-reason APIs; the tracking permission prompt before any cross-app tracking; tokens in the Keychain or Android Keystore (secure storage plugins), never in AsyncStorage, localStorage or plain files.
**Trap:** adding a permission string for the camera but not for the photo library the picker also opens.
**Verify:** each permission prompt shows the right text on a real device; the build passes the store's privacy checks; tokens aren't visible in app storage dumps.

### Desktop apps and browser extensions
**Covers:** DSK-001, DSK-002, DSK-003, DSK-004, DSK-005, DSK-011, DSK-012, DSK-013, DSK-014
**Safe fix:** Electron with `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true` and a minimal preload bridge; no remote content with privileges; signed and notarized builds with signed updates; extensions on Manifest V3 with the fewest permissions and host permissions; content scripts that treat the page as hostile; store disclosures that match what's collected.
**Trap:** exposing `ipcRenderer` or `require` to the page through the preload "for convenience".
**Verify:** the page can't reach Node APIs (test in devtools); the update feed is signed; the extension's permissions list matches what it uses.

### Languages and countries
**Covers:** LOC-001, LOC-002, LOC-008, LOC-012
**Safe fix:** no missing translation keys (a test that compares locale files), legal and consent text available in each language you serve, fonts that render every script you support, and prices and currencies formatted with `Intl` in the user's locale with the right currency.
**Trap:** translating the UI but leaving consent, checkout and emails in English.
**Verify:** the locale test passes; checkout in each language shows the right currency and legal text.

### Enterprise readiness
**Covers:** ENT-002, ENT-006, ENT-009
**Safe fix:** roles defined in one place with an admin UI, an append-only audit log of security-relevant actions (who, what, when, from where) that customers can export, and a documented data region with the option to choose one if customers need it.
**Trap:** writing audit logs to the same table users can edit, or promising a data region the provider doesn't actually guarantee.
**Verify:** role changes take effect immediately; audit entries can't be altered by app users; the hosting and database regions match what's promised.

### Logic bugs found by hunting
**Covers:** HUNT-001, HUNT-002, HUNT-003, HUNT-006, REL-012
**Safe fix:** enforce the broken rule where it can't be skipped: a database constraint, an atomic update, a unique index, or a server-side state check (for example "only `paid` orders can ship") in the one function every path uses. Then fix every variant the hunt found, not only the one you proved.
**Trap:** patching the single endpoint you tested while the mobile, `/v1/` or admin path keeps the bug.
**Verify:** the hunt's proof in `.vibe-check/proofs/` now fails to break the rule; the variant search finds no other path; the invariant has a permanent test.

### A safe target for live tests
**Covers:** LIVE-001
**Safe fix:** a staging or local environment with its own database, test accounts, test payment keys and fake email delivery, that can be reset. Record the URL and the user's OK in the ledger.
**Trap:** a "staging" that shares the production database or payment account.
**Verify:** the staging environment variables point at test resources (user confirms); a reset restores the test data.

### Handover: running the app
**Covers:** MNT-007
**Safe fix:** a README with how to install, configure (`.env.example` with every variable, no real values), run, test and deploy the app.
**Trap:** pasting real secrets into the example file.
**Verify:** someone new can clone, copy `.env.example`, and run the app and tests by following the README.

### Hidden instructions for AI tools
**Covers:** SEC-083
**Safe fix:** delete the AI-directed text and strip invisible and bidirectional Unicode characters (show them with `grep -nP '[\x{200B}-\x{200F}\x{202A}-\x{202E}\x{2066}-\x{2069}\x{FEFF}]'`), then find out how it got there: a copied snippet, a dependency, a contributor or a compromised tool. Rules files for AI tools are reviewed like code.
**Trap:** "fixing" it by adding a counter-instruction, or deleting the visible text while the invisible characters stay.
**Verify:** the sweep shows no `AI-INSTRUCTION` or `HIDDEN-UNICODE` hits; `git log -p` on the file shows who added it.

### Views and database functions that skip row-level security
**Covers:** SEC-084
**Safe fix:** `alter view <name> set (security_invoker = on);` for each view the API can reach (Postgres 15+), move materialized views out of exposed schemas, revoke `execute` on `SECURITY DEFINER` functions from `anon` and `authenticated` (or rewrite them as `SECURITY INVOKER`), add `set search_path = ''` to the ones that must stay, and move policy checks off `user_metadata` to `app_metadata` or a table users can't write.
**Trap:** turning RLS off on the underlying table "because the view needs it", or granting `select` on `auth.users` to make a view work.
**Verify:** Supabase Security Advisor shows no `security_definer_view`, `auth_users_exposed` or exposed `SECURITY DEFINER` lints, and a signed-in test user querying the view gets only their own rows.

### Checks that fail open
**Covers:** SEC-085
**Safe fix:** make every guard return "deny" on error: the `catch` refuses the request, a missing secret stops the app at startup instead of skipping verification, a rate limiter that can't reach its store refuses expensive or auth routes, and unknown roles get no access. Log the failure and alert.
**Trap:** swallowing the error to "keep the site up", which is exactly the hole.
**Verify:** with the secret unset, the store stopped or the lookup forced to throw, the protected request is refused (4xx/5xx), never served.

### SAML single sign-on
**Covers:** SEC-086
**Safe fix:** update the SAML library to its latest release (ruby-saml 1.18.0+ or 1.12.4+, samlify 2.10.0+, the current node-saml or python3-saml), require signed assertions, read only the assertion the library returns as verified, check audience, recipient, `NotOnOrAfter` and `InResponseTo`, and store assertion IDs to refuse reuse.
**Trap:** parsing the XML a second time yourself to read the user's email; that reopens signature wrapping.
**Verify:** the library version is patched against the advisories, and a response with an extra unsigned assertion, a changed audience or a replayed ID is refused in a test.

### Client IP, one-time codes and password hashing limits
**Covers:** SEC-087, SEC-088, SEC-089
**Safe fix:** read the client IP only from the platform's verified source or with a fixed trusted-proxy count; mark each OTP and 2FA code used in the same database write that accepts it; cap password length (for example 64 characters) or use Argon2id; never bcrypt a joined string.
**Trap:** trusting the left-most `X-Forwarded-For` value, or a TOTP check that's "valid for 30 seconds" and therefore accepts the same code several times.
**Verify:** a request with a fake `X-Forwarded-For` still hits the rate limit; sending the same valid code twice fails the second time; two passwords that differ only after byte 72 don't both work.

### Authenticated encryption
**Covers:** SEC-090
**Safe fix:** replace ECB or CBC code with AES-256-GCM or libsodium `secretbox`, a fresh random nonce per message, and a key from the secret store; re-encrypt stored data in a migration.
**Trap:** keeping CBC and adding a home-made checksum.
**Verify:** the sweep shows no `WEAK-CIPHER` hits, and changing one byte of a ciphertext makes decryption fail with the same generic error.

### Security alerts
**Covers:** SEC-091
**Safe fix:** send the security events listed in the check to the same alert channel as production errors, with thresholds (for example 20 failed logins a minute) and a named person who gets them.
**Trap:** a dashboard nobody opens.
**Verify:** a test burst of failed logins produces an alert within minutes.
