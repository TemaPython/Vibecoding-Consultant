"""Main recommendation engine."""
import numpy as np
from typing import List, Dict, Tuple
import pandas as pd
from embeddings.embedding_manager import EmbeddingManager
from embeddings.vector_store import VectorStore
from embeddings.similarity import find_most_similar, average_embeddings
from catalog.catalog_loader import CatalogLoader
from recommender.content_filter import ContentFilter


class RecommendationEngine:
    """Main recommendation engine using embeddings."""
    
    def __init__(
        self,
        catalog_loader: CatalogLoader,
        embedding_manager: EmbeddingManager,
        vector_store: VectorStore
    ):
        """Initialize recommendation engine.
        
        Args:
            catalog_loader: Catalog loader instance
            embedding_manager: Embedding manager instance
            vector_store: Vector store instance
        """
        self.catalog = catalog_loader
        self.embedding_manager = embedding_manager
        self.vector_store = vector_store
        self.content_filter = ContentFilter(catalog_loader.df)
    
    def initialize_embeddings(self, force_refresh: bool = False):
        """Initialize or load movie embeddings.
        
        Args:
            force_refresh: Force regeneration of embeddings
        """
        # Try to load from cache first
        if not force_refresh and self.vector_store.load_from_disk():
            print(f"[+] Using cached embeddings ({self.vector_store.size()} movies)")
            return
        
        print("[i] Generating embeddings for all movies (this may take a while)...")
        
        # Generate embeddings for all movies
        movie_descriptions = []
        movie_indices = []
        
        for idx in self.catalog.df.index:
            movie = self.catalog.get_movie_by_index(idx)
            description = self.catalog.create_movie_description(movie)
            movie_descriptions.append(description)
            movie_indices.append(idx)
        
        # Create embeddings in batches
        embeddings = self.embedding_manager.create_embeddings_batch(movie_descriptions)
        
        # Store embeddings
        self.vector_store.add_embeddings_batch(movie_indices, embeddings)
        
        # Save to cache
        self.vector_store.save_to_disk()
        
        print(f"[+] Generated and cached {len(embeddings)} embeddings")
    
    def get_recommendations_by_query(
        self,
        query_text: str,
        top_k: int = 10,
        exclude_indices: List[int] = None
    ) -> List[Tuple[int, float]]:
        """Get recommendations based on text query.
        
        Args:
            query_text: User query or preferences as text
            top_k: Number of recommendations
            exclude_indices: Movie indices to exclude
            
        Returns:
            List of (movie_index, similarity_score) tuples
        """
        # Create embedding for query
        query_embedding = self.embedding_manager.create_embedding(query_text)
        
        # Search in vector store
        results = self.vector_store.search_similar(
            query_embedding,
            top_k=top_k * 2,  # Get more to account for exclusions
            exclude_indices=exclude_indices
        )
        
        return results[:top_k]
    
    def get_recommendations_by_preferences(
        self,
        preferences: Dict,
        top_k: int = 10,
        exclude_indices: List[int] = None
    ) -> List[Tuple[int, float]]:
        """Get recommendations based on user preferences.
        
        Args:
            preferences: Dictionary with user preferences
            top_k: Number of recommendations
            exclude_indices: Movie indices to exclude
            
        Returns:
            List of (movie_index, similarity_score) tuples
        """
        # Convert preferences to query text
        from ai.assistant import MovieAssistant
        assistant = MovieAssistant()
        query_text = assistant.create_query_embedding_text(preferences)
        
        return self.get_recommendations_by_query(query_text, top_k, exclude_indices)
    
    def get_recommendations_by_liked_movies(
        self,
        liked_movie_indices: List[int],
        top_k: int = 10,
        exclude_indices: List[int] = None
    ) -> List[Tuple[int, float]]:
        """Get recommendations based on movies user liked.
        
        Args:
            liked_movie_indices: Indices of movies user liked
            top_k: Number of recommendations
            exclude_indices: Movie indices to exclude
            
        Returns:
            List of (movie_index, similarity_score) tuples
        """
        if not liked_movie_indices:
            return []
        
        # Get embeddings for liked movies
        liked_embeddings = []
        for idx in liked_movie_indices:
            emb = self.vector_store.get_embedding(idx)
            if emb is not None:
                liked_embeddings.append(emb)
        
        if not liked_embeddings:
            return []
        
        # Calculate average embedding of liked movies
        avg_embedding = average_embeddings(liked_embeddings)
        
        # Search for similar movies
        results = self.vector_store.search_similar(
            avg_embedding,
            top_k=top_k * 2,
            exclude_indices=exclude_indices
        )
        
        return results[:top_k]
    
    def refine_recommendations(
        self,
        preferences: Dict,
        liked_movie_indices: List[int],
        disliked_movie_indices: List[int],
        top_k: int = 15
    ) -> List[Tuple[int, float]]:
        """Refine recommendations based on preferences and ratings.
        
        Args:
            preferences: User preferences
            liked_movie_indices: Movies user liked
            disliked_movie_indices: Movies user disliked
            top_k: Number of recommendations
            
        Returns:
            List of (movie_index, similarity_score) tuples
        """
        # Combine liked movies and disliked movies for exclusion
        exclude_indices = liked_movie_indices + disliked_movie_indices
        
        # Get recommendations from both preferences and liked movies
        pref_recs = self.get_recommendations_by_preferences(
            preferences,
            top_k=top_k,
            exclude_indices=exclude_indices
        )
        
        liked_recs = self.get_recommendations_by_liked_movies(
            liked_movie_indices,
            top_k=top_k,
            exclude_indices=exclude_indices
        )
        
        # Combine and deduplicate
        combined = {}
        
        # Weight preference-based recommendations higher
        for idx, score in pref_recs:
            combined[idx] = score * 0.6
        
        # Add liked-based recommendations
        for idx, score in liked_recs:
            if idx in combined:
                combined[idx] += score * 0.4
            else:
                combined[idx] = score * 0.4
        
        # Sort by combined score
        results = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        
        return results[:top_k]
    
    def get_movies_dataframe(self, movie_indices: List[int]) -> pd.DataFrame:
        """Get DataFrame with movie details.
        
        Args:
            movie_indices: List of movie indices
            
        Returns:
            DataFrame with movie details
        """
        return self.catalog.get_movies_by_indices(movie_indices)

