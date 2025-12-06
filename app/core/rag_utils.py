import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
from functools import lru_cache

# Initialize model (lazy loading handled by library, but we instantiate global)
# all-MiniLM-L6-v2 is fast and efficient
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

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

@lru_cache(maxsize=10)
def generate_embeddings_cached(text_hash: int, text_content: str) -> Tuple[np.ndarray, List[str]]:
    """
    Generate embeddings for a text. Cached by hash of the text to speed up multi-turn chat.
    Returns (embeddings_matrix, chunks_list)
    """
    chunks = chunk_text(text_content)
    model = get_embedding_model()
    embeddings = model.encode(chunks)
    return embeddings, chunks

def retrieve_context(paper_text: str, query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant chunks for a query from the paper text.
    """
    if not paper_text or not query:
        return ""

    # Generate or get cached embeddings
    # We use hash(paper_text) as a simple cache key
    embeddings, chunks = generate_embeddings_cached(hash(paper_text), paper_text)
    
    model = get_embedding_model()
    query_embedding = model.encode([query])
    
    # Calculate similarity
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # Get top k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Construct context
    context_chunks = [chunks[i] for i in top_indices]
    return "\n\n".join(context_chunks)
