# Contributing to vibe-check

Thanks for helping make AI-built apps safer.

## What makes a good addition

- **A real, recurring mistake** that AI coding tools make, or that vibe-coded apps commonly ship with. Link an example, a CVE or an article if you can.
- **Checkable.** Say *how* an agent can verify it (a grep pattern, a command, a config value, a file to read). A vague "make sure it's secure" won't help an agent.
- **Prioritized.** 🔴 means it can leak data, lose money, lock users out or break the law. 🟡 means it hurts at scale. 🟢 is good practice.
- **Short.** One line per item, bolded name first.

## How to change things

1. Edit only the source files:
   - `skills/vibe-check/SKILL.md`: workflow, ground rules, AI blind spots
   - `skills/vibe-check/references/*.md`: area checklists
2. Regenerate the single-file version and adapters:
   ```bash
   python3 scripts/build.py
   ```
3. Commit the source *and* the generated files. CI fails if they're out of sync.

Don't edit `dist/` or `adapters/*/` by hand.

## Adding a new tool adapter

Add an output in `scripts/build.py` → `outputs()`, plus a row in the README install table. Include a link to the tool's docs in the PR.

## Testing a change

Run the skill on a small app with a known bug (for example, a Supabase table with RLS off, or an API route missing an ownership check). Confirm the agent finds it, cites evidence and suggests a correct fix.
