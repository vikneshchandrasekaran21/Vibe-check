# vibe-check ✅

**The pre-launch audit for AI-built apps.** Before you ship, have your AI coding agent check the parts it usually misses.

AI tools are great at writing code that works in the demo. They often miss what only shows up with real users, real attackers and real money: auth checks that only test whether someone is logged in, database rules left open, secrets in the browser, payments trusted from a redirect, no rate limits on the LLM endpoint, a privacy policy that doesn't match the app.

`vibe-check` is an open [Agent Skill](https://agentskills.io) that turns your coding agent into a strict pre-launch reviewer. It checks **250+ checks** across security, data, reliability, cost, AI features, legal and privacy, and UX. It cites evidence for every finding and ends with a plain-language report: **🟢 SHIP / 🟡 SHIP AFTER FIXES / 🔴 DO NOT SHIP**, plus a copy-paste fix prompt for each problem.

Works with **Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, Windsurf, Cline, Roo, Goose, OpenCode, Amp, Junie, Kiro** and other agents that read `SKILL.md`. For browser builders (**Lovable, Bolt, v0, Replit**), you paste one file into the chat.

---

## Install

### Option 1: one command (most agents)

```bash
npx skills add vikneshchandrasekaran21/vibe-check
```

The [skills CLI](https://github.com/vercel-labs/skills) detects which agents you have and installs the skill for them. Add `-g` to install for all your projects.

### Option 2: copy the folder

Copy [`skills/vibe-check/`](skills/vibe-check) into your agent's skills directory:

| Agent | Project folder | Global folder |
|---|---|---|
| Claude Code | `.claude/skills/vibe-check/` | `~/.claude/skills/vibe-check/` |
| OpenAI Codex | `.agents/skills/vibe-check/` | `~/.codex/skills/vibe-check/` |
| GitHub Copilot | `.github/skills/vibe-check/` | `~/.copilot/skills/vibe-check/` |
| Cursor | `.cursor/skills/vibe-check/` | `~/.cursor/skills/vibe-check/` |
| Gemini CLI | `.gemini/skills/vibe-check/` | `~/.gemini/skills/vibe-check/` |
| Other Agent Skills tools | see your tool's docs (often `.agents/skills/`) | |

### Option 3: tools that use rules or commands instead of skills

Ready-made files live in [`adapters/`](adapters). Copy the folder for your tool into your project root:

| Tool | Copy | Then run |
|---|---|---|
| Cursor (rules) | `adapters/cursor/.cursor/` | ask "run vibe-check" or `@vibe-check` |
| GitHub Copilot (prompt file) | `adapters/copilot/.github/` | `/vibe-check` in Copilot Chat |
| Windsurf | `adapters/windsurf/.windsurf/` | `/vibe-check` |
| Cline / Roo | `adapters/cline/.clinerules/` | `/vibe-check.md` |
| Gemini CLI (command) | `adapters/gemini/.gemini/` | `/vibe-check` |
| Any agent that reads `AGENTS.md` | add the snippet from [`adapters/AGENTS.md`](adapters/AGENTS.md) | "run vibe-check" |

### Option 4: Lovable, Bolt, v0, Replit, ChatGPT, Claude.ai (no file system)

Open [`dist/vibe-check.md`](dist/vibe-check.md), copy everything, paste it into the chat and add:

> Run this audit on my project. I'm not a developer, so explain each finding simply.

The skill switches to **static review mode** when it can't run commands, and tells you which commands to run yourself.

---

## Use

Ask your agent in plain words:

- "vibe check this app" → **Quick mode**: the AI blind spots plus every 🔴 launch blocker
- "run a full vibe-check before launch" → **Full mode**: everything
- "is this ready to ship?" / "what did the AI miss?" / "security audit"

The agent will:

1. **Map your project:** stack, data collected, entry points, database rules, env vars. It asks about your users and business where that affects legal checks.
2. **Check the 17 AI blind spots first:** the mistakes AI coding tools make most often.
3. **Run the area checklists** that apply to your stack.
4. **Write the report:** verdict, blockers with copy-paste fix prompts, questions for you, a "needs a lawyer" list, and what passed.
5. **Fix only what you approve**, using a built-in [fix playbook](skills/vibe-check/references/fixes.md): prove the bug, apply a proven pattern for your stack, add a test, and re-check. For things only you can do (rotating a leaked key, DNS, legal calls), it gives you exact steps.

It never changes code during the audit, never marks something as passed without evidence, and never prints your secrets in full.

**It won't change what you built.** Your design, features, flows and copy stay as they are. vibe-check fixes only the issues it found, with the smallest possible change. If a fix has to add something users will see (a cookie banner, a "Delete account" button), it asks first and builds it to match your existing design. Anything else it notices goes under "Other suggestions" instead of being changed.

## What it checks

| Area | Examples |
|---|---|
| 🧠 **AI blind spots** | Authorization (IDOR), RLS or Firebase rules, leaked secrets, mass assignment, client-side prices, missing timeouts, race conditions, invented packages, LLM spend caps, exposed admin and debug |
| 🔐 **Security & auth** | Sessions, cookies, JWTs, password reset, brute force, roles, multi-tenancy, injection (SQL, NoSQL, XSS, command), uploads, SSRF, CORS, CSRF, headers, hashing, dependencies |
| 🗄️ **Data & reliability** | Migrations, indexes, backups and restore tests, constraints, idempotency, webhooks, queues, cron, caching, pooling, CI/CD, staging, rollback, disaster recovery, cost alerts, logging, error tracking, uptime |
| 🤖 **AI features** | Keys on the server, per-user quotas, prompt injection, unsafe rendering of LLM output, agent tool permissions, RAG tenant isolation, provider data terms, moderation, AI disclosure |
| ⚖️ **Legal & privacy** | Privacy policy vs actual data, terms, cookie consent (no trackers before consent), deletion and export, OSS licenses (GPL/AGPL), asset licensing, refunds, PCI, tax, age limits, honest marketing, dark patterns. GDPR, CCPA, India DPDP, COPPA flagged for a lawyer |
| 📱 **UX & launch** | Accessibility (WCAG 2.2 AA), mobile, Core Web Vitals, 404/500 pages, SEO basics, email deliverability (SPF/DKIM/DMARC), signup and SMS abuse, mobile app store rules |
| 🛠️ **Fix playbook** | Tested patterns for IDOR, Supabase RLS, Firebase rules, leaked secrets, mass assignment, webhooks and idempotency, race conditions, rate limits, LLM spend caps, XSS, uploads, headers, consent, account deletion |
| 🧩 **Platform traps** | Supabase, Firebase, Vercel/Netlify, Next.js, Lovable/Bolt/v0/Replit, Stripe/Razorpay, Django/Rails/Express, Expo, Docker/VPS |

The full checklists are in [`skills/vibe-check/references/`](skills/vibe-check/references).

## Example verdict

```text
Verdict: 🔴 DO NOT SHIP
Any logged-in user can read every other user's invoices, and the Stripe secret key
is in the browser bundle. Fix these two before launch; the rest can follow.

Score: 96 / 121 checks passed · 🔴 2 blockers · 🟡 9 to fix before scale · ❓ 5 questions
```

## Important

- **This is not legal advice or a professional security audit.** It catches the common, costly mistakes. For payments at scale, health, finance or children's data, or enterprise customers, also get a lawyer and a professional pentest.
- An AI reviewer can miss things too. Treat 🟢 as "no known blockers", not a guarantee.

## Contributing

Found something AI tools keep getting wrong that isn't covered? PRs welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). Edit files in `skills/vibe-check/`, then run `python3 scripts/build.py` to regenerate `dist/` and `adapters/`.

## License

[MIT](LICENSE). Use it, fork it, ship safer.
