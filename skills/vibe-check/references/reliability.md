# Data, reliability, infrastructure and observability

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
- [ ] 🔴 **Backups** are automatic and off-site, with point-in-time recovery if available. **Ask the user whether a restore has ever been tested.**
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
- [ ] 🟡 **Cron jobs** can't overlap, are idempotent, and alert when they fail or don't run.

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
- [ ] 🟢 **Load test** of the main flows (k6, Artillery) before launches and campaigns.
- [ ] 🟢 **Profiling** before optimizing.

## Infrastructure and deployment

- [ ] 🔴 **CI** runs lint, type-check, tests and build on every PR. Main is protected.
- [ ] 🔴 **Rollback.** Deploys can be reverted in minutes.
- [ ] 🔴 **Staging separate from production**, with separate DBs, keys and webhooks. Preview deploys don't use production data or keys.
- [ ] 🔴 **Disaster recovery plan:** what happens if the DB is deleted, a key leaks, the cloud or GitHub account is locked, or the only developer is unavailable. Who has access, and where are the credentials?
- [ ] 🔴 **Cost monitoring.** Billing alerts and caps on cloud, DB, LLM, SMS and email providers.
- [ ] 🟡 **`/health` endpoint** that checks the DB and critical dependencies.
- [ ] 🟡 **Feature flags** for risky features, with a kill switch.
- [ ] 🟡 **Domain and DNS.** Domain auto-renew is on, with registrar 2FA. SSL auto-renews. `www` and the apex redirect consistently.
- [ ] 🟢 **Docker or another reproducible environment.**
- [ ] 🟢 **Infrastructure as Code** (Terraform, Pulumi, SST).
- [ ] 🟢 **Graceful shutdown.** In-flight requests and jobs finish before the process stops.

## Observability

- [ ] 🔴 **Error tracking** on frontend and backend (Sentry, PostHog, Bugsnag, Rollbar), with source maps uploaded privately.
- [ ] 🔴 **No sensitive data in logs:** grep logging calls for passwords, tokens, auth headers, card data, full request bodies and personal data.
- [ ] 🔴 **Uptime monitoring** from outside (BetterStack, UptimeRobot, Checkly), with alerts that reach a human.
- [ ] 🟡 **Structured JSON logs** with request ID, user ID and route.
- [ ] 🟡 **Dashboards** for latency, error rate, traffic and saturation.
- [ ] 🟡 **Alerting** on things that need action, without noise.
- [ ] 🟡 **Status page** or a way to tell users about outages.
- [ ] 🟢 **Distributed tracing** (OpenTelemetry) once there are several services.

## Testing and process

- [ ] 🔴 **Tests for the money and safety paths:** signup, login, password reset, payment, permissions ("user A can't touch user B"), and data deletion.
- [ ] 🟡 **Test pyramid.** Unit tests for logic, integration tests for API plus DB, and E2E (Playwright, Cypress) for the main journeys.
- [ ] 🟡 **Code review.** A human reviews changes to auth, payments, data access, migrations and infrastructure.
- [ ] 🟡 **Branching strategy.** Short-lived branches; main is always deployable.
- [ ] 🟡 **Tech debt written down**, with the shortcuts listed.
- [ ] 🟡 **Project rules file** (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`) recording architecture, conventions and "never do" rules, so future AI sessions stay consistent.
- [ ] 🟢 **Semantic versioning** for APIs, packages and app releases.
- [ ] 🟢 **Docs.** A README covering setup, environment variables and deployment, so someone else could run it.
