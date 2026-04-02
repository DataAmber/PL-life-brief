import time
import json
from google import genai
from google.genai import errors

# Instantiate client once at module level for reuse
client = genai.Client(vertexai=False)

def summarize_with_ai(title, content, tag, _retry=False):
    """
    Calls Gemini and returns a structured dict:
    {
        "title": "emoji + Chinese title",
        "tags": ["中文tag1", "tag2", "tag3"],
        "body": "full markdown body"
    }
    Uses 'gemini-2.5-flash-lite' (Free Tier: 15 RPM, 1000 RPD).
    """
    prompt = f"""
You are a professional Chinese editor at a Warsaw newsroom. Focus area: {tag}.
Summarize the following Polish news into Chinese.

Return ONLY a valid JSON object. No markdown fences, no preamble, no explanation.

{{
  "title": "A catchy Chinese title with a relevant emoji at the start",
  "tags": ["Chinese tag 1", "Chinese tag 2", "Chinese tag 3"],
  "body": "Full markdown body in Chinese using the exact format below"
}}

Body format (use this structure exactly):
### 🚨 预警详情
[2-3 sentence summary in Chinese]

**具体信息：**
- **key point 1**
- **key point 2**
- **key point 3**

**波兰语地道词汇：**
- *Polish term 1* (Chinese meaning)
- *Polish term 2* (Chinese meaning)
- *Polish term 3* (Chinese meaning)

Source Title: {title}
Source Content: {content[:3500]}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        # Respect 15 RPM free tier limit
        time.sleep(1)

        raw = response.text or ""

        # Strip accidental markdown fences if model disobeys
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        return json.loads(clean)

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nRaw response: {raw[:300]}")
        raise

    except errors.ClientError as e:
        if "429" in str(e) and not _retry:
            print("Rate limit hit. Waiting 15 seconds before one retry...")
            time.sleep(15)
            return summarize_with_ai(title, content, tag, _retry=True)
        raise

    except Exception as e:
        print(f"Unexpected error in summarize_with_ai: {e}")
        raise
