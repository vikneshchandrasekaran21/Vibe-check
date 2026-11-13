# Security and authentication

Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence. 🔴 blocks launch · 🟡 before scale · 🟢 recommended.

## Authentication and sessions

- [ ] 🔴 **Proven auth provider.** Supabase Auth, Clerk, Auth0, Firebase Auth, NextAuth/Auth.js, Lucia or similar. No hand-rolled password or JWT logic.
- [ ] 🔴 **Sessions end.** Sessions expire, logout invalidates them on the server, and a password change ends other sessions.
- [ ] 🔴 **Cookie flags.** Auth cookies are `HttpOnly`, `Secure` and `SameSite=Lax` or `Strict`. No long-lived tokens in `localStorage`.
- [ ] 🔴 **JWTs verified properly.** Signature checked, `alg: none` rejected, expiry enforced, and the secret is strong and kept on the server.
- [ ] 🔴 **Password reset and magic links.** Tokens are single-use, expire in 15–60 minutes, and are stored hashed. The response is the same whether or not the email exists.
- [ ] 🔴 **Email verification** before the account can do anything sensitive (if it matters for this product).
- [ ] 🔴 **Brute-force protection.** Rate limits on login, OTP, signup, password reset and verification resends, by IP and by account.
- [ ] 🟡 **Account lockout or CAPTCHA** after repeated failures, without letting attackers permanently lock out real users.
- [ ] 🟡 **Token expiry and refresh rotation.** Short-lived access tokens, rotating refresh tokens, and a way to revoke them.
- [ ] 🟡 **2FA**, at least for admin accounts.
- [ ] 🟡 **OAuth done right.** `state` parameter used, redirect URIs exact-matched (no wildcards), and accounts aren't auto-linked by unverified email.
- [ ] 🟢 **Passkeys** if the provider supports them.
- [ ] 🟢 **SSO (SAML/OIDC)** if selling to companies.

## Access control

- [ ] 🔴 **Authorization on every request.** Checked on the server for every route, server action, RPC and edge function, not just in the UI or middleware.
- [ ] 🔴 **No IDOR.** Changing an ID in a URL or body never exposes or changes another user's data. Prefer UUIDs, but still check ownership.
- [ ] 🔴 **Roles in one place.** Defined centrally and enforced on the server. Users can't change their own role.
- [ ] 🔴 **Row-Level Security / security rules.** On for every table, collection and storage bucket, with policies for select, insert, update and delete. `WITH CHECK` on insert and update so users can't write rows for others.
- [ ] 🔴 **No mass assignment.** Writes allow-list fields.
- [ ] 🔴 **Least privilege.** DB users, service accounts, API keys, CI tokens and team members get only what they need. The service-role or admin SDK is never used where the user's own session would do.
- [ ] 🔴 **Multi-tenant isolation** (if there are teams or orgs). Every query is scoped by tenant, and invites can't be replayed or used to join other orgs.
- [ ] 🟡 **Audit log** for admin actions, permission changes, payments, exports and deletions.

## Secrets and keys

- [ ] 🔴 **No secrets in the repo, git history, client bundle or public env vars.** If one has ever leaked, rotate it. Deleting the line is not enough.
- [ ] 🔴 **Separate keys per environment.** Test keys in dev and staging, live keys only in production.
- [ ] 🔴 **The app's own API keys** (if you issue them) are stored hashed, scoped and revocable.
- [ ] 🟡 **Rotation plan.** A documented way to rotate every secret quickly.
- [ ] 🟡 **Secret scanning on.** GitHub secret scanning and push protection, or gitleaks/trufflehog in CI.

## Injection and input

- [ ] 🔴 **Input validation on the server** of type, length, format and range, using a schema (Zod, Valibot, Joi, Pydantic).
- [ ] 🔴 **SQL injection.** Parameterized queries or an ORM only. No string-concatenated SQL, including in `.rpc()`, raw queries and `sql.unsafe`.
- [ ] 🔴 **NoSQL injection.** No user objects passed straight into Mongo or Firestore queries (`{ $gt: "" }`).
- [ ] 🔴 **XSS.** No `dangerouslySetInnerHTML`, `v-html`, `innerHTML` or markdown-to-HTML on user content without sanitizing (DOMPurify). URLs from users are checked against `javascript:`.
- [ ] 🔴 **Command injection.** No `exec`, `spawn` with a shell, `eval`, `new Function` or `child_process` with user input.
- [ ] 🔴 **File uploads.** Type is checked by content (not just extension), size is limited, files get random names, they're stored in a private bucket with signed URLs, and SVG/HTML aren't served inline from your domain.
- [ ] 🟡 **Path traversal.** File paths are never built from user input (`../../`).
- [ ] 🟡 **SSRF.** Server-side fetches of URLs users supply block private IP ranges and cloud metadata (`169.254.169.254`).
- [ ] 🟡 **Open redirects.** `?next=`, `?redirect=` and `?returnTo=` only allow relative paths or an allow-list.
- [ ] 🟡 **CSRF.** SameSite cookies, plus CSRF tokens or origin checks for state-changing requests that use cookie auth.
- [ ] 🟡 **CORS.** No `Access-Control-Allow-Origin: *` together with credentials. Allowed origins are an explicit list.
- [ ] 🟡 **Deserialization.** No `pickle`, `yaml.load` (unsafe) or `unserialize` on untrusted input.
- [ ] 🟡 **Regex DoS.** No catastrophic regex on user input.

## Transport, headers and crypto

- [ ] 🔴 **HTTPS everywhere**, with HTTP redirected to HTTPS and HSTS on.
- [ ] 🔴 **Passwords hashed** with argon2id or bcrypt (salted automatically). Never encrypted, plain text, MD5 or SHA-*.
- [ ] 🟡 **Hashing vs encryption.** Hashing for things you only verify (passwords, tokens); encryption for things you need back (keys for third-party accounts and similar).
- [ ] 🔴 **Encryption at rest** for the DB, file storage and backups (check the provider's setting; most managed DBs and storage encrypt by default, so confirm it). 🔴 for apps with children's, health, financial or ID data; 🟡 otherwise.
- [ ] 🔴 **Field-level encryption for very sensitive data** (government IDs, health records, bank details, stored OAuth or API tokens of users), with keys kept outside the DB. N/A if the app stores none.
- [ ] 🔴 **Encryption in transit** everywhere: HTTPS for the app and API, TLS to the DB, storage and between services, and no `http://` calls to third parties.
- [ ] 🟡 **Security headers:** `Content-Security-Policy` (start report-only), `frame-ancestors` or `X-Frame-Options` (clickjacking), `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`. Check with securityheaders.com.
- [ ] 🟡 **Cryptographic randomness** for tokens and IDs (`crypto.randomUUID` or `crypto.getRandomValues`, never `Math.random`).

## Dependencies and supply chain

- [ ] 🔴 **`npm audit` / `pnpm audit` / `pip-audit` / `bundle audit`** run, with no unresolved critical or high findings that are reachable.
- [ ] 🔴 **Every package is real and reputable:** check downloads, maintainers and last release. Watch for typosquats.
- [ ] 🟡 **Lockfile committed** and versions pinned. Dependabot or Renovate enabled.
- [ ] 🟡 **No unneeded packages.** Remove what isn't used.
- [ ] 🟢 **Pentest.** At least an OWASP ZAP baseline scan against staging. A professional pentest before enterprise deals or sensitive data.

## Rate limiting and abuse

- [ ] 🔴 **Rate limits** on auth, password reset, OTP and SMS (to prevent SMS-pumping fraud), email sending, LLM calls, file uploads, search, exports and any expensive endpoint.
- [ ] 🟡 **Bot protection** on signup and public forms (Turnstile, hCaptcha, honeypot).

## Data leakage

Check how data could reach someone who shouldn't see it, even when access control looks right.

- [ ] 🔴 **API responses return only what the screen needs:** no password hashes, tokens, internal flags, other users' emails or phone numbers, or whole database rows (`select *` sent to the client). Check list endpoints, search, public profiles, exports and server-rendered page data.
- [ ] 🔴 **No account enumeration:** signup, login, password reset and invite flows don't reveal whether an email or phone number is registered (same message and similar timing), or, where the product must say so, they're rate-limited.
- [ ] 🔴 **Private data isn't cached for others:** responses with personal data send `Cache-Control: private, no-store`. CDN, edge and framework caches never serve one user's page or API response to another.
- [ ] 🔴 **No secrets or personal data in URLs:** tokens, emails and IDs aren't in query strings (they end up in logs, browser history, analytics and `Referer` headers). Reset and magic links are single-use, and `Referrer-Policy` is set.
- [ ] 🔴 **Share and file links aren't guessable:** long random IDs or signed, expiring URLs for shared reports, invoices, uploads and exports. No sequential IDs.
- [ ] 🟡 **Third parties get only what they need:** analytics, error tracking, session replay, chat widgets and AI providers don't receive passwords, form contents, health data or children's data. Session replay masks inputs. Error tracking scrubs personal data.
- [ ] 🟡 **Client bundles and source don't expose internals:** no admin routes, internal API keys, feature flags for unreleased paid features, or other customers' data in JavaScript bundles, HTML comments or `__NEXT_DATA__` and similar.
- [ ] 🟡 **Exports and downloads** (CSV, PDF, backups) are access-checked and logged, include only the requester's data, and are protected against CSV formula injection (`=`, `+`, `-`, `@` at the start of cells).
- [ ] 🟡 **No sensitive data in emails and notifications:** they don't include sensitive data in subject lines or lock-screen previews, and go only to verified addresses.
- [ ] 🟡 **Deleted data is really gone:** deleted accounts, files and messages are removed from search indexes, caches, CDN, storage buckets and third parties within the stated time.
