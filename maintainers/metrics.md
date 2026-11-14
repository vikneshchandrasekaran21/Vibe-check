# How vibe-check is being used (without tracking anyone)

## Free signals you can check any time
```bash
R=vikneshchandrasekaran21/Vibe-check
gh api repos/$R --jq '{stars: .stargazers_count, forks: .forks_count, watchers: .subscribers_count}'
gh api repos/$R/traffic/views  --jq '{views_14d: .count, unique_visitors: .uniques}'
gh api repos/$R/traffic/clones --jq '{clones_14d: .count, unique_cloners: .uniques}'
gh api repos/$R/releases --jq '.[] | {release: .tag_name, zip_downloads: ([.assets[].download_count] | add)}'
gh api repos/$R/traffic/popular/referrers --jq '.[] | {from: .referrer, visits: .count}'
```
- **Installs:** the skills.sh page for the repo shows install counts for `npx skills add`.
- **Claude app users:** the release zip download count above.
- Traffic data only covers the last 14 days: copy it somewhere weekly if you want a history.

## Opt-in anonymous results (what vibe-check finds)
At the end of an audit, vibe-check offers once to share **anonymous counts** (`scripts/share_stats.py`): version, level, month, ecosystems and framework names, modules run, pass/fail counts, failed check IDs by severity, hunt counts, and sweep and version totals. No code, paths, names, URLs or evidence. The user sees exactly what would be sent first and must say yes.

To switch it on:
1. Create an HTTPS endpoint that accepts a JSON POST and stores it **without the sender's IP address**. For example, a Supabase Edge Function inserting into a `vibe_check_stats` table, with rate limiting.
2. Put its URL in `STATS_URL` in `skills/vibe-check/scripts/share_stats.py`.
3. Mention the endpoint and what's kept in the README's privacy section, then release.

Useful questions the data answers: the most common failed checks, the share of apps with at least one 🔴, what hunt mode finds that the checklists don't, and how results differ by stack.
