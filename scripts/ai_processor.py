import os
from google import genai

def summarize_with_ai(title, content, tag):
    # Initialize the new Client
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    
    prompt = f"""
    Context: Professional Chinese newsroom in Poland. Focus: {tag}.
    Task: Summarize this Polish news into Chinese for local residents.
    
    Requirements:
    1. Title: Catchy Chinese title with one relevant emoji.
    2. Summary: 3 clear bullet points in Chinese.
    3. Vocabulary: 3 key Polish terms from the text with Chinese meanings.
    
    Content to process:
    Title: {title}
    Text: {content[:3000]}
    """
    
    # New method call: models.generate_content
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    
    return response.text
    
