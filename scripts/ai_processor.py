import time
import json
import re
from google import genai
from google.genai import errors

# Instantiate client once at module level for reuse
client = genai.Client(vertexai=False)

def _parse_retry_delay(error_str: str) -> int:
    """Extract retryDelay seconds from a 429 error string."""
    match = re.search(r"retryDelay.*?(\d+)s", error_str)
    return int(match.group(1)) + 2 if match else 60

def summarize_with_ai(title, content, tag, _retry=False):
    """
    Calls Gemini and returns a structured dict:
    {
        "title": "emoji + Chinese title",
        "tags": ["中文tag1", "tag2", "tag3"],
        "body": "full markdown body with Chinese summary + Polish learning section"
    }
    Uses 'gemini-3.1-flash-lite-preview' (Free Tier: 15 RPM).
    """
    prompt = f"""
You are a professional Chinese editor at a Warsaw newsroom who also teaches Polish to Chinese speakers at A2/B1 level. Focus area: {tag}.
Summarize the following Polish news into Chinese, and add a Polish language learning section.

Return ONLY a valid JSON object. No markdown fences, no preamble, no explanation.

{{
  "title": "A catchy Chinese title with a relevant emoji. MUST be under 20 Chinese characters. No subtitles, no colons.",
  "tags": ["Chinese tag 1", "Chinese tag 2", "Chinese tag 3"],
  "body": "Full markdown body using the exact format below"
}}

Body format (use this structure exactly):

### 🗞️ 中文摘要
[2-3 sentence summary in Chinese explaining what happened]

**关键信息：**
- **key point 1 in Chinese**
- **key point 2 in Chinese**
- **key point 3 in Chinese**

---

### 🇵🇱 波兰语学习 (3分钟速成)

**🎧 听力文本 (Polish Text for Listening)：**
[Write 2-3 simple Polish sentences at A2/B1 level summarizing the news. Keep it concise - this text will be converted to audio for listening practice.]

**💡 关键表达 (Key Expressions)：**
- **[Polish phrase]**: [Brief Chinese explanation of meaning and when/how to use it]
- **[Polish phrase]**: [Brief Chinese explanation]
- **[Polish phrase]**: [Brief Chinese explanation]
- **[Polish phrase]**: [Brief Chinese explanation]
- **[Polish phrase]**: [Brief Chinese explanation]

**语法小贴士：**
[One short tip in Chinese about an interesting Polish grammar point from this article, e.g. case endings, verb conjugation, useful phrase pattern. Keep it practical for A2/B1 learners.]

Source Title: {title}
Source Content: {content[:3500]}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        # Respect 15 RPM free tier limit
        time.sleep(10)

        raw = response.text or ""

        # Strip accidental markdown fences if model disobeys
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        return json.loads(clean)

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nRaw response: {raw[:300]}")
        raise

    except errors.ClientError as e:
        error_str = str(e)
        if "429" in error_str and not _retry:
            wait = _parse_retry_delay(error_str)
            print(f"Rate limit hit. Waiting {wait}s before one retry...")
            time.sleep(wait)
            return summarize_with_ai(title, content, tag, _retry=True)
        raise

    except Exception as e:
        print(f"Unexpected error in summarize_with_ai: {e}")
        raise
        
