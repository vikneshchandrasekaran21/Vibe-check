# Updating vibe-check, per tool

Use this when Step 0 finds a newer version, or the update check couldn't connect. Give the user the one step for their tool.

| Where vibe-check runs | Update step |
|---|---|
| Installed with `npx skills add` (Claude Code, Codex, Cursor, Gemini CLI, Replit…) | `npx skills update` (in Replit, in the Shell) |
| Claude app | Download `vibe-check.zip` from https://github.com/vikneshchandrasekaran21/Vibe-check/releases/latest and upload it again |
| Lovable | Settings → Skills: import again from `https://github.com/vikneshchandrasekaran21/Vibe-check/tree/main/skills/vibe-check` |
| A copied rules or command file (Cursor, Copilot, Windsurf, Cline, Gemini CLI) | Copy the new file from the repo's `adapters/` folder, or switch to `npx skills add` |
| Pasted into a chat (Bolt, v0, ChatGPT) | Paste the new `dist/vibe-check.md` from the repo |
