# Updating vibe-check, per tool

Use this when Step 0 finds a newer version, or the update check couldn't connect.

## When a newer version is out: the update is required

vibe-check only runs on its latest version, so every update is required. **Don't start the audit.** Ask, as a choice (question tool if you have one):

```text
⬆️ vibe-check v3.7.0 is out (you're on v3.6.4). vibe-check only runs on the latest version.
○ Update now (Recommended): I run `npx skills update -g`, then you start a new session
○ Show me how to update
```

- **Unattended or scheduled runs:** don't audit and don't install. Write the notice and the update step to `.vibe-check/summary.md` and stop.
- **Couldn't connect, or the user turned the check off:** the requirement can't be checked; carry on and say so in the report header.

## If the user picks "Update now"

- **`HOW: npx skills update -g`** (or `-p`) and you can run commands: run exactly that command (nothing else, never with `sudo`). Without `-g` or `-p` the update asks which scope to update and can pick the wrong one, so always pass the scope `HOW:` gives.
- **It worked:** run `version_check.py` again to confirm the new version is installed, then say: *"Updated to vX. This chat still has vY loaded: start a new session and say 'vibe check this app'."* Stop there.
- **It failed:** show the error in one line, give the manual step from the table below, and ask: *Try again* · *Show me how to update*. Don't audit on the old version.
- **`HOW: manual`**, or you can't run commands: give the one step for their tool from the table below, and stop.
- Never install anything without the user's pick, and never claim the new version is running in this chat: a session keeps the version it started with.

## If the user picks "Show me how to update"

Give the one step for their tool from the table below, then *"start a new session and say 'vibe check this app'"*, and stop.

## The update step for each tool


| Where vibe-check runs | Update step |
|---|---|
| Installed with `npx skills add -g` (Claude Code, Codex, Cursor, Gemini CLI…) | `npx skills update -g` |
| Installed into a project (Replit, or `npx skills add` without `-g`) | `npx skills update -p`, run in the project folder (in Replit, in the Shell) |
| Claude app | Download `vibe-check.zip` from https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest and upload it again |
| Lovable | Settings → Skills: import again from `https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check` |
| A copied rules or command file (Cursor, Copilot, Windsurf, Cline, Gemini CLI) | Copy the new file from the repo's `adapters/` folder, or switch to `npx skills add` |
| Pasted into a chat (Bolt, v0, ChatGPT) | Paste the new `dist/vibe-check.md` from the repo |
