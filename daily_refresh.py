#!/usr/bin/env python3
"""
每日自动刷新所有博主信息（cron调用）
用法: python3 daily_refresh.py

设置cron: crontab -e
添加: 0 9 * * * cd /Users/lafae/projects/thai-kol-finder && python3 daily_refresh.py >> output/refresh.log 2>&1
"""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_FILE = BASE_DIR / "data" / "kol_db.json"


def curl_fetch(url):
    try:
        result = subprocess.run(
            ["curl", "-sL", "-m", "15",
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
             url],
            capture_output=True, text=True, timeout=20,
        )
        return result.stdout
    except:
        return ""


def scrape_meta(url):
    from bs4 import BeautifulSoup
    html = curl_fetch(url)
    if not html:
        return {}
    soup = BeautifulSoup(html, "html.parser")
    meta = {}
    meta["title"] = soup.title.string if soup.title else ""
    for tag in soup.find_all("meta"):
        prop = tag.get("property", "") or tag.get("name", "")
        content = tag.get("content", "")
        if prop in ("og:description", "description") and content:
            meta["description"] = content
        if prop == "og:image" and content:
            meta["image"] = content
        if prop == "og:title" and content:
            meta["og_title"] = content
    return meta


def run():
    print(f"\n[{datetime.now().isoformat()}] 开始每日刷新...")

    if not DB_FILE.exists():
        print("数据库不存在，跳过")
        return

    db = json.loads(DB_FILE.read_text(encoding="utf-8"))
    updated = 0

    for key, profile in db["profiles"].items():
        url = profile.get("url", "")
        if not url:
            continue

        meta = scrape_meta(url)
        if meta:
            if meta.get("description"):
                profile["scraped_bio"] = meta["description"]
            if meta.get("image"):
                profile["avatar_url"] = meta["image"]
            if meta.get("og_title"):
                profile["scraped_name"] = meta["og_title"]
            bio = meta.get("description", "")
            email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.]+', bio)
            if email_match and not profile.get("contact_email"):
                profile["contact_email"] = email_match.group(0)
            profile["last_scraped"] = datetime.now().isoformat()
            updated += 1

        import time
        time.sleep(1)

    db["last_run"] = datetime.now().isoformat()
    DB_FILE.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"刷新完成: {updated}/{len(db['profiles'])} 个博主已更新")


if __name__ == "__main__":
    run()
