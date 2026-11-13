# Fix playbook

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
Allow-list fields with a schema. Never write the raw body.
```ts
const UpdateProfile = z.object({ name: z.string().min(1).max(80), bio: z.string().max(500).optional() }).strict();
const data = UpdateProfile.parse(await req.json());   // role, credits, userId are rejected
await db.user.update({ where: { id: session.user.id }, data });
```

## Secrets

### Leaked secret (in code, the client bundle or git history)
Do these in order. **Rotating the key is the fix.** Deleting the line is not.
1. **Rotate now** in the provider dashboard (Stripe, OpenAI, Supabase and so on). Give the user exact steps; you usually can't do this yourself.
2. Move the new value into server-only env vars (not `NEXT_PUBLIC_` / `VITE_` / `EXPO_PUBLIC_`), and into the hosting provider's env settings for each environment.
3. If the browser needed it, put a server route in between that calls the provider.
4. Add `.env*` (except `.env.example`) to `.gitignore`. Turn on GitHub secret scanning and push protection, or gitleaks in CI.
5. Rewriting git history (git filter-repo) is optional once the key is rotated. Tell the user it's a destructive, team-wide operation.

## Data leakage

### API returns too much data
Send a response shape that lists exactly the fields the screen needs (a DTO or `select`), never the raw row:
```ts
const user = await db.user.findUnique({ where: { id }, select: { id: true, name: true, avatarUrl: true } });
```
For server-rendered frameworks, pass only those fields to client components. **Test:** the response for another user's public profile contains no email, phone, password hash or internal flags.

### Account enumeration
Return the same message, with similar timing, whether or not the account exists: *"If an account exists for that email, we've sent a link."* For signup, send a "you already have an account" **email** instead of showing it on screen. Rate-limit these endpoints.

### Private data in shared caches
Add `Cache-Control: private, no-store` to authenticated responses, and make sure CDN or framework caching (e.g. `revalidate`, edge cache rules) is off for personalised routes. **Test:** two users fetch the same URL and each sees only their own data.

## Input and injection

### Server-side validation
One schema per endpoint, parsed on the server, and shared with the form for UX. Reject with 400 or 422 and field errors. Limit string lengths, array sizes and numbers.

### SQL / NoSQL injection
Parameterized queries only: `` sql`select * from users where email = ${email}` `` (tagged template), `$1` placeholders, or ORM methods. For Mongo, validate that inputs are primitives (`z.string()`) so `{ "$gt": "" }` can't get through.

### XSS
- Render user content as text by default (React escapes it automatically).
- If HTML or markdown must render: `DOMPurify.sanitize(html)`, or a markdown renderer with raw HTML disabled (`react-markdown` without `rehype-raw`).
- Validate user URLs: allow only `http:` and `https:` (blocks `javascript:`).

### File uploads
Accept uploads through **signed upload URLs** to a **private** bucket. On the server: check size, check the real type (magic bytes, e.g. the `file-type` package), generate a random filename, and serve files via short-lived signed URLs with `Content-Disposition: attachment` for anything not shown as an image. Don't serve SVG or HTML uploads inline from your main domain.

### Open redirect
`const next = url.startsWith("/") && !url.startsWith("//") ? url : "/";`

### SSRF
Resolve the hostname and block private, loopback, link-local and metadata ranges before fetching. Better still, fetch only from an allow-list of domains. Turn off redirects or re-check after each one.

## Money

### Prices from the client / payments trusted from the redirect
- The client sends a **product or price ID**. The server looks up the amount and creates the checkout session.
- Access is granted only in the **verified webhook** handler. The success page just shows "processing…" and polls your DB.

### Webhook verification and idempotency
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
Use a single atomic statement or a constraint, never read-then-write:
```sql
update accounts set credits = credits - 1 where id = $1 and credits > 0 returning credits;  -- 0 rows → insufficient
create unique index one_redemption_per_user on coupon_redemptions (coupon_id, user_id);
```
For multi-step changes, use a transaction with `select … for update`.

## Reliability

### Timeouts and error handling
```ts
const res = await fetch(url, { signal: AbortSignal.timeout(10_000) });
```
- Set timeouts on DB clients, LLM SDKs (`timeout`, `maxRetries`) and serverless functions.
- One error handler per layer: it logs the full error with a request ID to the error tracker, and returns a generic message plus the right status code to the client. Add a React error boundary or `error.tsx` for the UI.
- Replace every empty `catch {}` with handling, or rethrow.

### Retries
Retry only idempotent operations, with exponential backoff and jitter (e.g. 0.5s, 1s, 2s ± random), at most 3–5 times. Prefer the SDK's built-in retry option.

### Indexes and migrations
Create a migration (Prisma, Drizzle, Supabase or Rails) that adds the index, e.g. `create index concurrently if not exists idx_orders_user_created on orders (user_id, created_at desc);`. Confirm it's used with `EXPLAIN ANALYZE`.

### Backups and restore test
Turn on automated backups and point-in-time recovery in the DB provider. Then help the user **restore into a new staging DB** and check that row counts and a few records match. Record the date and the time it took.

### Error tracking and uptime (quickest path)
Install the framework's official Sentry or PostHog wizard (`npx @sentry/wizard@latest -i nextjs`), set DSNs per environment, and filter personal data out before sending. Add an external uptime check on `/` and `/api/health` with alerts to email, Slack or phone.

## Abuse and cost

### Rate limiting
Use the platform's built-in limiter or a shared store (Upstash Ratelimit, Redis, Cloudflare rules), keyed by user ID, and by IP for anonymous traffic. Apply it to auth, OTP and SMS, email sending, uploads and AI endpoints. Return 429 with `Retry-After`. In-memory limiters don't work on serverless.

### LLM spend caps
- Calls go only through your server, with `max_tokens` and an input length limit.
- A `usage` table (user_id, period, tokens or cost). Check and increment it atomically before each call, and refuse with a friendly "limit reached" message.
- Set a monthly budget and alert in the provider dashboard (give the user the steps).

## Headers and transport

### Security headers (Next.js example)
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
`Set-Cookie: session=…; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=…`. Move tokens out of `localStorage`, using the auth library's cookie mode.

## AI features

### Prompt injection and unsafe output
- Treat model output like user input: sanitize before rendering, and validate with a schema before using it.
- Tools run with the end user's permissions. Destructive tools need a confirmation step in the UI.
- Scope RAG retrieval by `user_id` / `org_id` in the query itself.
- Strip or restrict external images and links in rendered output.

## Legal and privacy

### Privacy policy that doesn't match the app
Generate a draft **from the data map** in Step 1 (each field, purpose, processor, retention, user rights, contact), not from a generic template. Mark it "DRAFT – needs legal review" and put it on the "Needs a lawyer" list.

### Analytics before consent
Load analytics, ads pixels and session replay only after consent: keep the consent state, and initialize the scripts in a callback (or use the tool's consent mode, e.g. Google Consent Mode v2 or PostHog `opt_out_capturing_by_default`). Essential cookies stay on.

### Account and data deletion
- Add a "Delete account" button in settings (required in mobile apps). Re-authenticate, then confirm.
- A server job deletes or anonymizes the user's rows (FK `on delete cascade` or explicit deletes), storage files, and third-party records (payment customer, email list contact, analytics person, AI provider data where possible). Revoke sessions.
- Keep only what the law requires (invoices), documented in the privacy policy.
- **Test:** after deletion, the user's data can't be found anywhere in the DB or storage.

### GPL/AGPL dependency in closed-source code
Replace the package with a permissively licensed alternative, or isolate it. Put the license question on the "Needs a lawyer" list. Don't decide this yourself.
