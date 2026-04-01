import os
from google import genai

def summarize_with_ai(title, content, tag):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    # According to the latest docs, explicitly disabling vertexai 
    # forces the client to use the API Key for authentication.
    client = genai.Client(
        api_key=api_key,
        vertexai=False
    )

    prompt = f"""
    Context: Professional Chinese newsroom in Poland. Focus: {tag}.
    Task: Summarize this Polish news into Chinese for local residents.
    
    Structure:
    - Chinese Title with emoji
    - 3 Bullet points in Chinese
    - 3 Polish-Chinese vocabulary pairs
    
    Source Title: {title}
    Source Content: {content[:3500]}
    """

    try:
        # Use the simple model string; the SDK handles the rest.
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        # The response object in google-genai returns a 'text' attribute
        return response.text
        
    except Exception as e:
        print(f"GenAI Client Error: {e}")
        raise e
        
