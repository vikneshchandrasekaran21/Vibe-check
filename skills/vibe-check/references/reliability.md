# Data, reliability and testing

Code-level reliability: APIs, data, background work, performance and tests. Deployment, monitoring, backups and operations are in `devops.md`.

Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence. 🔴 blocks launch · 🟡 before scale · 🟢 recommended.

## APIs and error handling

- [ ] 🔴 **Correct HTTP status codes:** 200/201/204, 400/401/403/404/409/422/429, 500/503. No "200 with an error body".
- [ ] 🔴 **Errors handled.** Users see a friendly message, logs get the details, and stack traces and SQL errors never reach the client.
- [ ] 🔴 **Timeouts** on every outbound HTTP, DB and LLM call, and on serverless functions.
- [ ] 🔴 **Idempotency.** Payment, order and signup endpoints and webhook handlers can safely run twice (idempotency keys, unique constraints, upserts).
- [ ] 🟡 **Retries with exponential backoff and jitter**, with a maximum. Retry only safe or idempotent operations.
- [ ] 🟡 **Webhooks.** Signature verified, 200 returned fast, work done in a background job, duplicate and out-of-order events handled, and a replay path exists.
- [ ] 🟡 **API versioning** (`/v1/` or a header) if mobile apps or third parties call the API.
- [ ] 🟡 **API documentation** (OpenAPI or a README) for any public or partner API.
- [ ] 🟢 **Circuit breakers or fallbacks** for flaky dependencies.

## Database and data

- [ ] 🔴 **Migrations.** Every schema change is a versioned migration in git. No manual edits in the production dashboard.
- [ ] 🔴 **Indexes** on the columns the code filters, joins and sorts on (foreign keys, `user_id`, `created_at`, slugs). Check them against the actual queries.
- [ ] 🔴 **Constraints in the DB:** `NOT NULL`, `UNIQUE`, foreign keys and check constraints, so bad data can't get in even if app code has a bug.
- [ ] 🟡 **Normalized schema**, with no duplicated data that can drift apart. Denormalize only on purpose.
- [ ] 🟡 **Soft deletes** (`deleted_at`) where users may want data back, and **hard deletes** for privacy erasure requests.
- [ ] 🟡 **Connection pooling.** Required on serverless (Supabase pooler, PgBouncer, Neon pooling, Prisma Accelerate).
- [ ] 🟡 **Transactions** around multi-step writes.
- [ ] 🟡 **Optimistic locking** (version column or `updated_at` check) where two users can edit the same thing.
- [ ] 🟡 **UTC timestamps** (`timestamptz`), converted only for display.
- [ ] 🟡 **UTF-8 end to end** (DB, APIs, CSV exports with a BOM for Excel).
- [ ] 🟡 **Pagination** on every list, with limits on page size.
- [ ] 🟢 **Read replicas** when read load outgrows one DB.

## Background work

- [ ] 🟡 **Slow work runs in the background:** emails, AI calls, image or video processing, reports and imports run in a queue, not in the request.
- [ ] 🟡 **Queue with retries and a dead-letter queue** (BullMQ, SQS, Inngest, Trigger.dev, QStash, Cloud Tasks).
- [ ] 🟡 **Cron jobs** can't overlap and are idempotent. (Monitoring them is in `devops.md`.)
- [ ] 🟡 **Cleanup jobs run on a schedule,** not as a side effect of user actions. For example, deleting expired uploads, old logs and sessions shouldn't depend on a user coming back or an admin opening a page.

## Performance and scaling

- [ ] 🟡 **Caching** of expensive reads, with an explicit expiry.
- [ ] 🟡 **Cache invalidation** decided for each cache. Prices, permissions and plan limits are never served stale.
- [ ] 🟡 **CDN** for static assets, and images resized and served in modern formats.
- [ ] 🟡 **Stateless services.** No sessions, uploads or job state in server memory or on local disk.
- [ ] 🟡 **Async correctness.** No missing `await`, no unhandled promise rejections, and independent calls run in parallel (`Promise.all`).
- [ ] 🟡 **Memory leaks.** Listeners, intervals, subscriptions and DB connections are cleaned up.
- [ ] 🟡 **Concurrency.** Shared counters and limits are updated atomically.
- [ ] 🟢 **Load balancing**, reverse proxy (Nginx, Caddy, Cloudflare) and API gateway when the architecture needs them.
- [ ] 🟢 **Horizontal vs vertical scaling.** Know which your setup supports and where it stops.
- [ ] 🟢 **Profiling** before optimizing.

## Testing and process

- [ ] 🔴 **Tests for the money and safety paths,** including a **replay test** for each payment and webhook route: signup, login, password reset, payment, permissions ("user A can't touch user B"), and data deletion.
- [ ] 🟡 **Test pyramid.** Unit tests for logic, integration tests for API plus DB, and E2E (Playwright, Cypress) for the main journeys.
- [ ] 🟡 **Code review.** A human reviews changes to auth, payments, data access, migrations and infrastructure.
- [ ] 🟡 **Branching strategy.** Short-lived branches; main is always deployable.
- [ ] 🟡 **Tech debt written down**, with the shortcuts listed.
- [ ] 🟡 **Project rules file** (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`) recording architecture, conventions and "never do" rules, so future AI sessions stay consistent.
- [ ] 🟢 **Semantic versioning** for APIs, packages and app releases.
- [ ] 🟢 **Docs.** A README covering setup, environment variables and deployment, so someone else could run it.

## Load and stress

**Never load-test or stress-test production, or anything you don't own.** Run these on staging or a local copy, only with the user's approval, and keep paid APIs (AI, SMS, email, payments) in test or mock mode so a test can't create a bill. If there's no safe environment, review the code for the risks below and list the test as "Not checked", with the command for the user.

- [ ] 🔴 **Expensive endpoints are protected before any load arrives:** rate limits, request size limits, pagination caps, timeouts and per-user quotas on AI, uploads, search, exports and sign-ups (see `security.md` and `ai-features.md`).
- [ ] 🟡 **Load test of the main journeys** before launch or a campaign, with a tool such as k6, Artillery, autocannon or Locust: expected peak users × 2, measuring p95 response time and error rate. Record the result and the date.
- [ ] 🟡 **Spike test:** a sudden jump (e.g. 10× normal for 1–2 minutes). The app slows down or queues work, but doesn't crash, corrupt data or double-charge.
- [ ] 🟡 **Realistic data volume:** pages and queries tested with production-sized data (e.g. 100k rows, users with 1,000 items), not just a few test records. Watch for slow queries and memory use.
- [ ] 🟡 **Concurrency test of money and limits:** many parallel requests to payment, credit, coupon and quota endpoints prove there are no double spends or limit bypasses.
- [ ] 🟡 **Graceful overload:** when limits are hit, users get a clear "busy, try again" message (HTTP 429/503 with `Retry-After`), and background queues absorb bursts.
- [ ] 🟡 **Platform limits known:** the serverless timeout, memory, DB connection limit, storage and AI provider rate limits, and what happens when each is hit.
- [ ] 🟢 **Soak test:** a few hours at normal load shows no memory leaks or growing response times.
