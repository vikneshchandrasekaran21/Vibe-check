# Security and authentication

Mark each item PASS / FAIL / N/A / CAN'T TELL, with evidence. 🔴 blocks launch · 🟡 before scale · 🟢 recommended.

## Authentication and sessions

- [ ] 🔴 SEC-001 **Proven auth provider.** Supabase Auth, Clerk, Auth0, Firebase Auth, NextAuth/Auth.js, Lucia or similar. No hand-rolled password or JWT logic.
- [ ] 🔴 SEC-002 **Sessions end.** Sessions expire, logout invalidates them on the server, and a password change ends other sessions.
- [ ] 🔴 SEC-003 **Cookie flags.** Auth cookies are `HttpOnly`, `Secure` and `SameSite=Lax` or `Strict`. No long-lived tokens in `localStorage`.
- [ ] 🔴 SEC-004 **JWTs verified properly.** Signature checked, `alg: none` rejected, expiry enforced, and the secret is strong and kept on the server.
- [ ] 🔴 SEC-005 **Password reset and magic links.** Tokens are single-use, expire in 15–60 minutes, and are stored hashed. The response is the same whether or not the email exists.
- [ ] 🔴 SEC-006 **Email verification** before the account can do anything sensitive (if it matters for this product).
- [ ] 🔴 SEC-007 **Brute-force protection.** Rate limits on login, OTP, signup, password reset and verification resends, by IP and by account.
- [ ] 🟡 SEC-008 **Account lockout or CAPTCHA** after repeated failures, without letting attackers permanently lock out real users.
- [ ] 🟡 SEC-009 **Token expiry and refresh rotation.** Short-lived access tokens, rotating refresh tokens, and a way to revoke them.
- [ ] 🟡 SEC-010 **2FA**, at least for admin accounts.
- [ ] 🟡 SEC-011 **OAuth done right.** `state` parameter used, redirect URIs exact-matched (no wildcards), and accounts aren't auto-linked by unverified email.
- [ ] 🟢 SEC-012 **Passkeys** if the provider supports them.
- [ ] 🟢 SEC-013 **SSO (SAML/OIDC)** if selling to companies.

## Access control

- [ ] 🔴 SEC-014 **Authorization on every request.** Checked on the server for every route, server action, RPC and edge function, not just in the UI or middleware.
- [ ] 🔴 SEC-015 **No IDOR.** Changing an ID in a URL or body never exposes or changes another user's data. Prefer UUIDs, but still check ownership.
- [ ] 🔴 SEC-016 **Roles in one place.** Defined centrally and enforced on the server. Users can't change their own role.
- [ ] 🔴 SEC-017 **Row-Level Security / security rules.** On for every table, collection and storage bucket, with policies for select, insert, update and delete. `WITH CHECK` on insert and update so users can't write rows for others.
- [ ] 🔴 SEC-018 **No mass assignment.** Writes allow-list fields.
- [ ] 🔴 SEC-019 **Least privilege.** DB users, service accounts, API keys, CI tokens and team members get only what they need. The service-role or admin SDK is never used where the user's own session would do.
- [ ] 🔴 SEC-020 **Multi-tenant isolation** (if there are teams or orgs). Every query is scoped by tenant, and invites can't be replayed or used to join other orgs.
- [ ] 🟡 SEC-021 **Audit log** for admin actions, permission changes, payments, exports and deletions.

## Secrets and keys

- [ ] 🔴 SEC-022 **No secrets in the repo, git history, client bundle or public env vars.** If one has ever leaked, rotate it. Deleting the line is not enough.
- [ ] 🔴 SEC-023 **Separate keys per environment.** Test keys in dev and staging, live keys only in production.
- [ ] 🔴 SEC-024 **The app's own API keys** (if you issue them) are stored hashed, scoped and revocable.
- [ ] 🟡 SEC-025 **Rotation plan.** A documented way to rotate every secret quickly.
- [ ] 🟡 SEC-026 **Secret scanning on.** GitHub secret scanning and push protection, or gitleaks/trufflehog in CI.

## Injection and input

- [ ] 🔴 SEC-027 **Input validation on the server** of type, length, format and range, using a schema (Zod, Valibot, Joi, Pydantic).
- [ ] 🔴 SEC-028 **SQL injection.** Parameterized queries or an ORM only. No string-concatenated SQL, including in `.rpc()`, raw queries and `sql.unsafe`.
- [ ] 🔴 SEC-029 **NoSQL injection.** No user objects passed straight into Mongo or Firestore queries (`{ $gt: "" }`).
- [ ] 🔴 SEC-030 **XSS.** No `dangerouslySetInnerHTML`, `v-html`, `innerHTML` or markdown-to-HTML on user content without sanitizing (DOMPurify). URLs from users are checked against `javascript:`.
- [ ] 🔴 SEC-031 **Command injection.** No `exec`, `spawn` with a shell, `eval`, `new Function` or `child_process` with user input.
- [ ] 🔴 SEC-032 **File uploads.** Type is checked by content (not just extension), size is limited, files get random names, they're stored in a private bucket with signed URLs, and SVG/HTML aren't served inline from your domain.
- [ ] 🟡 SEC-033 **Path traversal.** File paths are never built from user input (`../../`).
- [ ] 🟡 SEC-034 **SSRF.** Server-side fetches of URLs users supply block private IP ranges and cloud metadata (`169.254.169.254`).
- [ ] 🟡 SEC-035 **Open redirects.** `?next=`, `?redirect=` and `?returnTo=` only allow relative paths or an allow-list.
- [ ] 🟡 SEC-036 **CSRF.** SameSite cookies, plus CSRF tokens or origin checks for state-changing requests that use cookie auth.
- [ ] 🟡 SEC-037 **CORS.** No `Access-Control-Allow-Origin: *` together with credentials. Allowed origins are an explicit list.
- [ ] 🟡 SEC-038 **Deserialization.** No `pickle`, `yaml.load` (unsafe) or `unserialize` on untrusted input.
- [ ] 🟡 SEC-039 **Regex DoS.** No catastrophic regex on user input.

## Transport, headers and crypto

- [ ] 🔴 SEC-040 **HTTPS everywhere**, with HTTP redirected to HTTPS and HSTS on.
- [ ] 🔴 SEC-041 **Passwords hashed** with argon2id or bcrypt (salted automatically). Never encrypted, plain text, MD5 or SHA-*.
- [ ] 🟡 SEC-042 **Hashing vs encryption.** Hashing for things you only verify (passwords, tokens); encryption for things you need back (keys for third-party accounts and similar).
- [ ] 🔴 SEC-043 **Encryption at rest** for the DB, file storage and backups (check the provider's setting; most managed DBs and storage encrypt by default, so confirm it). 🔴 for apps with children's, health, financial or ID data; 🟡 otherwise.
- [ ] 🔴 SEC-044 **Field-level encryption for very sensitive data** (government IDs, health records, bank details, stored OAuth or API tokens of users), with keys kept outside the DB. N/A if the app stores none.
- [ ] 🔴 SEC-045 **Encryption in transit** everywhere: HTTPS for the app and API, TLS to the DB, storage and between services, and no `http://` calls to third parties.
- [ ] 🟡 SEC-046 **Security headers:** `Content-Security-Policy` (start report-only), `frame-ancestors` or `X-Frame-Options` (clickjacking), `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`. Check with securityheaders.com.
- [ ] 🟡 SEC-047 **Cryptographic randomness** for tokens and IDs (`crypto.randomUUID` or `crypto.getRandomValues`, never `Math.random`).

## Dependencies and supply chain

- [ ] 🔴 SEC-048 **`npm audit` / `pnpm audit` / `pip-audit` / `bundle audit`** run, with no unresolved critical or high findings that are reachable.
- [ ] 🔴 SEC-049 **Every package is real and reputable:** check downloads, maintainers and last release. Watch for typosquats.
- [ ] 🟡 SEC-050 **Lockfile committed** and versions pinned. Dependabot or Renovate enabled.
- [ ] 🟡 SEC-051 **No unneeded packages.** Remove what isn't used.
- [ ] 🟢 SEC-052 **Pentest.** At least an OWASP ZAP baseline scan against staging. A professional pentest before enterprise deals or sensitive data.

## Rate limiting and abuse

- [ ] 🔴 SEC-053 **Rate limits** on auth, password reset, OTP and SMS (to prevent SMS-pumping fraud), email sending, LLM calls, file uploads, search, exports and any expensive endpoint.
- [ ] 🟡 SEC-054 **Bot protection** on signup and public forms (Turnstile, hCaptcha, honeypot).

## Data leakage

Check how data could reach someone who shouldn't see it, even when access control looks right.

- [ ] 🔴 SEC-055 **API responses return only what the screen needs:** no password hashes, tokens, internal flags, other users' emails or phone numbers, or whole database rows (`select *` sent to the client). Check list endpoints, search, public profiles, exports and server-rendered page data.
- [ ] 🔴 SEC-056 **No account enumeration:** signup, login, password reset and invite flows don't reveal whether an email or phone number is registered (same message and similar timing), or, where the product must say so, they're rate-limited.
- [ ] 🔴 SEC-057 **Private data isn't cached for others:** responses with personal data send `Cache-Control: private, no-store`. CDN, edge and framework caches never serve one user's page or API response to another.
- [ ] 🔴 SEC-058 **No secrets or personal data in URLs:** tokens, emails and IDs aren't in query strings (they end up in logs, browser history, analytics and `Referer` headers). Reset and magic links are single-use, and `Referrer-Policy` is set.
- [ ] 🔴 SEC-059 **Share and file links aren't guessable:** long random IDs or signed, expiring URLs for shared reports, invoices, uploads and exports. No sequential IDs.
- [ ] 🟡 SEC-060 **Third parties get only what they need:** analytics, error tracking, session replay, chat widgets and AI providers don't receive passwords, form contents, health data or children's data. Session replay masks inputs. Error tracking scrubs personal data.
- [ ] 🟡 SEC-061 **Client bundles and source don't expose internals:** no admin routes, internal API keys, feature flags for unreleased paid features, or other customers' data in JavaScript bundles, HTML comments or `__NEXT_DATA__` and similar.
- [ ] 🟡 SEC-062 **Exports and downloads** (CSV, PDF, backups) are access-checked and logged, include only the requester's data, and are protected against CSV formula injection (`=`, `+`, `-`, `@` at the start of cells).
- [ ] 🟡 SEC-063 **No sensitive data in emails and notifications:** they don't include sensitive data in subject lines or lock-screen previews, and go only to verified addresses.
- [ ] 🟡 SEC-064 **Deleted data is really gone:** deleted accounts, files and messages are removed from search indexes, caches, CDN, storage buckets and third parties within the stated time.

## Often missed by developers and testers
- [ ] 🔴 SEC-065 **No template injection (SSTI):** user input is never compiled as a template (`render_template_string(user_input)`, `Template(req.body…)`, Twig/Blade/EJS/Handlebars/Jinja rendered from user text). User text is passed as data into a fixed template.
- [ ] 🔴 SEC-066 **No XML external entities (XXE):** XML parsers (SAML, SVG, DOCX/XLSX imports, RSS, SOAP) have external entities and DTDs turned off.
- [ ] 🟡 SEC-067 **No prototype pollution (JavaScript):** request bodies are never deep-merged into objects (`_.merge`, `Object.assign` with nested user input, custom `deepMerge`); keys like `__proto__`, `constructor` and `prototype` are rejected; schema validation runs first.
- [ ] 🟡 SEC-068 **No header or CRLF injection:** user input never goes into response headers, redirect `Location`, cookies, log lines or email headers without stripping line breaks.
- [ ] 🔴 SEC-069 **Links in emails don't trust the Host header:** password-reset, magic-link, invite and verification URLs are built from a configured base URL (`APP_URL`), never from `req.headers.host`, `$_SERVER['HTTP_HOST']` or `request.host`. Otherwise an attacker sends a reset to the victim that points at the attacker's domain.
- [ ] 🟡 SEC-070 **Caches can't be poisoned or tricked:** CDN or proxy caches don't key private pages on attacker-controlled headers, and don't cache personal pages under public-looking URLs (web cache deception, for example `/account/settings.css`). Unusual front-end/back-end server chains get checked for request smuggling.
- [ ] 🔴 SEC-071 **Sensitive account changes need re-authentication and a notice:** changing the email, password, 2FA, payout details or connected logins requires the current password (or a fresh login), sends a notice to the **old** email, and ends other sessions on password change.
- [ ] 🟡 SEC-072 **Secrets are compared in constant time:** API keys, webhook signatures, reset tokens and OTPs are compared with `crypto.timingSafeEqual`, `hmac.compare_digest`, `hash_equals` or the platform's verify function, never `==`/`===`.
- [ ] 🟡 SEC-073 **Identifiers are normalized:** emails and usernames are compared after lowercasing and Unicode normalization (NFKC), so `Admin@x.com`, `admin@x.com` and look-alike characters can't create a second account or take over the first.
- [ ] 🔴 SEC-074 **GraphQL is locked down** (if used): introspection off in production, query depth and complexity limits, batching and alias limits, and authorization on every field and nested resolver, not only on the top-level query.
- [ ] 🔴 SEC-075 **Every API endpoint checks object and function access:** each endpoint, including old versions (`/v1/`), mobile-only, internal and admin endpoints, checks that the caller may touch **this** object (BOLA) and may call **this** function (BFLA). List them from the inventory and check each one.
- [ ] 🔴 SEC-076 **Real-time connections are authenticated:** WebSocket, Socket.IO, SSE and realtime channels check the session on connect **and** per channel or room, verify the `Origin`, and don't trust user IDs sent in messages.
- [ ] 🟡 SEC-077 **Archive uploads are extracted safely:** ZIP/TAR extraction blocks `../` paths and absolute paths (zip slip), limits total size and file count (zip bombs), and never extracts into a served folder.
- [ ] 🟡 SEC-078 **File processors can't be turned against the server:** SVGs are sanitized or served as downloads, HTML-to-PDF and screenshot tools can't fetch internal URLs or local files, and image libraries (ImageMagick, sharp, Pillow) are patched with risky formats disabled.
- [ ] 🔴 SEC-079 **No sensitive files are reachable on the live site:** read-only checks return 404 for `/.git/HEAD`, `/.env`, `/.env.production`, backup files (`.zip`, `.sql`, `.bak`, `~`), `/phpinfo.php`, `/.DS_Store`, `/server-status`, `/actuator` and source maps on private apps.
- [ ] 🔴 SEC-080 **No default credentials or open admin tools:** no default or seeded admin passwords, and admin panels, database tools (phpMyAdmin, Adminer, Supabase Studio), queue dashboards, Swagger "try it" consoles and debug toolbars aren't public in production.
- [ ] 🔴 SEC-081 **No subdomain takeover:** every DNS record (CNAME to Vercel, Netlify, Heroku, GitHub Pages, S3, Azure…) points at a resource the user still owns. Dangling records let someone else serve content on your domain.
- [ ] 🟡 SEC-082 **Static analysis has run:** Semgrep (`semgrep --config auto`), CodeQL, or the language's scanner (Bandit, gosec, Brakeman, PHPStan/Psalm security rules) ran, and its findings were reviewed with the second look. If none is installed, say so in *Tools run* and rely on the sweep.
