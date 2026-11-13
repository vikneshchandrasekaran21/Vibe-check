# Supply chain and CI security

Load this file for every Full and Enterprise check. Attackers increasingly get in through **dependencies, build pipelines and third-party scripts** rather than the app's own code. Check `package.json` and lockfiles, `.github/workflows/`, other CI configs, and every `<script src>` loaded from another domain.

## Dependencies
- [ ] 🔴 SUP-001 **Lockfile committed and used:** `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `poetry.lock` or `requirements.txt` with pinned versions. CI installs with `npm ci` / `pnpm install --frozen-lockfile` (not a plain `npm install` that can drift).
- [ ] 🔴 SUP-002 **No suspicious or unknown packages:** every dependency is real, widely used and maintained. Check for typosquats (e.g. `reqeusts`, `lodahs`), very new packages with few downloads, and packages added by AI tools that don't match their purpose.
- [ ] 🟡 SUP-003 **Install scripts reviewed:** dependencies with `preinstall`/`postinstall` scripts are known and needed. Consider `npm config set ignore-scripts true` for CI where possible, or an allow-list.
- [ ] 🟡 SUP-004 **No dependencies from Git URLs, tarballs or personal forks** unless intentional and pinned to a commit.
- [ ] 🟡 SUP-005 **Unused dependencies removed** (`npx depcheck` or similar): fewer packages, fewer risks.
- [ ] 🟡 SUP-006 **Private package scopes protected:** internal package names are scoped (`@company/…`) and registries configured, so a public package with the same name can't be installed instead (dependency confusion).

## CI/CD pipelines (GitHub Actions and similar)
- [ ] 🔴 SUP-007 **Third-party actions pinned to a full commit SHA** (not `@main` or `@v1`), at least for actions that touch secrets or deploy.
- [ ] 🔴 SUP-008 **No dangerous triggers:** `pull_request_target` or `workflow_run` workflows never check out and run code from a fork with access to secrets.
- [ ] 🔴 SUP-009 **Least-privilege tokens:** `permissions:` set per workflow (default `contents: read`). Deploy tokens are scoped to one project, and short-lived OIDC credentials are used for cloud deploys where possible.
- [ ] 🔴 SUP-010 **Secrets never printed or exposed:** no `echo $SECRET`, no secrets in build logs, artifacts, caches or client bundles. Secrets aren't available to pull requests from forks.
- [ ] 🟡 SUP-011 **No untrusted input in shell steps:** PR titles, branch names and issue text aren't interpolated directly into `run:` commands (`${{ github.event.pull_request.title }}`). Pass them through environment variables instead.
- [ ] 🟡 SUP-012 **Production deploys need the main branch and passing checks.** Environment protection rules or required reviewers for production.
- [ ] 🟢 SUP-013 **Build provenance / signed artifacts** for packages or containers you publish.

## Third-party scripts in the browser
- [ ] 🔴 SUP-014 **Every external script is known and needed:** list each `<script src>` from another domain (analytics, chat, A/B testing, tag managers, widgets). Each one can read the page, including forms and tokens.
- [ ] 🟡 SUP-015 **Subresource Integrity (SRI)** (`integrity="sha384-…"` plus `crossorigin`) on scripts and styles loaded from public CDNs with fixed versions, or self-host them.
- [ ] 🟡 SUP-016 **Tag managers are locked down:** few people can publish tags, and changes are reviewed. A tag manager can inject any script into production.
- [ ] 🟡 SUP-017 **Script sources restricted by CSP:** the Content Security Policy limits which domains scripts can load from (see `security.md`).
- [ ] 🟡 SUP-018 **Third-party scripts don't load on sensitive pages** (login, payment, password reset, admin), or are reviewed for those pages.

## Repository and accounts
- [ ] 🔴 SUP-019 **Secret scanning and push protection are on** for the repository.
- [ ] 🟡 SUP-020 **Branch protection and required reviews** on the default branch, and `CODEOWNERS` for sensitive paths (auth, payments, infra, workflows).
- [ ] 🟡 SUP-021 **Signed commits or verified committers** for maintainers, and 2FA required for the organisation.
- [ ] 🟢 SUP-022 **An SBOM can be generated** (e.g. `npx @cyclonedx/cyclonedx-npm`) for customers or audits.
