import os
from groq import Groq

# Initialize Groq client
# Ensure GROQ_API_KEY is set in environment variables
# Helper to lazy-load Groq client
def get_groq_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    return Groq(api_key=api_key)

from app.core.rag_utils import retrieve_context

def chat_with_paper(paper_text: str, user_query: str) -> str:
    """
    Chat with a paper using RAG and Groq API.
    """
    if not paper_text:
        return "Error: No paper content available to chat with."

    # Retrieve relevant context using RAG
    # We use a generous window (e.g., top 5 chunks) to give LLM enough info
    context = retrieve_context(paper_text, user_query, top_k=5)
    
    if not context:
        context = "No specific relevant context found in the paper. Answer based on general knowledge if possible, or state that the paper doesn't cover this."

    system_prompt = f"""You are a helpful research assistant. 
    You have read a research paper. Here are the most relevant sections to the user's query:
    
    ---CONTEXT START---
    {context}
    ---CONTEXT END---
    
    Answer the user's questions based ONLY on the context provided above.
    If the answer is not in the context, say so.
    """

    try:
        client = get_groq_client()
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
            model="llama-3.3-70b-versatile",
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
        client = get_groq_client()
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
