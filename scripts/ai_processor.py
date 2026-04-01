import os
from google import genai
from google.genai import types

def summarize_with_ai(title, content, tag):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    # Explicitly initialize the client for the Gemini 1.5 Flash model
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Context: Professional Chinese newsroom in Poland. Focus: {tag}.
    Task: Summarize this Polish news into Chinese for local residents.
    
    Requirements:
    1. Title: Catchy Chinese title with one relevant emoji.
    2. Summary: 3 clear bullet points in Chinese.
    3. Vocabulary: 3 key Polish terms from the text with Chinese meanings.
    
    Content to process:
    Title: {title}
    Text: {content[:4000]}
    """
    
    try:
        # Use the most stable call for the Flash model
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return f"Summary generation failed for: {title}"
