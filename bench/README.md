# Hunt benchmark

`hunt-app/` is a small, realistic Express app ("Pantry Pass") with **12 logic bugs that no vibe-check checklist line or sweep pattern names directly**: races, stacking coupons, negative totals, skipped payment states, an old endpoint missing an owner check, a self-chosen role, quota resets, referral farming, webhook retries, an open redirect that leaks a session token, and an unlimited AI bill. They're the kind of bug only **hunt mode** (attacking the app's own logic) finds. The answer key, `hunt-answers.json`, stays outside the app folder.

## Run it
1. Copy the app somewhere the agent can't see the answers:
   ```bash
   cp -R bench/hunt-app /tmp/pantry-pass && cd /tmp/pantry-pass && git init -q && git add -A && git commit -qm init
   ```
2. Open `/tmp/pantry-pass` in your AI tool (with vibe-check installed) and say **"vibe check this app"** (a Full check).
3. Score the ledger it wrote:
   ```bash
   python3 bench/score.py /tmp/pantry-pass/.vibe-check/ledger.md
   ```

Record the result in the table below with the vibe-check version, tool and model, so changes to hunt mode can be measured. Don't tune the skill to these exact bugs: add new cases instead.

| Date | vibe-check | Tool and model | Found |
|---|---|---|---|
| | | | |
