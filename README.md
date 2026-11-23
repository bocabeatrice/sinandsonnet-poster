# Sin & Sonnet Poster

Posts approved Sin & Sonnet content to **Instagram (@sinandsonnet)** — feed, carousels, Reels and stories — and the **Sin & Sonnet Facebook Page**, around **7:15pm Eastern**. Runs on GitHub's computers, so no computer needs to be on.

- **queue.json** — the line-up. Claude adds items; only items marked `"approved": true` ever post, on their `post_on` date.
- **media/** — the pictures and videos (this repo is public so Instagram can download them; the key stays secret).
- **posted-log.md** — what was posted, where and when, with links.
- **post.py** — the posting program. Never posts the same thing twice.
- **.github/workflows/daily-post.yml** — the daily schedule.

The Meta key is stored as the `META_TOKEN` secret (Settings → Secrets and variables → Actions). It never expires. Never paste it anywhere else.

To test by hand: **Actions** tab → **Sin & Sonnet daily post** → **Run workflow** → choose `check` (tests the key, posts nothing) or `force` (posts the next approved item now).

TikTok can't be auto-posted this way; Claude prepares TikTok versions for posting by hand.
