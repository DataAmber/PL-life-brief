import os
from datetime import datetime
from ai_processor import summarize_with_ai
from fetchers import gis_fetcher, udsc_fetcher, rss_fetcher

# ---------------------------------------------------------------
# Register fetcher modules here. Each must implement:
#   fetch_list() -> list of dicts with keys:
#       title, url, slug, tag, category
#   fetch_content(url) -> str
# ---------------------------------------------------------------
SOURCES = [gis_fetcher, udsc_fetcher, rss_fetcher]

POSTS_DIR = "content/posts/"

def run_engine():
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    for module in SOURCES:
        print(f"--- Checking Source: {module.__name__} ---")
        items = module.fetch_list()

        for item in items:
            file_path = os.path.join(POSTS_DIR, f"{item['slug']}.md")

            # IDEMPOTENCY CHECK: Skip if already processed
            if os.path.exists(file_path):
                print(f"Skipping: {item['slug']} (already exists)")
                continue

            print(f"New content found: {item['title']}")

            try:
                raw_text = module.fetch_content(item['url'])

                # Returns a structured dict, not raw text
                summary = summarize_with_ai(item['title'], raw_text, item['tag'])

                # Merge AI-generated fields into item
                item['title'] = summary['title']
                item['tags'] = summary['tags']
                item['category'] = summary['category']   # ← add this line

                save_post(file_path, summary['body'], item)

            except Exception as e:
                print(f"Failed on {item['slug']}: {e} — skipping.")
                continue

def save_post(path, body, meta):
    # Build Chinese tags list, always append "Automated" in English for filtering
    tags = meta.get('tags', []) + ['Automated']
    tags_str = '", "'.join(tags)

    # Timezone-aware ISO 8601 timestamp (Warsaw time via system timezone in CI)
    date_str = datetime.now().astimezone().isoformat()

    header = f"""---
title: "{meta['title']}"
date: {date_str}
categories: ["{meta['category']}"]
tags: ["{tags_str}"]
---

> Original Source: [{meta['url']}]({meta['url']})

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + body)
    print(f"Successfully deployed: {path}")

if __name__ == "__main__":
    run_engine()
