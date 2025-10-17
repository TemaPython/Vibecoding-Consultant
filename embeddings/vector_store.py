"""Vector store for caching and retrieving movie embeddings."""
import pickle
import numpy as np
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import config


class VectorStore:
    """Manages storage and retrieval of movie embeddings."""
    
    def __init__(self, cache_path: str = None):
        """Initialize vector store.
        
        Args:
            cache_path: Path to cache file
        """
        self.cache_path = cache_path or config.EMBEDDINGS_CACHE_PATH
        self.embeddings: Dict[int, np.ndarray] = {}  # movie_index -> embedding
        self.metadata: Dict[int, Dict] = {}  # movie_index -> metadata
        
    def add_embedding(self, movie_index: int, embedding: np.ndarray, metadata: Dict = None):
        """Add an embedding to the store.
        
        Args:
            movie_index: Movie index in catalog
            embedding: Embedding vector
            metadata: Optional metadata about the movie
        """
        self.embeddings[movie_index] = embedding
        
        if metadata:
            self.metadata[movie_index] = metadata
    
    def add_embeddings_batch(self, indices: List[int], embeddings: List[np.ndarray], metadata_list: List[Dict] = None):
        """Add multiple embeddings at once.
        
        Args:
            indices: List of movie indices
            embeddings: List of embedding vectors
            metadata_list: Optional list of metadata dictionaries
        """
        for i, (idx, emb) in enumerate(zip(indices, embeddings)):
            meta = metadata_list[i] if metadata_list and i < len(metadata_list) else None
            self.add_embedding(idx, emb, meta)
    
    def get_embedding(self, movie_index: int) -> Optional[np.ndarray]:
        """Get embedding for a specific movie.
        
        Args:
            movie_index: Movie index
            
        Returns:
            Embedding vector or None if not found
        """
        return self.embeddings.get(movie_index)
    
    def get_embeddings(self, movie_indices: List[int]) -> List[np.ndarray]:
        """Get embeddings for multiple movies.
        
        Args:
            movie_indices: List of movie indices
            
        Returns:
            List of embedding vectors (None for missing indices)
        """
        return [self.embeddings.get(idx) for idx in movie_indices]
    
    def get_all_embeddings(self) -> Tuple[List[int], List[np.ndarray]]:
        """Get all stored embeddings.
        
        Returns:
            Tuple of (indices, embeddings)
        """
        indices = list(self.embeddings.keys())
        embeddings = [self.embeddings[idx] for idx in indices]
        return indices, embeddings
    
    def has_embedding(self, movie_index: int) -> bool:
        """Check if embedding exists for a movie.
        
        Args:
            movie_index: Movie index
            
        Returns:
            True if embedding exists
        """
        return movie_index in self.embeddings
    
    def size(self) -> int:
        """Get number of stored embeddings.
        
        Returns:
            Number of embeddings
        """
        return len(self.embeddings)
    
    def save_to_disk(self):
        """Save embeddings to disk cache."""
        try:
            # Create directory if it doesn't exist
            Path(self.cache_path).parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'embeddings': self.embeddings,
                'metadata': self.metadata
            }
            
            with open(self.cache_path, 'wb') as f:
                pickle.dump(data, f)
            
            print(f"[+] Saved {len(self.embeddings)} embeddings to {self.cache_path}")
            
        except Exception as e:
            print(f"[!] Error saving embeddings: {e}")
    
    def load_from_disk(self) -> bool:
        """Load embeddings from disk cache.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not Path(self.cache_path).exists():
                print(f"[i] No cache file found at {self.cache_path}")
                return False
            
            with open(self.cache_path, 'rb') as f:
                data = pickle.load(f)
            
            self.embeddings = data.get('embeddings', {})
            self.metadata = data.get('metadata', {})
            
            print(f"[+] Loaded {len(self.embeddings)} embeddings from cache")
            return True
            
        except Exception as e:
            print(f"[!] Error loading embeddings: {e}")
            return False
    
    def clear(self):
        """Clear all embeddings from memory."""
        self.embeddings.clear()
        self.metadata.clear()
    
    def search_similar(
        self,
        query_embedding: np.ndarray,
        top_k: int = 10,
        exclude_indices: List[int] = None
    ) -> List[Tuple[int, float]]:
        """Search for similar movies using cosine similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            exclude_indices: Movie indices to exclude from results
            
        Returns:
            List of (movie_index, similarity_score) tuples
        """
        from embeddings.similarity import calculate_cosine_similarity
        
        exclude_set = set(exclude_indices or [])
        similarities = []
        
        for movie_idx, movie_emb in self.embeddings.items():
            if movie_idx in exclude_set:
                continue
            
            similarity = calculate_cosine_similarity(query_embedding, movie_emb)
            similarities.append((movie_idx, similarity))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]

