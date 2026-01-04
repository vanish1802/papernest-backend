import os
import numpy as np
from typing import List, Tuple
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_embedding_model():
    """Get FastEmbed model"""
    try:
        from fastembed import TextEmbedding
        # Use a lightweight, high-performance model (defaults to BAAI/bge-small-en-v1.5)
        # These models are ONNX optimized and very memory efficient (~200MB RAM)
        return TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    except ImportError:
        raise ImportError("Please install fastembed: pip install fastembed")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks with overlap.
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

@lru_cache(maxsize=5)
def generate_embeddings_cached(text_hash: int, text_content: str) -> Tuple[np.ndarray, List[str]]:
    """
    Generate embeddings using local FastEmbed.
    Cached by hash of the text to speed up multi-turn chat.
    Returns (embeddings_matrix, chunks_list)
    """
    chunks = chunk_text(text_content)
    # Limit chunks processing
    chunks = chunks[:50] 
    
    model = get_embedding_model()
    
    # Generate embeddings locally
    # fastembed returns a generator of numpy arrays, we convert to list then array
    embeddings_list = list(model.embed(chunks))
    embeddings = np.array(embeddings_list)
    
    return embeddings, chunks

def retrieve_context(paper_text: str, query: str, top_k: int = 5) -> str:
    """
    Retrieve relevant chunks for a query from the paper text using local embeddings.
    """
    if not paper_text or not query:
        return ""

    # Generate or get cached embeddings for document
    embeddings, chunks = generate_embeddings_cached(hash(paper_text), paper_text)
    
    # Get query embedding
    model = get_embedding_model()
    # model.embed returns generator, we take first item for single query
    query_embedding = list(model.embed([query]))[0]
    
    # Calculate cosine similarity
    # Normalize vectors
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    
    # Compute similarities
    similarities = np.dot(embeddings_norm, query_norm)
    
    # Get top k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Construct context
    context_chunks = [chunks[i] for i in top_indices]
    
    return "\n\n".join(context_chunks)


