from typing import List, Tuple
from functools import lru_cache

def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap.
    Simple character-based splitting for basic RAG.
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def simple_keyword_score(query: str, text: str) -> float:
    """
    Simple keyword-based relevance scoring.
    Returns a score based on how many query words appear in the text.
    """
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    
    if not query_words:
        return 0.0
    
    # Count matching words
    matches = query_words.intersection(text_words)
    return len(matches) / len(query_words)

@lru_cache(maxsize=10)
def generate_chunks_cached(text_hash: int, text_content: str) -> List[str]:
    """
    Generate chunks for a text. Cached by hash to speed up multi-turn chat.
    """
    return chunk_text(text_content)

def retrieve_context(paper_text: str, query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant chunks for a query from the paper text using keyword matching.
    """
    if not paper_text or not query:
        return ""

    # Generate or get cached chunks
    chunks = generate_chunks_cached(hash(paper_text), paper_text)
    
    # Score each chunk
    scored_chunks = []
    for i, chunk in enumerate(chunks):
        score = simple_keyword_score(query, chunk)
        scored_chunks.append((score, i, chunk))
    
    # Sort by score (descending) and get top k
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [chunk for _, _, chunk in scored_chunks[:top_k]]
    
    return "\n\n".join(top_chunks)

