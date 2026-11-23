"""Sin & Sonnet poster: posts approved items from queue.json to Instagram (@sinandsonnet)
and the Sin & Sonnet Facebook Page.

Modes (first argument):
  check  - confirm the key works and find the Page + Instagram account; posts nothing
  post   - post every approved item scheduled for today or earlier (only at posting time)
  force  - post the next approved item right now, whatever its date (used for tests)

Each item in queue.json:
  {
    "id": "2026-11-24-feed",              unique name
    "kind": "feed" | "story" | "reel",
    "post_on": "2026-11-24",              the day it goes up (Eastern)
    "approved": true,                     nothing posts unless she approved it
    "platforms": ["instagram", "facebook"],
    "media": ["media/file.png", ...],     files in this repo (or full https links); up to 10 for a carousel
    "caption": "...",
    "ai_generated": false                 true if it shows realistic AI-made people
  }

Needs the META_TOKEN secret (Sin & Sonnet system-user key). Uses only the Python standard library.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

VERSION = "v23.0"
GRAPH = f"https://graph.facebook.com/{VERSION}"
QUEUE_FILE = "queue.json"
LOG_FILE = "posted-log.md"
EASTERN = ZoneInfo("America/New_York")
POST_HOURS = (19, 20)  # ~7:15pm Eastern; the 8pm wake-up retries if the first one failed
IG_USERNAME = "sinandsonnet"
REPO = os.environ.get("GITHUB_REPOSITORY", "bocabeatrice/sinandsonnet-poster")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")

PAGE_ID = PAGE_TOKEN = IG_ID = None


class ApiError(SystemExit):
    pass


class MediaError(SystemExit):
    pass


def api(method, path, token=None, **params):
    for attempt in range(4):
        try:
            return _api(method, path, token, **params)
        except ApiError as e:
            msg = str(e)
            transient = '"is_transient":true' in msg or "said no (5" in msg
            if not transient or attempt == 3 or path.endswith("media_publish"):
                raise
            print(f"Meta hiccup, trying again in {20 * (attempt + 1)}s...")
            time.sleep(20 * (attempt + 1))


def _api(method, path, token, **params):
    params["access_token"] = (token or os.environ["META_TOKEN"]).strip()
    data = urllib.parse.urlencode(params).encode()
    url = f"{GRAPH}/{path}"
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise ApiError(f"Meta said no ({e.code}) on {path}: {body}")


def find_accounts():
    """Find the Sin & Sonnet Page, its posting key, and the linked Instagram account."""
    global PAGE_ID, PAGE_TOKEN, IG_ID
    pages = api("GET", "me/accounts",
                fields="id,name,access_token,instagram_business_account{id,username}")
    data = pages.get("data", [])
    if not data:
        raise SystemExit("The key works but can't see any Facebook Page. "
                         "Check the system user has the Sin & Sonnet Page assigned.")
    chosen = None
    for p in data:
        ig = p.get("instagram_business_account") or {}
        if ig.get("username", "").lower() == IG_USERNAME:
            chosen = p
            break
    if not chosen:
        chosen = next((p for p in data if "sonnet" in p.get("name", "").lower()), data[0])
    PAGE_ID, PAGE_TOKEN = chosen["id"], chosen.get("access_token")
    ig = chosen.get("instagram_business_account") or {}
    IG_ID = ig.get("id")
    return chosen.get("name", ""), ig.get("username", "")


def media_url(path):
    if path.startswith("http"):
        return path
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{urllib.parse.quote(path)}"


def is_video(path):
    return path.lower().endswith((".mp4", ".mov"))


# ---------------- Instagram ----------------

def ig_wait(container_id, minutes=5):
    for _ in range(minutes * 12):
        status = api("GET", container_id, fields="status_code").get("status_code")
        if status == "FINISHED":
            return
        if status in ("ERROR", "EXPIRED"):
            raise MediaError(f"Instagram could not process the file (status {status}).")
        time.sleep(5)
    raise MediaError("Instagram took too long to process the file.")


def ig_find_existing(caption):
    if not caption.strip():
        return None
    recent = api("GET", f"{IG_ID}/media", fields="caption,permalink", limit="10")
    for m in recent.get("data", []):
        if (m.get("caption") or "").strip() == caption.strip():
            return m.get("permalink", "") or m["id"]
    return None


def ig_container(item):
    urls = [media_url(m) for m in item["media"]][:10]
    caption = item.get("caption", "")
    kind = item["kind"]
    if kind == "story":
        u = urls[0]
        key = "video_url" if is_video(u) else "image_url"
        return api("POST", f"{IG_ID}/media", media_type="STORIES", **{key: u})["id"]
    if kind == "reel":
        return api("POST", f"{IG_ID}/media", media_type="REELS", video_url=urls[0],
                   caption=caption, share_to_feed="true")["id"]
    if len(urls) == 1:
        return api("POST", f"{IG_ID}/media", image_url=urls[0], caption=caption)["id"]
    children = []
    for u in urls:
        params = {"is_carousel_item": "true"}
        if is_video(u):
            params.update(media_type="VIDEO", video_url=u)
        else:
            params["image_url"] = u
        child = api("POST", f"{IG_ID}/media", **params)["id"]
        ig_wait(child)
        children.append(child)
    return api("POST", f"{IG_ID}/media", media_type="CAROUSEL",
               children=",".join(children), caption=caption)["id"]


def post_instagram(item):
    if not IG_ID:
        raise SystemExit("No Instagram account is linked to the Page.")
    if item["kind"] != "story":
        found = ig_find_existing(item.get("caption", ""))
        if found:
            print("Already on Instagram, not posting twice.")
            return found
    container = ig_container(item)
    ig_wait(container, minutes=10 if item["kind"] == "reel" else 5)
    for attempt in range(4):
        try:
            media_id = api("POST", f"{IG_ID}/media_publish", creation_id=container)["id"]
            break
        except ApiError:
            time.sleep(30)
            if item["kind"] != "story":
                found = ig_find_existing(item.get("caption", ""))
                if found:
                    return found
            if attempt == 3:
                raise
    if item["kind"] == "story":
        return f"story {media_id}"
    return api("GET", media_id, fields="permalink").get("permalink", "") or media_id


# ---------------- Facebook Page ----------------

def post_facebook(item):
    tok = PAGE_TOKEN
    if not tok:
        raise SystemExit("Couldn't get a posting key for the Facebook Page.")
    urls = [media_url(m) for m in item["media"]]
    caption = item.get("caption", "")
    kind = item["kind"]
    if kind == "story":
        if is_video(urls[0]):
            return "skipped (video stories go to Instagram only)"
        photo = api("POST", f"{PAGE_ID}/photos", tok, url=urls[0], published="false")["id"]
        res = api("POST", f"{PAGE_ID}/photo_stories", tok, photo_id=photo)
        return f"story {res.get('post_id', '')}"
    if kind == "reel" or (len(urls) == 1 and is_video(urls[0])):
        res = api("POST", f"{PAGE_ID}/videos", tok, file_url=urls[0], description=caption)
        return f"https://www.facebook.com/{res['id']}"
    if len(urls) == 1:
        res = api("POST", f"{PAGE_ID}/photos", tok, url=urls[0], message=caption)
        return f"https://www.facebook.com/{res.get('post_id', res['id'])}"
    attached = []
    for u in urls[:10]:
        if is_video(u):
            continue
        pid = api("POST", f"{PAGE_ID}/photos", tok, url=u, published="false")["id"]
        attached.append(json.dumps({"media_fbid": pid}))
    params = {"message": caption}
    for i, a in enumerate(attached):
        params[f"attached_media[{i}]"] = a
    res = api("POST", f"{PAGE_ID}/feed", tok, **params)
    return f"https://www.facebook.com/{res['id']}"


# ---------------- main ----------------

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "post"
    now = datetime.now(EASTERN)

    if mode == "check":
        page, ig = find_accounts()
        print(f"Key works. Facebook Page: {page} (ID {PAGE_ID}).")
        print(f"Instagram: @{ig} (ID {IG_ID})." if IG_ID else "Instagram: NOT linked to this Page.")
        print("Page posting key: found." if PAGE_TOKEN else "Page posting key: MISSING.")
        if IG_ID:
            n = len(api("GET", f"{IG_ID}/media", fields="id", limit="25").get("data", []))
            print(f"Instagram posts visible to the robot: {n}.")
        print("Nothing was posted.")
        return

    with open(QUEUE_FILE) as f:
        queue = json.load(f)
    items = queue["items"]
    today = now.date().isoformat()

    if mode == "post" and now.hour not in POST_HOURS:
        print(f"It's {now:%H:%M} Eastern, not posting time. Nothing to do.")
        return

    def pending(i):
        done = i.get("results", {})
        return i.get("approved") and any(p not in done for p in i.get("platforms", []))

    if mode == "force":
        due = [i for i in items if pending(i)][:1]
    else:
        due = [i for i in items if pending(i) and i.get("post_on", "9999") <= today]
    if not due:
        print("Nothing approved is due. Ask Claude for the next line-up.")
        return

    find_accounts()
    problems = []
    for item in due:
        results = item.setdefault("results", {})
        for platform in item.get("platforms", []):
            if platform in results:
                continue
            print(f"Posting {item['id']} ({item['kind']}) to {platform}...")
            try:
                link = post_instagram(item) if platform == "instagram" else post_facebook(item)
            except SystemExit as e:
                problems.append(f"{item['id']} → {platform}: {e.code}")
                print(f"::warning::{item['id']} → {platform} failed: {str(e.code)[:500]}")
                continue
            results[platform] = link
            with open(LOG_FILE, "a") as f:
                f.write(f"| {now:%Y-%m-%d %I:%M %p} | {item['id']} | {item['kind']} | {platform} | {link} |\n")
            print(f"Posted! {link}")
        if all(p in results for p in item.get("platforms", [])):
            item["posted_at"] = now.isoformat(timespec="minutes")

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if problems:
        raise SystemExit("Some posts didn't go up (they'll be retried next run):\n" + "\n".join(problems))


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            print("::error::" + str(e.code).replace("%", "%25").replace("\n", "%0A"))
        raise
