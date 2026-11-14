# Updating vibe-check, per tool

Use this when Step 0 finds a newer version, or the update check couldn't connect.

## When a newer version is out: ask, as a choice

```text
⬆️ vibe-check v3.7.0 is out (you're on v3.6.3).
○ Update now (Recommended): I run `npx skills update`, then you start a new session
○ Continue this check on v3.6.3 and update later
```

Use the question tool if you have one (see *Asking the user* in SKILL.md). Don't ask in unattended or scheduled runs, or when `version_check.py` printed `ASK: no`: then give the one-line notice and carry on.

## If the user picks "Update now"

- **`HOW: npx skills update`** and you can run commands: run exactly `npx skills update` (nothing else, never with `sudo`). If it succeeds, say: *"Updated to vX. This chat still has vY loaded; start a new session and say 'vibe check this app' to use vX."* Then ask, as a choice: *Start a new session now (Recommended)* · *Finish this check on vY first*. If it fails, show the error in one line and give the manual step from the table below.
- **`HOW: manual`**, or you can't run commands: give the one step for their tool from the table below, then the same choice.
- Never update in the middle of a check without the user's pick, and never claim the new version is running in this chat: a session keeps the version it started with.

## If the user picks "Continue"

Add `update_declined: <new version>` to `.vibe-check/config` (create it if needed; `.vibe-check/` is gitignored) so they aren't asked again for that version, carry on, and keep the notice at the top of the report. A newer release after that is asked about again.

## The update step for each tool


| Where vibe-check runs | Update step |
|---|---|
| Installed with `npx skills add` (Claude Code, Codex, Cursor, Gemini CLI, Replit…) | `npx skills update` (in Replit, in the Shell) |
| Claude app | Download `vibe-check.zip` from https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest and upload it again |
| Lovable | Settings → Skills: import again from `https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check` |
| A copied rules or command file (Cursor, Copilot, Windsurf, Cline, Gemini CLI) | Copy the new file from the repo's `adapters/` folder, or switch to `npx skills add` |
| Pasted into a chat (Bolt, v0, ChatGPT) | Paste the new `dist/vibe-check.md` from the repo |
