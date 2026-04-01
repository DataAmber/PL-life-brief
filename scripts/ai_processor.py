import os
from google import genai

def summarize_with_ai(title, content, tag):
    # Retrieve the key from the environment injected by GitHub
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("Environment variable GEMINI_API_KEY is not set.")

    # Initialize the client specifically for the Generative AI (non-Vertex) endpoint
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1beta'})
    
    prompt = f"""
    Context: Professional Chinese newsroom in Poland. Topic: {tag}.
    Task: Summarize this Polish news into Chinese.
    
    Structure:
    - Chinese Title with emoji
    - 3 Bullet points in Chinese
    - 3 Polish-Chinese vocabulary pairs
    
    News Title: {title}
    News Content: {content[:3500]}
    """
    
    try:
        # Standard model string for the Flash model
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        # We print the error but NOT the API key
        print(f"Error during AI processing: {type(e).__name__}")
        raise e
        
