"""Data models for database."""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import json


@dataclass
class User:
    """User model."""
    user_id: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    preferences: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'preferences': json.dumps(self.preferences)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create from dictionary."""
        return cls(
            user_id=data['user_id'],
            name=data['name'],
            created_at=datetime.fromisoformat(data['created_at']),
            preferences=json.loads(data['preferences']) if isinstance(data['preferences'], str) else data['preferences']
        )


@dataclass
class Rating:
    """Movie rating model."""
    rating_id: Optional[int] = None
    user_id: str = ""
    movie_index: int = 0
    rating: int = 0  # 1 for like, -1 for dislike
    session_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'rating_id': self.rating_id,
            'user_id': self.user_id,
            'movie_index': self.movie_index,
            'rating': self.rating,
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Rating':
        """Create from dictionary."""
        return cls(
            rating_id=data.get('rating_id'),
            user_id=data['user_id'],
            movie_index=data['movie_index'],
            rating=data['rating'],
            session_id=data.get('session_id'),
            created_at=datetime.fromisoformat(data['created_at'])
        )


@dataclass
class Session:
    """Viewing session model."""
    session_id: str
    session_type: str  # 'single' or 'collaborative'
    user_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    state: str = 'active'  # 'active', 'completed', 'cancelled'
    conversation_history: List[Dict] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'session_id': self.session_id,
            'session_type': self.session_type,
            'user_ids': json.dumps(self.user_ids),
            'created_at': self.created_at.isoformat(),
            'state': self.state,
            'conversation_history': json.dumps(self.conversation_history)
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Session':
        """Create from dictionary."""
        return cls(
            session_id=data['session_id'],
            session_type=data['session_type'],
            user_ids=json.loads(data['user_ids']) if isinstance(data['user_ids'], str) else data['user_ids'],
            created_at=datetime.fromisoformat(data['created_at']),
            state=data.get('state', 'active'),
            conversation_history=json.loads(data['conversation_history']) if isinstance(data['conversation_history'], str) else data['conversation_history']
        )
    
    def add_message(self, role: str, content: str, user_id: str = None):
        """Add message to conversation history."""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        })

