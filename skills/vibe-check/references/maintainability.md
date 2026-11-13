# Maintainability and handover

Load this file for every Full and Enterprise check. AI-built apps often work but can't be maintained, handed to a developer, sold or shown to investors without a rewrite. These checks make sure someone other than the original builder (or their AI) can safely run and change the app. Most items are 🟡 or 🟢: they rarely block a launch, but they decide how expensive every future change is.

## Code health
- [ ] 🟡 **Type safety:** TypeScript `strict` mode (or the language's equivalent), with few `any`, `@ts-ignore` or `eslint-disable` escapes. Each escape has a reason.
- [ ] 🟡 **Linting and formatting run automatically** (ESLint/Biome/Ruff and Prettier, or similar), in CI and on commit.
- [ ] 🟡 **No dead or duplicated code:** unused files, components, routes and exports removed. No copy-pasted versions of the same logic from different AI sessions (see blind spot 16).
- [ ] 🟡 **No giant files or functions:** files over ~500 lines or functions over ~80 lines doing many things are listed for future splitting (list them; don't refactor during the audit).
- [ ] 🟡 **Configuration isn't hard-coded:** URLs, prices, limits, feature switches and email addresses live in config or env vars, not scattered through the code.
- [ ] 🟢 **Consistent structure and naming** that a new developer can guess (where routes, components, server code and tests live).

## Documentation
- [ ] 🔴 **README explains how to run it:** install, required env vars (with an `.env.example` listing every variable and what it's for, no real values), how to run locally, run tests, and deploy.
- [ ] 🟡 **Architecture notes:** a short page or diagram showing the main parts (frontend, API, database, storage, third-party services) and how data flows.
- [ ] 🟡 **Project rules for AI tools** (`CLAUDE.md`, `AGENTS.md`, `.cursor/rules`): stack, conventions, "never do" rules, and how to test, so future AI sessions don't drift.
- [ ] 🟡 **Database schema is documented** through migrations and a short description of the main tables and relationships.
- [ ] 🟢 **Changelog or release notes** for user-visible changes.

## Ownership and handover
- [ ] 🔴 **The business owns every account:** domain, hosting, database, code repository, app store accounts, payment provider, email provider and AI providers are owned by the company (or the client, for agency work), not a freelancer's or employee's personal login. → ask the user.
- [ ] 🔴 **Credentials are in a password manager or vault** that more than one trusted person can access. No credentials only in someone's head or chat history.
- [ ] 🟡 **Licences and third-party terms are listed** for code, assets, fonts, APIs and AI models (see `legal-privacy.md`), so a buyer or investor can check them.
- [ ] 🟡 **Known issues and tech debt are written down,** including shortcuts taken during the build and the latest vibe-check report.
- [ ] 🟢 **Due-diligence pack ready:** architecture notes, security summary, the latest vibe-check report, dependency and licence list, data map, and the policies in `policies.md`.
