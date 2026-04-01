import os
import google.generativeai as genai

def summarize_news(raw_title, raw_text, domain_context):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Precise prompt to ensure high-quality Chinese output with Polish annotations
    prompt = f"""
    Context: Professional Chinese newsroom in Poland ({domain_context}).
    Task: Summarize the following Polish news into Chinese for local residents.
    
    Format:
    - Title: Catchy Chinese title with one relevant emoji.
    - Summary: 3 concise bullet points in Chinese.
    - Vocabulary: 3 key Polish terms from the text with Chinese translations.
    
    Source Title: {raw_title}
    Source Content: {raw_text[:2000]}
    """
    
    response = model.generate_content(prompt)
    return response.text

