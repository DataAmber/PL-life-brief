import os
from google import genai

def summarize_with_ai(title, content, tag):
    """
    Explicitly using the stable 'v1' API version to avoid the 404 beta error.
    The SDK pulls GOOGLE_API_KEY from the environment.
    """
    try:
        # Force the stable 'v1' version via http_options
        client = genai.Client(
            vertexai=False,
            http_options={'api_version': 'v1'}
        )
        
        prompt = f"""
        Context: Professional Chinese newsroom in Poland. Focus: {tag}.
        Task: Summarize this Polish news into Chinese for local residents.
        
        Format:
        1. Catchy Chinese Title with emoji
        2. 3 Bullet points in Chinese
        3. 3 Polish-Chinese vocabulary pairs
        
        Source Title: {title}
        Source Content: {content[:3500]}
        """

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        return response.text if response.text else "AI summary empty."

    except Exception as e:
        print(f"GenAI SDK Error: {e}")
        raise e
        
