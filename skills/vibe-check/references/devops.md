# DevOps and operations

Load this file for every Full and Enterprise check. It covers how the app is built, deployed, watched, backed up and recovered, and who can operate it. Many items are settings or processes rather than code: check config files (`.github/workflows`, `wrangler.*`, `vercel.json`, `netlify.toml`, `fly.toml`, `Dockerfile`, `package.json` scripts, IaC), run safe read-only commands, and ask the user for anything that lives in a dashboard. Record the evidence or the question for each item.

## CI and code flow
- [ ] 🔴 OPS-001 **CI runs on every push and PR:** install, lint, type-check, tests and build (e.g. a GitHub Actions workflow). A local "release check" script doesn't count unless deploys can't skip it.
- [ ] 🔴 OPS-002 **The main branch is protected:** PRs and passing checks required, no force-pushes. → ask the user, or check the repo settings with `gh api` if available.
- [ ] 🟡 OPS-003 **Dependency updates are automated** (Dependabot or Renovate), with security alerts on.
- [ ] 🟡 OPS-004 **Secret scanning and push protection** are on for the repo.
- [ ] 🟡 OPS-005 **Reproducible builds:** lockfile committed, runtime version pinned (`.nvmrc`, `engines`, `.tool-versions`, `runtime.txt`).

## Environments and deploys
- [ ] 🔴 OPS-006 **Dev, staging and production are separate,** with separate DBs, storage buckets, keys, webhooks and OAuth apps. Preview deploys never use production data or live keys.
- [ ] 🔴 OPS-007 **Deploys are automated and traceable:** every production deploy maps to a commit, and the tests run before it.
- [ ] 🔴 OPS-008 **Rollback in minutes:** a known way to go back to the previous version (platform rollback, redeploy a tag), plus how to handle DB migrations when rolling back. → ask if not documented.
- [ ] 🟡 OPS-009 **Migrations run as part of the deploy,** are backwards-compatible where possible, and are tested on staging first.
- [ ] 🟡 OPS-010 **Feature flags or a kill switch** for risky or costly features (AI, payments, sign-ups).
- [ ] 🟡 OPS-011 **Platform default domains** (`*.workers.dev`, `*.vercel.app`, `*.netlify.app`, `*.pages.dev`, `*.fly.dev`) are disabled or redirect to the real domain.
- [ ] 🟢 OPS-012 **Infrastructure as Code** (Terraform, Pulumi, SST, wrangler config in git), so the setup can be rebuilt.
- [ ] 🟢 OPS-013 **Graceful shutdown:** in-flight requests and jobs finish before the process stops (for long-running servers).

## Monitoring and alerting
- [ ] 🔴 OPS-014 **Error tracking with alerts:** production errors (frontend and backend) go to a tool that **notifies a human** (Sentry, PostHog, Bugsnag, Rollbar, Cloudflare/Vercel alerts). An admin page that nobody watches doesn't count.
- [ ] 🔴 OPS-015 **Outside uptime monitoring** of the main site and API (BetterStack, UptimeRobot, Checkly), with alerts to email, phone or Slack.
- [ ] 🔴 OPS-016 **Scheduled jobs are monitored:** a cron or heartbeat monitor alerts if a job fails **or stops running** (e.g. Healthchecks.io, Cronitor, Sentry Crons).
- [ ] 🟡 OPS-017 **A health check endpoint** (`/health`) that checks the DB and critical dependencies, used by the uptime monitor.
- [ ] 🟡 OPS-018 **Third-party outages are handled:** calls to AI, payment, auth and email providers have timeouts, limited retries, and a friendly fallback message. Check each provider the app calls.
- [ ] 🟡 OPS-019 **Structured logs** with request ID, user ID and route, kept for a defined period, searchable when something breaks.
- [ ] 🟡 OPS-020 **Alerts are actionable:** few and meaningful (error spikes, downtime, failed jobs, payment webhook failures), each with a clear owner.
- [ ] 🟢 OPS-021 **Dashboards** for traffic, latency, error rate and resource use.
- [ ] 🟢 OPS-022 **Status page,** or another way to tell users about outages.

## Logs and data in operations
- [ ] 🔴 OPS-023 **No secrets or sensitive personal data in logs:** grep logging calls and error handlers for passwords, tokens, auth headers, card data, dates of birth, health data and full request bodies.
- [ ] 🟡 OPS-024 **Log retention matches the privacy policy,** and is enforced by a scheduled job or platform setting, not manually.
- [ ] 🟡 OPS-025 **Admin and support tools** that show user data have their own auth, 2FA and an access log.

## Backups and recovery
- [ ] 🔴 OPS-026 **Automatic, off-site backups** of the database (point-in-time recovery if available) and of important file storage.
- [ ] 🔴 OPS-027 **A restore has been tested,** with a date recorded and how long it took. → ask the user. Never tested = FAIL.
- [ ] 🔴 OPS-028 **Disaster recovery plan:** what happens if the DB is deleted, a key leaks, the cloud, GitHub or app-store account is locked, or the only developer is unavailable.
- [ ] 🟡 OPS-029 **Recovery targets known:** how much data could be lost (RPO) and how long recovery would take (RTO).

## Secrets and access
- [ ] 🔴 OPS-030 **Production secrets live in the platform's secret store,** not in config files or the repo.
- [ ] 🔴 OPS-031 **MFA on every critical account:** cloud, GitHub, domain registrar, DNS, payment provider, email provider, app stores, AI providers. → ask the user.
- [ ] 🟡 OPS-032 **Secret rotation:** a documented way to rotate each key quickly, and rotation after anyone with access leaves.
- [ ] 🟡 OPS-033 **Bus factor:** at least two trusted people can access and operate production. Accounts belong to the company, not one personal login.
- [ ] 🟡 OPS-034 **Least privilege for people and tokens:** CI tokens, deploy keys and team members get only the access they need.

## Costs, domains and certificates
- [ ] 🔴 OPS-035 **Billing alerts and spending caps** on cloud, database, storage, AI, SMS and email providers. → ask the user.
- [ ] 🟡 OPS-036 **Domain auto-renew is on,** with registrar lock and 2FA, and the expiry date is known.
- [ ] 🟡 OPS-037 **SSL/TLS certificates renew automatically,** and an expiry alert exists (many uptime tools include this).
- [ ] 🟡 OPS-038 **Email sending domain** has SPF, DKIM and DMARC, and transactional email (verification, password reset, receipts, alerts) actually arrives. Check that the app has an email provider at all.

## Incidents
- [ ] 🟡 OPS-039 **Incident runbook:** who gets alerted, first steps (roll back, disable feature, rotate key), how users are told, and the legal notification timelines (e.g. CERT-In 6 hours in India, GDPR 72 hours).
- [ ] 🟢 OPS-040 **Post-incident notes** are written, so the same failure doesn't repeat.
