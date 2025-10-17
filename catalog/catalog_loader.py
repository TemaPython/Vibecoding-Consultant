"""Movie catalog loader and manager."""
import pandas as pd
from typing import List, Dict, Optional
import config


class CatalogLoader:
    """Manages loading and querying the Okko movie catalog."""
    
    def __init__(self, catalog_path: str = None):
        """Initialize catalog loader.
        
        Args:
            catalog_path: Path to the parquet catalog file
        """
        self.catalog_path = catalog_path or config.CATALOG_PATH
        self.df: Optional[pd.DataFrame] = None
        
    def load_catalog(self) -> pd.DataFrame:
        """Load the movie catalog from parquet file.
        
        Returns:
            DataFrame with movie catalog
        """
        try:
            self.df = pd.read_parquet(self.catalog_path)
            print(f"[+] Catalog loaded: {len(self.df)} movies")
            return self.df
        except FileNotFoundError:
            print(f"[!] Error: Catalog file not found at {self.catalog_path}")
            raise
        except Exception as e:
            print(f"[!] Error loading catalog: {e}")
            raise
    
    def get_catalog_info(self) -> Dict:
        """Get information about the catalog.
        
        Returns:
            Dictionary with catalog statistics
        """
        if self.df is None:
            raise ValueError("Catalog not loaded. Call load_catalog() first.")
        
        return {
            "total_movies": len(self.df),
            "columns": list(self.df.columns),
            "genres": self._get_unique_genres(),
            "countries": self.df['country'].unique().tolist() if 'country' in self.df.columns else [],
            "age_ratings": self.df['age_rating'].unique().tolist() if 'age_rating' in self.df.columns else []
        }
    
    def _get_unique_genres(self) -> List[str]:
        """Extract unique genres from the catalog."""
        if 'genres' not in self.df.columns:
            return []
        
        genres = set()
        for genre_str in self.df['genres'].dropna():
            # Assuming genres are comma-separated
            if isinstance(genre_str, str):
                genres.update([g.strip() for g in genre_str.split(',')])
        return sorted(list(genres))
    
    def search_by_actor(self, actor_name: str, limit: int = 50) -> pd.DataFrame:
        """Search movies by actor name.
        
        Args:
            actor_name: Actor name to search for
            limit: Maximum number of results
            
        Returns:
            DataFrame with matching movies
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        mask = self.df['actors'].str.contains(actor_name, case=False, na=False)
        return self.df[mask].head(limit)
    
    def search_by_director(self, director_name: str, limit: int = 50) -> pd.DataFrame:
        """Search movies by director name.
        
        Args:
            director_name: Director name to search for
            limit: Maximum number of results
            
        Returns:
            DataFrame with matching movies
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        mask = self.df['director'].str.contains(director_name, case=False, na=False)
        return self.df[mask].head(limit)
    
    def search_by_genre(self, genre: str, limit: int = 50) -> pd.DataFrame:
        """Search movies by genre.
        
        Args:
            genre: Genre to search for
            limit: Maximum number of results
            
        Returns:
            DataFrame with matching movies
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        mask = self.df['genres'].str.contains(genre, case=False, na=False)
        return self.df[mask].head(limit)
    
    def filter_by_age_rating(self, max_age_rating: float) -> pd.DataFrame:
        """Filter movies by age rating.
        
        Args:
            max_age_rating: Maximum age rating (inclusive)
            
        Returns:
            DataFrame with matching movies
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        if 'age_rating' not in self.df.columns:
            return self.df
        
        mask = self.df['age_rating'] <= max_age_rating
        return self.df[mask]
    
    def get_movie_by_index(self, index: int) -> Optional[Dict]:
        """Get movie details by DataFrame index.
        
        Args:
            index: DataFrame index
            
        Returns:
            Dictionary with movie details or None
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        if index not in self.df.index:
            return None
        
        return self.df.loc[index].to_dict()
    
    def get_movies_by_indices(self, indices: List[int]) -> pd.DataFrame:
        """Get multiple movies by their indices.
        
        Args:
            indices: List of DataFrame indices
            
        Returns:
            DataFrame with selected movies
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        return self.df.loc[indices]
    
    def create_movie_description(self, movie: Dict) -> str:
        """Create a text description of a movie for embeddings.
        
        Args:
            movie: Dictionary with movie details
            
        Returns:
            Text description
        """
        parts = []
        
        if movie.get('serial_name'):
            parts.append(f"Название: {movie['serial_name']}")
        
        if movie.get('genres'):
            parts.append(f"Жанры: {movie['genres']}")
        
        if movie.get('director'):
            parts.append(f"Режиссер: {movie['director']}")
        
        if movie.get('actors'):
            parts.append(f"Актеры: {movie['actors']}")
        
        if movie.get('country'):
            parts.append(f"Страна: {movie['country']}")
        
        if movie.get('description'):
            parts.append(f"Описание: {movie['description']}")
        
        return ". ".join(parts)
    
    def get_random_movies(self, n: int = 10) -> pd.DataFrame:
        """Get random movies from catalog.
        
        Args:
            n: Number of movies to return
            
        Returns:
            DataFrame with random movies
        """
        if self.df is None:
            raise ValueError("Catalog not loaded")
        
        return self.df.sample(n=min(n, len(self.df)))

