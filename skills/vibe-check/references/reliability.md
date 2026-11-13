# Data, reliability and testing

Code-level reliability: APIs, data, background work, performance and tests. Deployment, monitoring, backups and operations are in `devops.md`.

Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence. 🔴 blocks launch · 🟡 before scale · 🟢 recommended.

## APIs and error handling

- [ ] 🔴 REL-001 **Correct HTTP status codes:** 200/201/204, 400/401/403/404/409/422/429, 500/503. No "200 with an error body".
- [ ] 🔴 REL-002 **Errors handled.** Users see a friendly message, logs get the details, and stack traces and SQL errors never reach the client.
- [ ] 🔴 REL-003 **Timeouts** on every outbound HTTP, DB and LLM call, and on serverless functions.
- [ ] 🔴 REL-004 **Idempotency.** Payment, order and signup endpoints and webhook handlers can safely run twice (idempotency keys, unique constraints, upserts).
- [ ] 🟡 REL-005 **Retries with exponential backoff and jitter**, with a maximum. Retry only safe or idempotent operations.
- [ ] 🟡 REL-006 **Webhooks.** Signature verified, 200 returned fast, work done in a background job, duplicate and out-of-order events handled, and a replay path exists.
- [ ] 🟡 REL-007 **API versioning** (`/v1/` or a header) if mobile apps or third parties call the API.
- [ ] 🟡 REL-008 **API documentation** (OpenAPI or a README) for any public or partner API.
- [ ] 🟢 REL-009 **Circuit breakers or fallbacks** for flaky dependencies.

## Database and data

- [ ] 🔴 REL-010 **Migrations.** Every schema change is a versioned migration in git. No manual edits in the production dashboard.
- [ ] 🔴 REL-011 **Indexes** on the columns the code filters, joins and sorts on (foreign keys, `user_id`, `created_at`, slugs). Check them against the actual queries.
- [ ] 🔴 REL-012 **Constraints in the DB:** `NOT NULL`, `UNIQUE`, foreign keys and check constraints, so bad data can't get in even if app code has a bug.
- [ ] 🟡 REL-013 **Normalized schema**, with no duplicated data that can drift apart. Denormalize only on purpose.
- [ ] 🟡 REL-014 **Soft deletes** (`deleted_at`) where users may want data back, and **hard deletes** for privacy erasure requests.
- [ ] 🟡 REL-015 **Connection pooling.** Required on serverless (Supabase pooler, PgBouncer, Neon pooling, Prisma Accelerate).
- [ ] 🟡 REL-016 **Transactions** around multi-step writes.
- [ ] 🟡 REL-017 **Optimistic locking** (version column or `updated_at` check) where two users can edit the same thing.
- [ ] 🟡 REL-018 **UTC timestamps** (`timestamptz`), converted only for display.
- [ ] 🟡 REL-019 **UTF-8 end to end** (DB, APIs, CSV exports with a BOM for Excel).
- [ ] 🟡 REL-020 **Pagination** on every list, with limits on page size.
- [ ] 🟢 REL-021 **Read replicas** when read load outgrows one DB.

## Background work

- [ ] 🟡 REL-022 **Slow work runs in the background:** emails, AI calls, image or video processing, reports and imports run in a queue, not in the request.
- [ ] 🟡 REL-023 **Queue with retries and a dead-letter queue** (BullMQ, SQS, Inngest, Trigger.dev, QStash, Cloud Tasks).
- [ ] 🟡 REL-024 **Cron jobs** can't overlap and are idempotent. (Monitoring them is in `devops.md`.)
- [ ] 🟡 REL-025 **Cleanup jobs run on a schedule,** not as a side effect of user actions. For example, deleting expired uploads, old logs and sessions shouldn't depend on a user coming back or an admin opening a page.

## Performance and scaling

- [ ] 🟡 REL-026 **Caching** of expensive reads, with an explicit expiry.
- [ ] 🟡 REL-027 **Cache invalidation** decided for each cache. Prices, permissions and plan limits are never served stale.
- [ ] 🟡 REL-028 **CDN** for static assets, and images resized and served in modern formats.
- [ ] 🟡 REL-029 **Stateless services.** No sessions, uploads or job state in server memory or on local disk.
- [ ] 🟡 REL-030 **Async correctness.** No missing `await`, no unhandled promise rejections, and independent calls run in parallel (`Promise.all`).
- [ ] 🟡 REL-031 **Memory leaks.** Listeners, intervals, subscriptions and DB connections are cleaned up.
- [ ] 🟡 REL-032 **Concurrency.** Shared counters and limits are updated atomically.
- [ ] 🟢 REL-033 **Load balancing**, reverse proxy (Nginx, Caddy, Cloudflare) and API gateway when the architecture needs them.
- [ ] 🟢 REL-034 **Horizontal vs vertical scaling.** Know which your setup supports and where it stops.
- [ ] 🟢 REL-035 **Profiling** before optimizing.

## Testing and process

- [ ] 🔴 REL-036 **Tests for the money and safety paths,** including a **replay test** for each payment and webhook route: signup, login, password reset, payment, permissions ("user A can't touch user B"), and data deletion.
- [ ] 🟡 REL-037 **Test pyramid.** Unit tests for logic, integration tests for API plus DB, and E2E (Playwright, Cypress) for the main journeys.
- [ ] 🟡 REL-038 **Code review.** A human reviews changes to auth, payments, data access, migrations and infrastructure.
- [ ] 🟡 REL-039 **Branching strategy.** Short-lived branches; main is always deployable.
- [ ] 🟡 REL-040 **Tech debt written down**, with the shortcuts listed.
- [ ] 🟡 REL-041 **Project rules file** (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`) recording architecture, conventions and "never do" rules, so future AI sessions stay consistent.
- [ ] 🟢 REL-042 **Semantic versioning** for APIs, packages and app releases.
- [ ] 🟢 REL-043 **Docs.** A README covering setup, environment variables and deployment, so someone else could run it.

## Load and stress

**Never load-test or stress-test production, or anything you don't own.** Run these on staging or a local copy, only with the user's approval, and keep paid APIs (AI, SMS, email, payments) in test or mock mode so a test can't create a bill. If there's no safe environment, review the code for the risks below and list the test as "Not checked", with the command for the user.

- [ ] 🔴 REL-044 **Expensive endpoints are protected before any load arrives:** rate limits, request size limits, pagination caps, timeouts and per-user quotas on AI, uploads, search, exports and sign-ups (see `security.md` and `ai-features.md`).
- [ ] 🟡 REL-045 **Load test of the main journeys** before launch or a campaign, with a tool such as k6, Artillery, autocannon or Locust: expected peak users × 2, measuring p95 response time and error rate. Record the result and the date.
- [ ] 🟡 REL-046 **Spike test:** a sudden jump (e.g. 10× normal for 1–2 minutes). The app slows down or queues work, but doesn't crash, corrupt data or double-charge.
- [ ] 🟡 REL-047 **Realistic data volume:** pages and queries tested with production-sized data (e.g. 100k rows, users with 1,000 items), not just a few test records. Watch for slow queries and memory use.
- [ ] 🟡 REL-048 **Concurrency test of money and limits:** many parallel requests to payment, credit, coupon and quota endpoints prove there are no double spends or limit bypasses.
- [ ] 🟡 REL-049 **Graceful overload:** when limits are hit, users get a clear "busy, try again" message (HTTP 429/503 with `Retry-After`), and background queues absorb bursts.
- [ ] 🟡 REL-050 **Platform limits known:** the serverless timeout, memory, DB connection limit, storage and AI provider rate limits, and what happens when each is hit.
- [ ] 🟢 REL-051 **Soak test:** a few hours at normal load shows no memory leaks or growing response times.
