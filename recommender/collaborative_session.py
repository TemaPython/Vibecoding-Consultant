"""Collaborative recommendation session for two users (30-30-40 split)."""
import numpy as np
from typing import List, Dict, Tuple
from embeddings.similarity import find_intersection_preferences
from recommender.recommendation_engine import RecommendationEngine
from recommender.content_filter import ContentFilter
import config


class CollaborativeSession:
    """Manages collaborative movie recommendations for two users."""
    
    def __init__(self, recommendation_engine: RecommendationEngine):
        """Initialize collaborative session.
        
        Args:
            recommendation_engine: Recommendation engine instance
        """
        self.engine = recommendation_engine
        self.content_filter = ContentFilter(recommendation_engine.catalog.df)
    
    def get_collaborative_recommendations(
        self,
        user1_preferences: Dict,
        user2_preferences: Dict,
        user1_liked_movies: List[int],
        user2_liked_movies: List[int],
        user1_disliked_movies: List[int] = None,
        user2_disliked_movies: List[int] = None,
        total_count: int = None
    ) -> Dict[str, List[Tuple[int, float]]]:
        """Get collaborative recommendations with 30-30-40 split.
        
        Args:
            user1_preferences: User 1 preferences
            user2_preferences: User 2 preferences
            user1_liked_movies: Movies user 1 liked
            user2_liked_movies: Movies user 2 liked
            user1_disliked_movies: Movies user 1 disliked
            user2_disliked_movies: Movies user 2 disliked
            total_count: Total number of recommendations (default from config)
            
        Returns:
            Dictionary with 'user1', 'user2', and 'intersection' movie lists
        """
        total_count = total_count or config.FINAL_RECOMMENDATIONS_COUNT
        
        # Calculate split
        split = config.RECOMMENDATION_SPLIT
        user1_count = int(total_count * split['user1_preference'])
        user2_count = int(total_count * split['user2_preference'])
        intersection_count = total_count - user1_count - user2_count
        
        # Combine all rated movies for exclusion
        user1_disliked = user1_disliked_movies or []
        user2_disliked = user2_disliked_movies or []
        
        all_rated = (user1_liked_movies + user2_liked_movies + 
                    user1_disliked + user2_disliked)
        
        # Get recommendations for user 1
        user1_recs = self._get_user_specific_recommendations(
            user1_preferences,
            user1_liked_movies,
            all_rated,
            user1_count
        )
        
        # Get recommendations for user 2
        user2_recs = self._get_user_specific_recommendations(
            user2_preferences,
            user2_liked_movies,
            all_rated,
            user2_count
        )
        
        # Get intersection recommendations
        intersection_recs = self._get_intersection_recommendations(
            user1_preferences,
            user2_preferences,
            user1_liked_movies,
            user2_liked_movies,
            all_rated,
            intersection_count
        )
        
        return {
            'user1': user1_recs,
            'user2': user2_recs,
            'intersection': intersection_recs
        }
    
    def _get_user_specific_recommendations(
        self,
        preferences: Dict,
        liked_movies: List[int],
        exclude_movies: List[int],
        count: int
    ) -> List[Tuple[int, float]]:
        """Get recommendations specific to one user.
        
        Args:
            preferences: User preferences
            liked_movies: Movies user liked
            exclude_movies: Movies to exclude
            count: Number of recommendations
            
        Returns:
            List of (movie_index, score) tuples
        """
        # Try to get recommendations based on specific actor/director first
        specific_actor = None
        specific_director = None
        
        if preferences.get('actors'):
            actors = preferences['actors']
            specific_actor = actors[0] if isinstance(actors, list) else actors
        
        if preferences.get('directors'):
            directors = preferences['directors']
            specific_director = directors[0] if isinstance(directors, list) else directors
        
        # Filter by actor if specified
        if specific_actor:
            actor_movies = self.content_filter.filter_by_actor(specific_actor)
            actor_indices = [idx for idx in actor_movies.index if idx not in exclude_movies]
            
            if len(actor_indices) >= count:
                # Get embeddings and rank
                return self._rank_by_preferences(
                    actor_indices[:count * 2],
                    preferences,
                    liked_movies,
                    count
                )
        
        # Filter by director if specified
        if specific_director:
            director_movies = self.content_filter.catalog_df[
                self.content_filter.catalog_df['director'].str.contains(
                    specific_director, case=False, na=False
                )
            ]
            director_indices = [idx for idx in director_movies.index if idx not in exclude_movies]
            
            if len(director_indices) >= count:
                return self._rank_by_preferences(
                    director_indices[:count * 2],
                    preferences,
                    liked_movies,
                    count
                )
        
        # Fall back to general recommendations
        return self.engine.refine_recommendations(
            preferences,
            liked_movies,
            [],
            top_k=count
        )
    
    def _get_intersection_recommendations(
        self,
        user1_preferences: Dict,
        user2_preferences: Dict,
        user1_liked_movies: List[int],
        user2_liked_movies: List[int],
        exclude_movies: List[int],
        count: int
    ) -> List[Tuple[int, float]]:
        """Get intersection recommendations that both users might like.
        
        Args:
            user1_preferences: User 1 preferences
            user2_preferences: User 2 preferences
            user1_liked_movies: Movies user 1 liked
            user2_liked_movies: Movies user 2 liked
            exclude_movies: Movies to exclude
            count: Number of recommendations
            
        Returns:
            List of (movie_index, score) tuples
        """
        # Extract genres from liked movies of both users
        user1_genres = self.content_filter.extract_genres_from_movies(user1_liked_movies)
        user2_genres = self.content_filter.extract_genres_from_movies(user2_liked_movies)
        
        # Find common genres
        common_genres = self.content_filter.get_genre_intersection(user1_genres, user2_genres)
        
        # If no common genres, use all genres from both users
        if not common_genres:
            common_genres = list(set(user1_genres + user2_genres))
        
        # Filter movies by common genres
        genre_movies = self.content_filter.filter_by_genres_intersection(common_genres)
        candidate_indices = [idx for idx in genre_movies.index if idx not in exclude_movies]
        
        if not candidate_indices:
            # Fallback: combine preferences
            combined_prefs = self._combine_preferences(user1_preferences, user2_preferences)
            return self.engine.get_recommendations_by_preferences(
                combined_prefs,
                top_k=count,
                exclude_indices=exclude_movies
            )
        
        # Get embeddings for both users' liked movies
        user1_embeddings = [
            self.engine.vector_store.get_embedding(idx)
            for idx in user1_liked_movies
            if self.engine.vector_store.has_embedding(idx)
        ]
        
        user2_embeddings = [
            self.engine.vector_store.get_embedding(idx)
            for idx in user2_liked_movies
            if self.engine.vector_store.has_embedding(idx)
        ]
        
        if not user1_embeddings or not user2_embeddings:
            # Fallback to genre-based ranking
            return [(idx, 1.0) for idx in candidate_indices[:count]]
        
        # Get all candidate embeddings
        candidate_embeddings = [
            self.engine.vector_store.get_embedding(idx)
            for idx in candidate_indices
        ]
        candidate_embeddings = [emb for emb in candidate_embeddings if emb is not None]
        
        if not candidate_embeddings:
            return []
        
        # Find movies that match both users' preferences
        results = find_intersection_preferences(
            user1_embeddings,
            user2_embeddings,
            candidate_embeddings,
            threshold=config.SIMILARITY_THRESHOLD * 0.8,  # Lower threshold for intersection
            top_k=count
        )
        
        # Map back to original indices
        valid_candidate_indices = [
            idx for idx in candidate_indices
            if self.engine.vector_store.has_embedding(idx)
        ]
        
        mapped_results = [
            (valid_candidate_indices[idx], score)
            for idx, score in results
            if idx < len(valid_candidate_indices)
        ]
        
        return mapped_results[:count]
    
    def _rank_by_preferences(
        self,
        candidate_indices: List[int],
        preferences: Dict,
        liked_movies: List[int],
        count: int
    ) -> List[Tuple[int, float]]:
        """Rank candidate movies by preferences.
        
        Args:
            candidate_indices: Candidate movie indices
            preferences: User preferences
            liked_movies: Movies user liked
            count: Number to return
            
        Returns:
            List of (movie_index, score) tuples
        """
        # Create preference embedding
        from ai.assistant import MovieAssistant
        assistant = MovieAssistant()
        query_text = assistant.create_query_embedding_text(preferences)
        query_embedding = self.engine.embedding_manager.create_embedding(query_text)
        
        # Score each candidate
        scored = []
        for idx in candidate_indices:
            emb = self.engine.vector_store.get_embedding(idx)
            if emb is not None:
                from embeddings.similarity import calculate_cosine_similarity
                score = calculate_cosine_similarity(query_embedding, emb)
                scored.append((idx, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return scored[:count]
    
    def _combine_preferences(self, prefs1: Dict, prefs2: Dict) -> Dict:
        """Combine two users' preferences.
        
        Args:
            prefs1: User 1 preferences
            prefs2: User 2 preferences
            
        Returns:
            Combined preferences
        """
        combined = {}
        
        # Combine lists
        for key in ['actors', 'directors', 'genres', 'themes']:
            items1 = prefs1.get(key, [])
            items2 = prefs2.get(key, [])
            
            if isinstance(items1, str):
                items1 = [items1]
            if isinstance(items2, str):
                items2 = [items2]
            
            combined[key] = list(set(items1 + items2))
        
        # Combine other fields
        if prefs1.get('mood') and prefs2.get('mood'):
            combined['mood'] = f"{prefs1['mood']}, {prefs2['mood']}"
        elif prefs1.get('mood'):
            combined['mood'] = prefs1['mood']
        elif prefs2.get('mood'):
            combined['mood'] = prefs2['mood']
        
        return combined

