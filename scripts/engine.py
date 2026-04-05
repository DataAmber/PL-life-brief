import os
import re
from datetime import datetime
from ai_processor import summarize_with_ai

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("Warning: gTTS not installed. Audio generation disabled. Install with: pip install gtts")

from fetchers import gis_fetcher, udsc_fetcher, rss_fetcher

# ---------------------------------------------------------------
# Register fetcher modules here. Each must implement:
#   fetch_list() -> list of dicts with keys:
#       title, url, slug, tag, category
#   fetch_content(url) -> str
# ---------------------------------------------------------------
SOURCES = [gis_fetcher, udsc_fetcher, rss_fetcher]

POSTS_DIR = "content/posts/"
AUDIO_DIR = "static/audio/"

def extract_polish_listening_text(markdown_body):
    """
    Extract Polish listening text from the markdown body.
    Looks for the section between "🎧 听力文本 (Polish Text for Listening)：" and the next section.
    """
    pattern = r"🎧 听力文本 \(Polish Text for Listening\)：\n(.*?)(?=\n\n\*\*|$)"
    match = re.search(pattern, markdown_body, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def generate_audio(polish_text, audio_path):
    """
    Generate Polish audio file using gTTS.
    Returns True if successful, False otherwise.
    """
    if not GTTS_AVAILABLE:
        return False
    
    try:
        # Create audio directory if it doesn't exist
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        
        # Generate Polish audio (lang='pl')
        tts = gTTS(polish_text, lang='pl', slow=False)
        tts.save(audio_path)
        print(f"Audio generated: {audio_path}")
        return True
    except Exception as e:
        print(f"Failed to generate audio: {e}")
        return False

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

    # Extract Polish listening text and generate audio
    polish_text = extract_polish_listening_text(body)
    audio_html = ""
    
    if polish_text:
        # Generate audio file with slug-based name
        slug = meta['slug']
        audio_filename = f"{slug}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        if generate_audio(polish_text, audio_path):
            # Add audio player to body (right after listening text)
            audio_html = f'\n\n<audio controls style="width: 100%; margin: 1rem 0;">\n  <source src="/audio/{audio_filename}" type="audio/mpeg">\n  Your browser does not support the audio element.\n</audio>\n'
            # Insert audio after the listening text section
            body = body.replace(
                f"🎧 听力文本 (Polish Text for Listening)：\n{polish_text}",
                f"🎧 听力文本 (Polish Text for Listening)：\n{polish_text}{audio_html}"
            )

    header = f"""---
title: "{meta['title']}"
date: {date_str}
categories: ["{meta['category']}"]
tags: ["{tags_str}"]
---

"""
    footer = f"""

---
> 📰 原文来源：[{meta['url']}]({meta['url']})
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + body + footer)
    print(f"Successfully deployed: {path}")
    if audio_html:
        print(f"  └─ with audio: {audio_path}")

if __name__ == "__main__":
    run_engine()
