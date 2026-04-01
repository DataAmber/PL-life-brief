import os
from google import genai

def summarize_with_ai(title, content, tag):
    """
    The SDK automatically authenticates using the GOOGLE_API_KEY 
    environment variable provided by the GitHub Action.
    """
    try:
        # No arguments needed if GOOGLE_API_KEY is set in the environment
        client = genai.Client(vertexai=False)
        
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
        
