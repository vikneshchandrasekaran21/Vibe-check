# Platform-specific traps

Check the sections for the stack you found in Step 1. These are the problems that come up again and again in AI-built apps on each platform.

## Supabase

- [ ] 🔴 RLS is **enabled on every table** in exposed schemas (`select relname, relrowsecurity from pg_class join pg_namespace n on n.oid = relnamespace where nspname = 'public' and relkind = 'r';`).
- [ ] 🔴 No policy uses `using (true)` or `with check (true)` on user data. Policies use `auth.uid()` and have a `WITH CHECK` on insert and update.
- [ ] 🔴 The `service_role` key is used only in server code or edge functions, never in the client or `NEXT_PUBLIC_`/`VITE_` variables. (The anon key in the client is fine *only* because RLS protects the data.)
- [ ] 🔴 Storage buckets holding private files are **not public**, and storage policies check ownership.
- [ ] 🔴 `security definer` functions and RPCs check the caller's permissions, set `search_path`, and aren't callable by `anon` unless intended.
- [ ] 🔴 Views don't bypass RLS (use `security_invoker = true` on Postgres 15+).
- [ ] 🟡 The Supabase **Security Advisor and Performance Advisor** in the dashboard show no errors.
- [ ] 🟡 Auth settings: email confirmation on, a sensible OTP expiry, leaked-password protection, redirect URLs restricted, and the rate limits reviewed.
- [ ] 🟡 Using the connection pooler for serverless. Point-in-time recovery or backups on the right plan.
- [ ] 🟡 Edge functions verify the JWT unless they're deliberately public (webhooks verify signatures instead).

## Firebase / Firestore

- [ ] 🔴 Firestore, Realtime Database and Storage rules are not in test mode (`allow read, write: if true` or a date-based rule that expires).
- [ ] 🔴 Rules check `request.auth.uid` against document ownership and validate the fields written (users can't set `role` or `isAdmin`).
- [ ] 🟡 App Check is enabled to cut down abuse of the public config.
- [ ] 🟡 Cloud Functions validate auth and input. Admin SDK use is restricted to trusted code.
- [ ] 🟡 Budget alerts are set. Firestore reads can explode in cost with unbounded listeners.

## Vercel / Netlify / Cloudflare Pages

- [ ] 🔴 **Preview deployments** don't use production DBs or live payment keys, and are protected (Vercel Deployment Protection) if they expose real data.
- [ ] 🔴 Environment variables are scoped per environment (Production / Preview / Development).
- [ ] 🟡 Serverless function timeouts and regions are set, with spend management or limits on.
- [ ] 🟡 Production source maps aren't publicly downloadable, or that's a deliberate decision.

## Cloudflare (Workers, Pages, D1, R2)

- [ ] 🔴 **Always Use HTTPS** is on, and the **minimum TLS version is 1.2** (SSL/TLS → Edge Certificates). Check live: `curl -I http://<domain>` should redirect, and `curl --tlsv1.1 --tls-max 1.1 https://<domain>` should fail.
- [ ] 🔴 **`*.workers.dev` and `*.pages.dev` routes** are disabled for production Workers, or redirected to the real domain (they bypass custom-domain rules and may expose a personal account name).
- [ ] 🔴 Secrets are set with `wrangler secret put` or the dashboard, not in `wrangler.toml` `[vars]`.
- [ ] 🔴 R2 buckets with private data have no public access and no `r2.dev` URL. Files are served through signed URLs or the Worker.
- [ ] 🟡 D1 has Time Travel/backups, and a restore has been tested. Migrations are done with `wrangler d1 migrations`.
- [ ] 🟡 The deploy runs the tests first (CI, then `wrangler deploy`), not only deploy-on-push.
- [ ] 🟡 Preview and dev Workers have their own bindings (DB, KV, R2), never production's.

## Next.js

- [ ] 🔴 **Server Actions and Route Handlers each check auth and authorization themselves.** Middleware alone is not enough (and older versions had middleware bypass bugs, so keep Next.js patched).
- [ ] 🔴 No secrets in `NEXT_PUBLIC_*`. Server-only modules import `server-only`.
- [ ] 🔴 Data passed to Client Components doesn't include fields the user shouldn't see (password hashes, other users' emails, internal flags). Use DTOs or `taintObjectReference` where useful.
- [ ] 🟡 `revalidate` and caching don't serve one user's private data to another.
- [ ] 🟡 `next.config` `images.remotePatterns` isn't a wildcard that turns your app into an open image proxy.

## Lovable / Bolt / v0 / Replit Agent / Firebase Studio (browser builders)

- [ ] 🔴 Read the generated Supabase or Firebase rules yourself. These tools often scaffold permissive rules to make the demo work.
- [ ] 🔴 Secrets are in the platform's secrets manager (Replit Secrets, Lovable or Supabase secrets), not in code. If the project or repo is public, assume earlier secrets have leaked and rotate them.
- [ ] 🔴 Payment and AI calls go through a backend or edge function, not straight from the browser.
- [ ] 🔴 The project or repo isn't accidentally **public** with real data or keys.
- [ ] 🟡 Export the code to GitHub so you have history, backups and the ability to run real tooling (`npm audit`, tests).
- [ ] 🟡 A custom domain with HTTPS, and the platform's default subdomain redirects or is noindexed.

## Stripe / Razorpay / Paddle / Lemon Squeezy

- [ ] 🔴 Webhook signatures are verified with the endpoint secret, using the **raw** request body.
- [ ] 🔴 Price IDs or amounts come from the server. Never trust an amount sent by the client.
- [ ] 🔴 Access is granted from webhook events (`checkout.session.completed`, `invoice.paid`, `payment.captured`), and revoked on `customer.subscription.deleted`, failed payments and refunds.
- [ ] 🔴 Live keys only in production. Test mode was used to rehearse success, failure, refund, dispute and cancellation.
- [ ] 🟡 Customer portal or self-serve cancellation.

## Express / Fastify / Django / Flask / Rails / Laravel

- [ ] 🔴 Debug mode is off in production (`DEBUG=False`, `app.debug=False`, `APP_DEBUG=false`, `NODE_ENV=production`).
- [ ] 🔴 The framework's secret key or session secret is strong, unique per environment, and not committed.
- [ ] 🔴 `ALLOWED_HOSTS`, CSRF middleware and secure-cookie settings are configured.
- [ ] 🟡 `helmet` (Express) or the framework's security middleware is on. The body size limit is set.
- [ ] 🟡 The admin panel (Django admin, Rails admin and so on) is at a non-default path, with strong auth and 2FA.

## Expo / React Native / Flutter

- See the mobile section of `launch-ux.md`. Plus: `EXPO_PUBLIC_*` variables are visible to anyone, so never put secrets there.

## Docker / VPS / self-hosted

- [ ] 🔴 Database, Redis and admin ports aren't open to the internet. A firewall allows only 80, 443 and SSH (key-only, no root login).
- [ ] 🔴 Containers don't run as root where avoidable, and no secrets are baked into images (`docker history`).
- [ ] 🟡 OS and images are updated regularly. Unattended security upgrades are on.
- [ ] 🟡 Backups are stored off the server.
