import os
import google.generativeai as genai

def summarize_with_ai(title, content, tag): # Ensure this name is exactly this
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
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
    
    response = model.generate_content(prompt)
    return response.text
    
