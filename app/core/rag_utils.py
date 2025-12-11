import numpy as np
from typing import List, Tuple
from functools import lru_cache
import gc

# Initialize model (lazy loading handled by library, but we instantiate global)
# Using all-MiniLM-L12-v2: smallest viable model (33MB) for Render Free Tier
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        # Lazy import to avoid OOM on startup
        from sentence_transformers import SentenceTransformer
        # Use smallest model for memory efficiency on Render
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2')
    return _model

def cleanup_model():
    """Explicitly cleanup model from memory after use"""
    global _model
    if _model is not None:
        del _model
        _model = None
        gc.collect()

def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap.
    Reduced chunk size for memory efficiency.
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

@lru_cache(maxsize=3)  # Reduced cache size to save memory
def generate_embeddings_cached(text_hash: int, text_content: str) -> Tuple[np.ndarray, List[str]]:
    """
    Generate embeddings for a text. Cached by hash of the text to speed up multi-turn chat.
    Returns (embeddings_matrix, chunks_list)
    """
    chunks = chunk_text(text_content)
    # Limit to first 10 chunks for memory efficiency (enough for demo)
    chunks = chunks[:10]
    
    model = get_embedding_model()
    embeddings = model.encode(chunks, show_progress_bar=False)
    
    # Aggressive cleanup after encoding
    cleanup_model()
    gc.collect()
    
    return embeddings, chunks

def retrieve_context(paper_text: str, query: str, top_k: int = 7) -> str:
    """
    Retrieve relevant chunks for a query from the paper text.
    """
    if not paper_text or not query:
        return ""

    # Generate or get cached embeddings
    # We use hash(paper_text) as a simple cache key
    embeddings, chunks = generate_embeddings_cached(hash(paper_text), paper_text)
    
    model = get_embedding_model()
    query_embedding = model.encode([query], show_progress_bar=False)
    
    # Calculate similarity
    from sklearn.metrics.pairwise import cosine_similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # Get top k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Construct context
    context_chunks = [chunks[i] for i in top_indices]
    
    # Force garbage collection
    gc.collect()
    
    return "\n\n".join(context_chunks)

