# Supply chain and CI security

Load this file for every Full and Enterprise check. Attackers increasingly get in through **dependencies, build pipelines and third-party scripts** rather than the app's own code. Check `package.json` and lockfiles, `.github/workflows/`, other CI configs, and every `<script src>` loaded from another domain.

## Dependencies
- [ ] 🔴 **Lockfile committed and used:** `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock` or `requirements.txt` with pinned versions. CI installs with `npm ci` / `pnpm install --frozen-lockfile` (not a plain `npm install` that can drift).
- [ ] 🔴 **No suspicious or unknown packages:** every dependency is real, widely used and maintained. Check for typosquats (e.g. `reqeusts`, `lodahs`), very new packages with few downloads, and packages added by AI tools that don't match their purpose.
- [ ] 🟡 **Install scripts reviewed:** dependencies with `preinstall`/`postinstall` scripts are known and needed. Consider `npm config set ignore-scripts true` for CI where possible, or an allow-list.
- [ ] 🟡 **No dependencies from Git URLs, tarballs or personal forks** unless intentional and pinned to a commit.
- [ ] 🟡 **Unused dependencies removed** (`npx depcheck` or similar): fewer packages, fewer risks.
- [ ] 🟡 **Private package scopes protected:** internal package names are scoped (`@company/…`) and registries configured, so a public package with the same name can't be installed instead (dependency confusion).

## CI/CD pipelines (GitHub Actions and similar)
- [ ] 🔴 **Third-party actions pinned to a full commit SHA** (not `@main` or `@v1`), at least for actions that touch secrets or deploy.
- [ ] 🔴 **No dangerous triggers:** `pull_request_target` or `workflow_run` workflows never check out and run code from a fork with access to secrets.
- [ ] 🔴 **Least-privilege tokens:** `permissions:` set per workflow (default `contents: read`). Deploy tokens are scoped to one project, and short-lived OIDC credentials are used for cloud deploys where possible.
- [ ] 🔴 **Secrets never printed or exposed:** no `echo $SECRET`, no secrets in build logs, artifacts, caches or client bundles. Secrets aren't available to pull requests from forks.
- [ ] 🟡 **No untrusted input in shell steps:** PR titles, branch names and issue text aren't interpolated directly into `run:` commands (`${{ github.event.pull_request.title }}`). Pass them through environment variables instead.
- [ ] 🟡 **Production deploys need the main branch and passing checks.** Environment protection rules or required reviewers for production.
- [ ] 🟢 **Build provenance / signed artifacts** for packages or containers you publish.

## Third-party scripts in the browser
- [ ] 🔴 **Every external script is known and needed:** list each `<script src>` from another domain (analytics, chat, A/B testing, tag managers, widgets). Each one can read the page, including forms and tokens.
- [ ] 🟡 **Subresource Integrity (SRI)** (`integrity="sha384-…"` plus `crossorigin`) on scripts and styles loaded from public CDNs with fixed versions, or self-host them.
- [ ] 🟡 **Tag managers are locked down:** few people can publish tags, and changes are reviewed. A tag manager can inject any script into production.
- [ ] 🟡 **Script sources restricted by CSP:** the Content Security Policy limits which domains scripts can load from (see `security.md`).
- [ ] 🟡 **Third-party scripts don't load on sensitive pages** (login, payment, password reset, admin), or are reviewed for those pages.

## Repository and accounts
- [ ] 🔴 **Secret scanning and push protection are on** for the repository.
- [ ] 🟡 **Branch protection and required reviews** on the default branch, and `CODEOWNERS` for sensitive paths (auth, payments, infra, workflows).
- [ ] 🟡 **Signed commits or verified committers** for maintainers, and 2FA required for the organisation.
- [ ] 🟢 **An SBOM can be generated** (e.g. `npx @cyclonedx/cyclonedx-npm`) for customers or audits.
