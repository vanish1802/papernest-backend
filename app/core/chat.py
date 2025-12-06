import os
from groq import Groq

# Initialize Groq client
# Ensure GROQ_API_KEY is set in environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def chat_with_paper(paper_text: str, user_query: str) -> str:
    """
    Chat with a paper using Groq API.
    """
    if not paper_text:
        return "Error: No paper content available to chat with."

    system_prompt = f"""You are a helpful research assistant. 
    You have read the following research paper:
    
    {paper_text[:25000]}  # Truncate to avoid token limits equivalent
    
    Answer the user's questions based ONLY on the paper content provided above.
    If the answer is not in the paper, say so.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_query,
                }
            ],
            model="llama-3.3-70b-versatile",  # Updated to supported model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error interacting with Groq API: {str(e)}"

def summarize_with_groq(text: str) -> str:
    """
    Summarize text using Groq API.
    """
    if not text:
        return "Error: No text to summarize."
        
    prompt = f"""Summarize the following research paper text into a concise and informative summary:
    
    {text[:25000]}
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error interacting with Groq API: {str(e)}"
