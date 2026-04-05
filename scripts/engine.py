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
    # Try new format first
    pattern = r"🎧 听力文本 \(Polish Text for Listening\)：\n(.*?)(?=\n\n\*\*|<audio|$)"
    match = re.search(pattern, markdown_body, re.DOTALL)
    
    if match:
        text = match.group(1).strip()
        if text:
            return text
    
    return None

def generate_audio(polish_text, audio_path):
    """
    Generate Polish audio file using gTTS.
    Returns True if successful, False otherwise.
    """
    if not GTTS_AVAILABLE:
        print(f"  ⚠ Audio skipped: gTTS not available")
        return False
    
    if not polish_text or len(polish_text.strip()) == 0:
        print(f"  ⚠ Audio skipped: empty Polish text")
        return False
    
    try:
        # Create audio directory if it doesn't exist
        audio_dir = os.path.dirname(audio_path)
        if audio_dir:
            os.makedirs(audio_dir, exist_ok=True)
            print(f"  📂 Audio dir ensured: {audio_dir}")
        
        # Generate Polish audio (lang='pl')
        print(f"  🎙 Generating audio from: '{polish_text[:50]}...'")
        tts = gTTS(polish_text, lang='pl', slow=False)
        tts.save(audio_path)
        
        if os.path.exists(audio_path):
            size = os.path.getsize(audio_path)
            print(f"  ✓ Audio generated: {audio_path} ({size} bytes)")
            return True
        else:
            print(f"  ✗ Audio file not created at {audio_path}")
            return False
            
    except Exception as e:
        print(f"  ✗ Audio generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_engine():
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)
    
    # Ensure audio directory exists
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        print(f"📂 Created audio directory: {AUDIO_DIR}")

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
    print(f"📝 Processing: {meta['slug']}")
    polish_text = extract_polish_listening_text(body)
    audio_html = ""
    
    if polish_text:
        # Generate audio file with slug-based name
        slug = meta['slug']
        audio_filename = f"{slug}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        if generate_audio(polish_text, audio_path):
            # Add audio player to body (right after listening text)
            audio_html = f'\n\n<audio controls style="width: 100%; margin: 1rem 0; display: block;">\n  <source src="/audio/{audio_filename}" type="audio/mpeg">\n  Your browser does not support the audio element.\n</audio>\n'
            # Insert audio after the listening text section
            text_section = f"🎧 听力文本 (Polish Text for Listening)：\n{polish_text}"
            if text_section in body:
                body = body.replace(text_section, f"{text_section}{audio_html}")
                print(f"  ✓ Audio player embedded")
            else:
                print(f"  ⚠ Could not find listening text section to embed audio")
    else:
        print(f"  ⚠ No Polish listening text found in post")

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
    print(f"  ✓ Post saved: {path}")

if __name__ == "__main__":
    run_engine()
