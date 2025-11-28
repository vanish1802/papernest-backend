from transformers import pipeline
from typing import Optional

# Initialize model once (singleton pattern for performance)
_summarizer = None

def get_summarizer():
    """Lazy load the summarization model"""
    global _summarizer
    if _summarizer is None:
        # Use distilbart - smaller, faster, good enough for demo
        _summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",  # ← Changed to smaller model (300MB vs 1.6GB)
            device=-1  # -1 for CPU, 0 for GPU
        )
    return _summarizer

def summarize_text(text: str, max_length: int = 150, min_length: int = 50) -> str:
    """
    Summarize text using BART model.
    
    Args:
        text: Input text to summarize
        max_length: Maximum summary length
        min_length: Minimum summary length
    
    Returns:
        Summarized text string
    """
    if not text or len(text.strip()) < 100:
        return "Text too short to summarize."
    
    summarizer = get_summarizer()
    
    # BART has max 1024 tokens, truncate if needed
    if len(text) > 1024:
        text = text[:1024]
    
    try:
        result = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False,
            truncation=True
        )
        return result[0]['summary_text']
    except Exception as e:
        return f"Summarization failed: {str(e)}"
