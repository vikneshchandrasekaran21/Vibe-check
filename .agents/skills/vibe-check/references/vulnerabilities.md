# Known vulnerabilities in everything the app runs

Load this file for every Full and Enterprise check (Quick runs its 🔴 items). Package audits only check the **libraries** an app installs. Attackers also go after the **language runtime, framework, CMS, plugins, web server and container image** the app runs on, and a single advisory in any of them (for example a remote-code-execution bug in a language runtime) can put every app on that version at risk. This module checks every component against **today's** advisories.

**Never from memory (ground rule 12).** Versions come from the project files or the live site, and "is this version safe?" comes from a source opened during this run: put the URL and the date in the ledger row. Training data is months old; advisories are not.

**Privacy (ground rule 13).** Look products up **one at a time on public pages** (a runtime's release page, endoflife.date, an advisory page). Never paste the user's dependency list into a website. Package lists are checked by the ecosystem's own audit tool, which the user runs as their tool.

## What's running
- [ ] 🔴 VUL-001 **Every component is listed with its exact version:** run `scripts/versions.py` and add what it missed. Runtime (PHP, Node, Python, Ruby, Java, Go, .NET), framework, CMS **and every plugin or theme**, packages (by ecosystem), web server, Docker base image, database engine, mobile SDK, and the hosting runtime (for example a Workers compatibility date or a platform's Node version). Record where each version came from.
- [ ] 🔴 VUL-002 **Production runs what the repo says:** compare with the live site using read-only requests (`curl -sI`: `Server`, `X-Powered-By`, a `generator` meta tag), the hosting dashboard or the deploy log. A different version in production is a finding of its own.

## Checked against today's advisories
- [ ] 🔴 VUL-003 **The runtime has its latest security release:** compare the exact version with the runtime's official release or security page, opened now (for example php.net, nodejs.org, python.org). Any security release newer than the running version is 🔴 until updated or mitigated.
- [ ] 🔴 VUL-004 **Nothing is end-of-life:** runtime, framework, CMS, database engine and base image are all still supported (check endoflife.date for the product, plus the official page). Past end-of-life = 🔴 (no more security fixes). Within 90 days of end-of-life = 🟡 with the date.
- [ ] 🔴 VUL-005 **Packages have no known critical or high vulnerabilities:** run the audit tool for **every** ecosystem in the project (table below), plus `osv-scanner` if installed. For each critical or high result, say whether the app actually calls the vulnerable code, and the fixed version.
- [ ] 🔴 VUL-006 **Nothing on CISA's Known Exploited Vulnerabilities (KEV) list:** check every CVE found against the KEV catalog (cisa.gov/known-exploited-vulnerabilities-catalog). A KEV entry is 🔴 whatever its score: attackers are already using it.
- [ ] 🔴 VUL-007 **Framework and CMS on a supported, patched release:** Next.js, Nuxt, SvelteKit, Remix, Express, NestJS, Laravel, Symfony, Django, Flask, FastAPI, Rails, Spring, WordPress core **and each plugin and theme**, Drupal, Strapi, Ghost, Shopify apps… Check the project's own security advisories page or GitHub Security Advisories. Unmaintained plugins (no release in 2+ years) are 🟡 even without a known CVE.
- [ ] 🔴 VUL-008 **Containers and servers are current:** the Docker base image is pinned to a specific supported tag (not `latest`, not an end-of-life distro), and nginx, Apache, Caddy or Node servers on a VPS are on supported, patched versions. Use `trivy image <name>` or `docker scout cves` when installed.
- [ ] 🟡 VUL-009 **The database engine and managed services are on supported versions** (Postgres, MySQL, Redis, MongoDB, Elasticsearch…). On managed platforms, check the dashboard for pending upgrades or deprecation notices.
- [ ] 🟡 VUL-010 **Mobile and native SDKs are supported:** Expo SDK, React Native, Flutter, Capacitor, Electron or Tauri versions are within their support window. Old SDKs block store submissions and miss security fixes.
- [ ] 🟡 VUL-011 **When an upgrade can't happen today, the official workaround is applied:** quote the mitigation from the advisory itself (for example a configuration setting the vendor says to change), confirm it's applied, and give a dated upgrade plan.
- [ ] 🟡 VUL-012 **The version isn't advertised:** production doesn't send `X-Powered-By`, detailed `Server` headers or `generator` tags with version numbers (PHP: `expose_php = Off`; Express: `app.disable('x-powered-by')`). It doesn't stop attacks, but it stops mass scanners from picking you.

## Staying patched
- [ ] 🟡 VUL-013 **Automatic update pull requests cover everything:** Dependabot or Renovate updates packages **and** Docker base images, GitHub Actions and runtime version files, and security updates are merged within days, not months.
- [ ] 🟡 VUL-014 **Someone hears about new advisories:** a named person watches the security announcements for the runtime, framework and CMS (mailing list, or GitHub **Watch → Custom → Security alerts**), and the team knows how fast it can ship a patch.
- [ ] 🟢 VUL-015 **CI fails on critical vulnerabilities:** an audit or `osv-scanner` step runs on every push and blocks critical findings.

## Audit tools by ecosystem

| Ecosystem (file that shows it) | Tool | Fallback if missing |
|---|---|---|
| JavaScript (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`) | `npm audit --omit=dev`, `pnpm audit --prod`, `yarn npm audit` | read the advisories page for each framework and key package |
| PHP (`composer.lock`) | `composer audit` | Packagist / FriendsOfPHP security advisories for each package |
| Python (`requirements.txt`, `poetry.lock`, `uv.lock`) | `pip-audit` | PyPI advisory database (GitHub Advisories) per package |
| Ruby (`Gemfile.lock`) | `bundle audit check --update` | rubysec advisories |
| Go (`go.mod`) | `govulncheck ./...` | pkg.go.dev/vuln |
| Rust (`Cargo.lock`) | `cargo audit` | rustsec.org |
| Java/Kotlin (`pom.xml`, `build.gradle`) | `osv-scanner` or OWASP Dependency-Check | GitHub Advisories per artifact |
| .NET (`*.csproj`) | `dotnet list package --vulnerable` | GitHub Advisories per package |
| Any lockfile | `osv-scanner scan source .` | the per-ecosystem tool above |
| Docker images | `trivy image`, `docker scout cves` | check the base image tag's support status on its official page |
| WordPress (`wp-content/plugins`) | `wp plugin list --update=available` (WP-CLI), WPScan if installed | each plugin's page and changelog |

Record every tool in the ledger's **Tools run** table, including "not installed" and which fallback you used.

## How to rank what you find
| Finding | Severity |
|---|---|
| On CISA's KEV list (known exploited) | 🔴 always |
| Critical or high CVE in code the app actually reaches, or in the runtime itself | 🔴 |
| Runtime, framework or CMS past end-of-life | 🔴 |
| High CVE in code that isn't reachable, or in dev-only tooling | 🟡 (say why it's not reachable) |
| End-of-life within 90 days, unmaintained plugin, version advertised in headers | 🟡 |
| Low or moderate CVE with no reachable path | 🟢 (list, don't block) |

For every 🔴, the ledger row and the report give: the component and exact version, the advisory ID (CVE/GHSA), the fixed version, the source URL opened during this run, and the workaround if one exists.
