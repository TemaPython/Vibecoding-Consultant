"""Content filtering for movie recommendations."""
import pandas as pd
from typing import List, Dict, Optional


class ContentFilter:
    """Filters movies based on various criteria."""
    
    def __init__(self, catalog_df: pd.DataFrame):
        """Initialize content filter.
        
        Args:
            catalog_df: Movie catalog DataFrame
        """
        self.catalog_df = catalog_df
    
    def filter_by_preferences(self, preferences: Dict) -> pd.DataFrame:
        """Filter movies by user preferences.
        
        Args:
            preferences: Dictionary with user preferences
            
        Returns:
            Filtered DataFrame
        """
        filtered_df = self.catalog_df.copy()
        
        # Filter by actors
        if preferences.get('actors'):
            actors = preferences['actors']
            if isinstance(actors, str):
                actors = [actors]
            
            mask = pd.Series([False] * len(filtered_df))
            for actor in actors:
                mask |= filtered_df['actors'].str.contains(actor, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        # Filter by directors
        if preferences.get('directors'):
            directors = preferences['directors']
            if isinstance(directors, str):
                directors = [directors]
            
            mask = pd.Series([False] * len(filtered_df))
            for director in directors:
                mask |= filtered_df['director'].str.contains(director, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        # Filter by genres
        if preferences.get('genres'):
            genres = preferences['genres']
            if isinstance(genres, str):
                genres = [genres]
            
            mask = pd.Series([False] * len(filtered_df))
            for genre in genres:
                mask |= filtered_df['genres'].str.contains(genre, case=False, na=False)
            filtered_df = filtered_df[mask]
        
        return filtered_df
    
    def exclude_rated_movies(self, movie_indices: List[int]) -> pd.DataFrame:
        """Exclude already rated movies.
        
        Args:
            movie_indices: List of movie indices to exclude
            
        Returns:
            Filtered DataFrame
        """
        return self.catalog_df[~self.catalog_df.index.isin(movie_indices)]
    
    def filter_by_age_rating(self, max_age_rating: float) -> pd.DataFrame:
        """Filter by age rating.
        
        Args:
            max_age_rating: Maximum age rating
            
        Returns:
            Filtered DataFrame
        """
        if 'age_rating' not in self.catalog_df.columns:
            return self.catalog_df
        
        return self.catalog_df[self.catalog_df['age_rating'] <= max_age_rating]
    
    def filter_by_genre(self, genre: str) -> pd.DataFrame:
        """Filter by specific genre.
        
        Args:
            genre: Genre name
            
        Returns:
            Filtered DataFrame
        """
        mask = self.catalog_df['genres'].str.contains(genre, case=False, na=False)
        return self.catalog_df[mask]
    
    def filter_by_actor(self, actor: str) -> pd.DataFrame:
        """Filter by specific actor.
        
        Args:
            actor: Actor name
            
        Returns:
            Filtered DataFrame
        """
        mask = self.catalog_df['actors'].str.contains(actor, case=False, na=False)
        return self.catalog_df[mask]
    
    def get_genre_intersection(self, genres1: List[str], genres2: List[str]) -> List[str]:
        """Get intersection of two genre lists.
        
        Args:
            genres1: First list of genres
            genres2: Second list of genres
            
        Returns:
            List of common genres
        """
        set1 = set(g.lower().strip() for g in genres1)
        set2 = set(g.lower().strip() for g in genres2)
        return list(set1 & set2)
    
    def filter_by_genres_intersection(self, genres: List[str]) -> pd.DataFrame:
        """Filter movies that contain any of the specified genres.
        
        Args:
            genres: List of genres
            
        Returns:
            Filtered DataFrame
        """
        if not genres:
            return pd.DataFrame()
        
        mask = pd.Series([False] * len(self.catalog_df))
        for genre in genres:
            mask |= self.catalog_df['genres'].str.contains(genre, case=False, na=False)
        
        return self.catalog_df[mask]
    
    def extract_genres_from_movies(self, movie_indices: List[int]) -> List[str]:
        """Extract all genres from given movies.
        
        Args:
            movie_indices: List of movie indices
            
        Returns:
            List of unique genres
        """
        movies = self.catalog_df.loc[movie_indices]
        genres_set = set()
        
        for genres_str in movies['genres'].dropna():
            if isinstance(genres_str, str):
                # Split by comma and clean
                genre_list = [g.strip() for g in genres_str.split(',')]
                genres_set.update(genre_list)
        
        return list(genres_set)

