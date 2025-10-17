"""Session manager for single and collaborative sessions."""
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from database.models import User, Session, Rating
from database.db_manager import DatabaseManager
from ai.assistant import MovieAssistant
from recommender.recommendation_engine import RecommendationEngine
from recommender.collaborative_session import CollaborativeSession


class SessionManager:
    """Manages user sessions (single or collaborative)."""
    
    def __init__(
        self,
        db_manager: DatabaseManager,
        recommendation_engine: RecommendationEngine
    ):
        """Initialize session manager.
        
        Args:
            db_manager: Database manager instance
            recommendation_engine: Recommendation engine instance
        """
        self.db = db_manager
        self.engine = recommendation_engine
        self.collaborative = CollaborativeSession(recommendation_engine)
    
    def create_single_session(self, user_name: str) -> Tuple[Session, User, MovieAssistant]:
        """Create a single-user session.
        
        Args:
            user_name: User's name
            
        Returns:
            Tuple of (Session, User, MovieAssistant)
        """
        # Create or get user
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        user = User(user_id=user_id, name=user_name)
        self.db.create_user(user)
        
        # Create session
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        session = Session(
            session_id=session_id,
            session_type='single',
            user_ids=[user_id]
        )
        self.db.create_session(session)
        
        # Create AI assistant
        assistant = MovieAssistant()
        
        return session, user, assistant
    
    def create_collaborative_session(
        self,
        user1_name: str,
        user2_name: str
    ) -> Tuple[Session, User, User, MovieAssistant, MovieAssistant]:
        """Create a collaborative session for two users.
        
        Args:
            user1_name: First user's name
            user2_name: Second user's name
            
        Returns:
            Tuple of (Session, User1, User2, Assistant1, Assistant2)
        """
        # Create users
        user1_id = f"user_{uuid.uuid4().hex[:8]}"
        user1 = User(user_id=user1_id, name=user1_name)
        self.db.create_user(user1)
        
        user2_id = f"user_{uuid.uuid4().hex[:8]}"
        user2 = User(user_id=user2_id, name=user2_name)
        self.db.create_user(user2)
        
        # Create session
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        session = Session(
            session_id=session_id,
            session_type='collaborative',
            user_ids=[user1_id, user2_id]
        )
        self.db.create_session(session)
        
        # Create AI assistants
        assistant1 = MovieAssistant()
        assistant2 = MovieAssistant()
        
        return session, user1, user2, assistant1, assistant2
    
    def add_rating(
        self,
        user_id: str,
        session_id: str,
        movie_index: int,
        is_like: bool
    ) -> bool:
        """Add a movie rating.
        
        Args:
            user_id: User ID
            session_id: Session ID
            movie_index: Movie index in catalog
            is_like: True for like, False for dislike
            
        Returns:
            True if successful
        """
        rating = Rating(
            user_id=user_id,
            movie_index=movie_index,
            rating=1 if is_like else -1,
            session_id=session_id
        )
        
        rating_id = self.db.add_rating(rating)
        return rating_id is not None
    
    def get_user_ratings(self, user_id: str, session_id: str) -> Dict[str, List[int]]:
        """Get user's ratings for current session.
        
        Args:
            user_id: User ID
            session_id: Session ID
            
        Returns:
            Dictionary with 'liked' and 'disliked' movie indices
        """
        liked = self.db.get_liked_movies(user_id, session_id)
        disliked = self.db.get_disliked_movies(user_id, session_id)
        
        return {
            'liked': liked,
            'disliked': disliked
        }
    
    def get_initial_recommendations(
        self,
        preferences: Dict,
        exclude_indices: List[int] = None,
        count: int = 10
    ) -> List[int]:
        """Get initial movie recommendations.
        
        Args:
            preferences: User preferences
            exclude_indices: Movies to exclude
            count: Number of recommendations
            
        Returns:
            List of movie indices
        """
        recommendations = self.engine.get_recommendations_by_preferences(
            preferences,
            top_k=count,
            exclude_indices=exclude_indices or []
        )
        
        return [idx for idx, score in recommendations]
    
    def get_refined_recommendations(
        self,
        preferences: Dict,
        liked_movies: List[int],
        disliked_movies: List[int],
        count: int = 15
    ) -> List[int]:
        """Get refined recommendations based on ratings.
        
        Args:
            preferences: User preferences
            liked_movies: Movies user liked
            disliked_movies: Movies user disliked
            count: Number of recommendations
            
        Returns:
            List of movie indices
        """
        recommendations = self.engine.refine_recommendations(
            preferences,
            liked_movies,
            disliked_movies,
            top_k=count
        )
        
        return [idx for idx, score in recommendations]
    
    def get_collaborative_recommendations(
        self,
        user1_preferences: Dict,
        user2_preferences: Dict,
        user1_liked: List[int],
        user2_liked: List[int],
        user1_disliked: List[int],
        user2_disliked: List[int],
        count: int = 15
    ) -> Dict[str, List[int]]:
        """Get collaborative recommendations (30-30-40 split).
        
        Args:
            user1_preferences: User 1 preferences
            user2_preferences: User 2 preferences
            user1_liked: Movies user 1 liked
            user2_liked: Movies user 2 liked
            user1_disliked: Movies user 1 disliked
            user2_disliked: Movies user 2 disliked
            count: Total number of recommendations
            
        Returns:
            Dictionary with 'user1', 'user2', and 'intersection' movie lists
        """
        results = self.collaborative.get_collaborative_recommendations(
            user1_preferences,
            user2_preferences,
            user1_liked,
            user2_liked,
            user1_disliked,
            user2_disliked,
            total_count=count
        )
        
        return {
            'user1': [idx for idx, score in results['user1']],
            'user2': [idx for idx, score in results['user2']],
            'intersection': [idx for idx, score in results['intersection']]
        }
    
    def update_session_state(self, session_id: str, state: str) -> bool:
        """Update session state.
        
        Args:
            session_id: Session ID
            state: New state ('active', 'completed', 'cancelled')
            
        Returns:
            True if successful
        """
        session = self.db.get_session(session_id)
        if session:
            session.state = state
            return self.db.update_session(session)
        return False

