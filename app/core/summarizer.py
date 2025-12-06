from app.core.chat import summarize_with_groq

def summarize_text(text: str, max_length: int = 150, min_length: int = 50) -> str:
    """
    Summarize text using Groq API (replacing the local BART model).
    Arguments max_length and min_length are kept for signature compatibility but might be ignored or handled by prompt if needed.
    """
    return summarize_with_groq(text)
