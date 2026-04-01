import os
import time
from google import genai
from google.genai import errors

def summarize_with_ai(title, content, tag):
    """
    Using 'gemini-2.5-flash-lite', which is the standard 2026 Free Tier model.
    It provides 15 RPM and 1,000 RPD, making it the most stable for news scraping.
    """
    try:
        client = genai.Client(vertexai=False)
        
        prompt = f"""
        Context: Professional Chinese newsroom in Warsaw. Focus: {tag}.
        Task: Summarize this Polish news into Chinese.
        
        Format:
        1. Catchy Chinese Title with emoji
        2. 3 Bullet points in Chinese
        3. 3 Polish-Chinese vocabulary pairs (B1 level)
        
        Source Title: {title}
        Source Content: {content[:3500]}
        """

        # This model is confirmed to be in your list as 'models/gemini-2.5-flash-lite'
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        
        # Essential 1-second delay to respect the 15 RPM (Requests Per Minute) limit
        time.sleep(1)
        
        return response.text if response.text else "AI summary empty."

    except errors.ClientError as e:
        if "429" in str(e):
            print("Rate limit hit. Waiting 15 seconds before one retry...")
            time.sleep(15)
            # Recursive retry for one final attempt
            return summarize_with_ai(title, content, tag)
        raise e
    except Exception as e:
        print(f"Unexpected Error: {e}")
        raise e
        
