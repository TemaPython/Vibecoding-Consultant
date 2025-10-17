"""Similarity calculation utilities for embeddings."""
import numpy as np
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Calculate cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        Cosine similarity score (0 to 1)
    """
    # Reshape to 2D arrays for sklearn
    emb1 = embedding1.reshape(1, -1)
    emb2 = embedding2.reshape(1, -1)
    
    similarity = cosine_similarity(emb1, emb2)[0][0]
    return float(similarity)


def calculate_similarity_matrix(embeddings: List[np.ndarray]) -> np.ndarray:
    """Calculate pairwise similarity matrix for multiple embeddings.
    
    Args:
        embeddings: List of embedding vectors
        
    Returns:
        Similarity matrix (n x n)
    """
    embeddings_array = np.array(embeddings)
    return cosine_similarity(embeddings_array)


def find_most_similar(
    query_embedding: np.ndarray,
    candidate_embeddings: List[np.ndarray],
    top_k: int = 10
) -> List[Tuple[int, float]]:
    """Find most similar embeddings to query.
    
    Args:
        query_embedding: Query embedding vector
        candidate_embeddings: List of candidate embeddings
        top_k: Number of top results to return
        
    Returns:
        List of (index, similarity_score) tuples, sorted by similarity descending
    """
    similarities = []
    
    for idx, candidate in enumerate(candidate_embeddings):
        similarity = calculate_cosine_similarity(query_embedding, candidate)
        similarities.append((idx, similarity))
    
    # Sort by similarity descending
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    return similarities[:top_k]


def average_embeddings(embeddings: List[np.ndarray], weights: List[float] = None) -> np.ndarray:
    """Calculate weighted average of embeddings.
    
    Args:
        embeddings: List of embedding vectors
        weights: Optional weights for each embedding (default: equal weights)
        
    Returns:
        Average embedding vector
    """
    embeddings_array = np.array(embeddings)
    
    if weights is None:
        return np.mean(embeddings_array, axis=0)
    
    weights_array = np.array(weights).reshape(-1, 1)
    weighted_sum = np.sum(embeddings_array * weights_array, axis=0)
    return weighted_sum / np.sum(weights)


def find_intersection_preferences(
    user1_embeddings: List[np.ndarray],
    user2_embeddings: List[np.ndarray],
    catalog_embeddings: List[np.ndarray],
    threshold: float = 0.7,
    top_k: int = 20
) -> List[Tuple[int, float]]:
    """Find movies that match both users' preferences.
    
    Args:
        user1_embeddings: Embeddings of movies liked by user 1
        user2_embeddings: Embeddings of movies liked by user 2
        catalog_embeddings: All movie embeddings in catalog
        threshold: Minimum similarity threshold
        top_k: Number of results to return
        
    Returns:
        List of (catalog_index, combined_score) tuples
    """
    # Calculate average preference for each user
    user1_avg = average_embeddings(user1_embeddings)
    user2_avg = average_embeddings(user2_embeddings)
    
    # Calculate combined similarity for each catalog movie
    results = []
    
    for idx, catalog_emb in enumerate(catalog_embeddings):
        sim1 = calculate_cosine_similarity(user1_avg, catalog_emb)
        sim2 = calculate_cosine_similarity(user2_avg, catalog_emb)
        
        # Only include if both similarities are above threshold
        if sim1 >= threshold and sim2 >= threshold:
            # Combined score (average of both similarities)
            combined_score = (sim1 + sim2) / 2
            results.append((idx, combined_score))
    
    # Sort by combined score descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    return results[:top_k]

