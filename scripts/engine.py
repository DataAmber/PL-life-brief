import os
from datetime import datetime
from ai_processor import summarize_with_ai
from fetchers import gis_fetcher

# Register your fetcher modules here
SOURCES = [gis_fetcher]
POSTS_DIR = "content/posts/"

def run_engine():
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    for module in SOURCES:
        print(f"--- Checking Source: {module.__name__} ---")
        items = module.fetch_list()
        
        for item in items:
            # File naming convention: slug.md
            file_path = os.path.join(POSTS_DIR, f"{item['slug']}.md")
            
            # IDEMPOTENCY CHECK: Skip if file already exists
            if os.path.exists(file_path):
                print(f"Skipping: {item['slug']} (Already exists)")
                continue
            
            print(f"New Content Found: {item['title']}")
            
            # Only fetch detail and call AI if it's a NEW post
            raw_text = module.fetch_content(item['url'])
            chinese_summary = summarize_with_ai(item['title'], raw_text, item['tag'])
            
            save_post(file_path, chinese_summary, item)

def save_post(path, content, meta):
    header = f"""---
title: "{meta['title']}"
date: {datetime.now().isoformat()}
categories: ["{meta['category']}"]
tags: ["{meta['tag']}", "Automated"]
---

> Original Source: [{meta['url']}]({meta['url']})

"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + content)
    print(f"Successfully deployed: {path}")

if __name__ == "__main__":
    run_engine()

