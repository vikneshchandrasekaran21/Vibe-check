# Platform-specific traps

Check the sections for the stack you found in Step 1. These are the problems that come up again and again in AI-built apps on each platform.

## Supabase

- [ ] 🔴 PLT-001 RLS is **enabled on every table** in exposed schemas (`select relname, relrowsecurity from pg_class join pg_namespace n on n.oid = relnamespace where nspname = 'public' and relkind = 'r';`).
- [ ] 🔴 PLT-002 No policy uses `using (true)` or `with check (true)` on user data. Policies use `auth.uid()` and have a `WITH CHECK` on insert and update.
- [ ] 🔴 PLT-003 The `service_role` key is used only in server code or edge functions, never in the client or `NEXT_PUBLIC_`/`VITE_` variables. (The anon key in the client is fine *only* because RLS protects the data.)
- [ ] 🔴 PLT-004 Storage buckets holding private files are **not public**, and storage policies check ownership.
- [ ] 🔴 PLT-005 `security definer` functions and RPCs check the caller's permissions, set `search_path`, and aren't callable by `anon` unless intended.
- [ ] 🔴 PLT-006 Views don't bypass RLS (use `security_invoker = true` on Postgres 15+).
- [ ] 🟡 PLT-007 The Supabase **Security Advisor and Performance Advisor** in the dashboard show no errors.
- [ ] 🟡 PLT-008 Auth settings: email confirmation on, a sensible OTP expiry, leaked-password protection, redirect URLs restricted, and the rate limits reviewed.
- [ ] 🟡 PLT-009 Using the connection pooler for serverless. Point-in-time recovery or backups on the right plan.
- [ ] 🟡 PLT-010 Edge functions verify the JWT unless they're deliberately public (webhooks verify signatures instead).

## Firebase / Firestore

- [ ] 🔴 PLT-011 Firestore, Realtime Database and Storage rules are not in test mode (`allow read, write: if true` or a date-based rule that expires).
- [ ] 🔴 PLT-012 Rules check `request.auth.uid` against document ownership and validate the fields written (users can't set `role` or `isAdmin`).
- [ ] 🟡 PLT-013 App Check is enabled to cut down abuse of the public config.
- [ ] 🟡 PLT-014 Cloud Functions validate auth and input. Admin SDK use is restricted to trusted code.
- [ ] 🟡 PLT-015 Budget alerts are set. Firestore reads can explode in cost with unbounded listeners.

## Vercel / Netlify / Cloudflare Pages

- [ ] 🔴 PLT-016 **Preview deployments** don't use production DBs or live payment keys, and are protected (Vercel Deployment Protection) if they expose real data.
- [ ] 🔴 PLT-017 Environment variables are scoped per environment (Production / Preview / Development).
- [ ] 🟡 PLT-018 Serverless function timeouts and regions are set, with spend management or limits on.
- [ ] 🟡 PLT-019 Production source maps aren't publicly downloadable, or that's a deliberate decision.

## Cloudflare (Workers, Pages, D1, R2)

- [ ] 🔴 PLT-020 **Always Use HTTPS** is on, and the **minimum TLS version is 1.2** (SSL/TLS → Edge Certificates). Check live: `curl -I http://<domain>` should redirect, and `curl --tlsv1.1 --tls-max 1.1 https://<domain>` should fail.
- [ ] 🔴 PLT-021 **`*.workers.dev` and `*.pages.dev` routes** are disabled for production Workers, or redirected to the real domain (they bypass custom-domain rules and may expose a personal account name).
- [ ] 🔴 PLT-022 Secrets are set with `wrangler secret put` or the dashboard, not in `wrangler.toml` `[vars]`.
- [ ] 🔴 PLT-023 R2 buckets with private data have no public access and no `r2.dev` URL. Files are served through signed URLs or the Worker.
- [ ] 🟡 PLT-024 D1 has Time Travel/backups, and a restore has been tested. Migrations are done with `wrangler d1 migrations`.
- [ ] 🟡 PLT-025 The deploy runs the tests first (CI, then `wrangler deploy`), not only deploy-on-push.
- [ ] 🟡 PLT-026 Preview and dev Workers have their own bindings (DB, KV, R2), never production's.

## Next.js

- [ ] 🔴 PLT-027 **Server Actions and Route Handlers each check auth and authorization themselves.** Middleware alone is not enough (and older versions had middleware bypass bugs, so keep Next.js patched).
- [ ] 🔴 PLT-028 No secrets in `NEXT_PUBLIC_*`. Server-only modules import `server-only`.
- [ ] 🔴 PLT-029 Data passed to Client Components doesn't include fields the user shouldn't see (password hashes, other users' emails, internal flags). Use DTOs or `taintObjectReference` where useful.
- [ ] 🟡 PLT-030 `revalidate` and caching don't serve one user's private data to another.
- [ ] 🟡 PLT-031 `next.config` `images.remotePatterns` isn't a wildcard that turns your app into an open image proxy.

## Lovable / Bolt / v0 / Replit Agent / Firebase Studio (browser builders)

- [ ] 🔴 PLT-032 Read the generated Supabase or Firebase rules yourself. These tools often scaffold permissive rules to make the demo work.
- [ ] 🔴 PLT-033 Secrets are in the platform's secrets manager (Replit Secrets, Lovable or Supabase secrets), not in code. If the project or repo is public, assume earlier secrets have leaked and rotate them.
- [ ] 🔴 PLT-034 Payment and AI calls go through a backend or edge function, not straight from the browser.
- [ ] 🔴 PLT-035 The project or repo isn't accidentally **public** with real data or keys.
- [ ] 🟡 PLT-036 Export the code to GitHub so you have history, backups and the ability to run real tooling (`npm audit`, tests).
- [ ] 🟡 PLT-037 A custom domain with HTTPS, and the platform's default subdomain redirects or is noindexed.

## Stripe / Razorpay / Paddle / Lemon Squeezy

- [ ] 🔴 PLT-038 Webhook signatures are verified with the endpoint secret, using the **raw** request body.
- [ ] 🔴 PLT-039 Price IDs or amounts come from the server. Never trust an amount sent by the client.
- [ ] 🔴 PLT-040 Access is granted from webhook events (`checkout.session.completed`, `invoice.paid`, `payment.captured`), and revoked on `customer.subscription.deleted`, failed payments and refunds.
- [ ] 🔴 PLT-041 Live keys only in production. Test mode was used to rehearse success, failure, refund, dispute and cancellation.
- [ ] 🟡 PLT-042 Customer portal or self-serve cancellation.

## Express / Fastify / Django / Flask / Rails / Laravel

- [ ] 🔴 PLT-043 Debug mode is off in production (`DEBUG=False`, `app.debug=False`, `APP_DEBUG=false`, `NODE_ENV=production`).
- [ ] 🔴 PLT-044 The framework's secret key or session secret is strong, unique per environment, and not committed.
- [ ] 🔴 PLT-045 `ALLOWED_HOSTS`, CSRF middleware and secure-cookie settings are configured.
- [ ] 🟡 PLT-046 `helmet` (Express) or the framework's security middleware is on. The body size limit is set.
- [ ] 🟡 PLT-047 The admin panel (Django admin, Rails admin and so on) is at a non-default path, with strong auth and 2FA.

## Expo / React Native / Flutter

- See `mobile.md`. Plus: `EXPO_PUBLIC_*` variables are visible to anyone, so never put secrets there.

## Docker / VPS / self-hosted

- [ ] 🔴 PLT-048 Database, Redis and admin ports aren't open to the internet. A firewall allows only 80, 443 and SSH (key-only, no root login).
- [ ] 🔴 PLT-049 Containers don't run as root where avoidable, and no secrets are baked into images (`docker history`).
- [ ] 🟡 PLT-050 OS and images are updated regularly. Unattended security upgrades are on.
- [ ] 🟡 PLT-051 Backups are stored off the server.
