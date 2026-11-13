# AGENTS.md snippet

Many agents (Codex, Copilot, Cursor, Windsurf, Amp, Devin, Goose, Jules and others) read an `AGENTS.md` file at the root of your project. To make vibe-check available in any of them:

1. Copy [`dist/vibe-check.md`](../dist/vibe-check.md) into your project, at `docs/vibe-check.md`.
2. Paste this into your project's `AGENTS.md` (create the file if it doesn't exist):

```markdown
## Pre-launch audit (vibe-check)

Before any production deploy or launch, or whenever I ask to "vibe check", "audit the app",
or "check if this is ready to ship", read `docs/vibe-check.md` and follow it exactly:
audit first without changing code, cite evidence for every finding, mask secrets,
and produce the report it describes. Fix only the issues I approve.
```
