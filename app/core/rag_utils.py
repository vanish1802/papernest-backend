import os
import numpy as np
from typing import List, Tuple
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_cohere_client():
    """Get Cohere client for embeddings"""
    try:
        import cohere
    except ImportError:
        raise ImportError("Please install cohere: pip install cohere")
    
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")
    
    return cohere.Client(api_key)

def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> List[str]:
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
    Generate embeddings using Cohere API.
    Cached by hash of the text to speed up multi-turn chat.
    Returns (embeddings_matrix, chunks_list)
    """
    chunks = chunk_text(text_content)
    # Limit to first 15 chunks (Cohere can handle more than local models)
    chunks = chunks[:15]
    
    client = get_cohere_client()
    
    # Get embeddings from Cohere API
    response = client.embed(
        texts=chunks,
        model='embed-english-light-v3.0',  # Lightweight, fast, free tier friendly
        input_type='search_document'
    )
    
    # Convert to numpy array
    embeddings = np.array(response.embeddings)
    
    return embeddings, chunks

def retrieve_context(paper_text: str, query: str, top_k: int = 7) -> str:
    """
    Retrieve relevant chunks for a query from the paper text using Cohere embeddings.
    """
    if not paper_text or not query:
        return ""

    # Generate or get cached embeddings for document
    embeddings, chunks = generate_embeddings_cached(hash(paper_text), paper_text)
    
    # Get query embedding
    client = get_cohere_client()
    query_response = client.embed(
        texts=[query],
        model='embed-english-light-v3.0',
        input_type='search_query'
    )
    query_embedding = np.array(query_response.embeddings)
    
    # Calculate cosine similarity
    # Normalize vectors
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    query_norm = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    
    # Compute similarities
    similarities = np.dot(embeddings_norm, query_norm.T).flatten()
    
    # Get top k indices
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Construct context
    context_chunks = [chunks[i] for i in top_indices]
    
    return "\n\n".join(context_chunks)


