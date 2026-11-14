# Security policy

vibe-check runs inside people's AI coding tools with access to their code, so problems in it matter. Thank you for reporting them privately.

## How to report
Use GitHub's private reporting: **Security → Report a vulnerability** on this repository. Please don't open a public issue for security problems.

Include what you found, how to reproduce it, and which version (`version:` in `skills/vibe-check/SKILL.md`).

## What's in scope
- **The helper scripts** (`skills/vibe-check/scripts/`): anything that reads outside the project, writes outside `.vibe-check/`, runs commands other than read-only git, sends data anywhere other than the documented GitHub reads and the opt-in stats, or leaks secrets into reports.
- **The instructions** (`SKILL.md`, `references/`): ways a project's own files could steer the audit (prompt injection), make it skip checks, pass something it shouldn't, or change code without approval.
- **The release process** (`scripts/release.sh`, the GitHub release zip): anything that could ship a tampered or stale copy.

Out of scope: findings vibe-check reports about *your* app (those are the tool working), and general limits of AI tools.

## What to expect
We aim to acknowledge reports within 3 days and to fix serious issues in a patch release, credited to you if you'd like. Everyone running vibe-check v2.7.1 or later is told about new releases by the built-in version check.
