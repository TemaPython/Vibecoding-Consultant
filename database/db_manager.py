"""Database manager for SQLite operations."""
import sqlite3
from typing import List, Optional, Dict
from pathlib import Path
import config
from database.models import User, Rating, Session


class DatabaseManager:
    """Manages SQLite database operations."""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path or config.DATABASE_PATH
        self._ensure_database_exists()
        self._create_tables()
    
    def _ensure_database_exists(self):
        """Ensure database directory exists."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                preferences TEXT
            )
        ''')
        
        # Ratings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                movie_index INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                session_id TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                session_type TEXT NOT NULL,
                user_ids TEXT NOT NULL,
                created_at TEXT NOT NULL,
                state TEXT NOT NULL,
                conversation_history TEXT
            )
        ''')
        
        # Create indices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ratings_user ON ratings(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ratings_movie ON ratings(movie_index)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ratings_session ON ratings(session_id)')
        
        conn.commit()
        conn.close()
    
    # User operations
    def create_user(self, user: User) -> bool:
        """Create a new user.
        
        Args:
            user: User object
            
        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            data = user.to_dict()
            cursor.execute('''
                INSERT INTO users (user_id, name, created_at, preferences)
                VALUES (?, ?, ?, ?)
            ''', (data['user_id'], data['name'], data['created_at'], data['preferences']))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            print(f"[!] User {user.user_id} already exists")
            return False
        except Exception as e:
            print(f"[!] Error creating user: {e}")
            return False
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return User.from_dict(dict(row))
            return None
            
        except Exception as e:
            print(f"[!] Error getting user: {e}")
            return None
    
    def update_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Update user preferences.
        
        Args:
            user_id: User ID
            preferences: New preferences dictionary
            
        Returns:
            True if successful
        """
        try:
            import json
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET preferences = ? WHERE user_id = ?
            ''', (json.dumps(preferences), user_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[!] Error updating preferences: {e}")
            return False
    
    # Rating operations
    def add_rating(self, rating: Rating) -> Optional[int]:
        """Add a movie rating.
        
        Args:
            rating: Rating object
            
        Returns:
            Rating ID or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            data = rating.to_dict()
            cursor.execute('''
                INSERT INTO ratings (user_id, movie_index, rating, session_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['user_id'], data['movie_index'], data['rating'], 
                  data['session_id'], data['created_at']))
            
            rating_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return rating_id
            
        except Exception as e:
            print(f"[!] Error adding rating: {e}")
            return None
    
    def get_user_ratings(self, user_id: str, session_id: str = None) -> List[Rating]:
        """Get all ratings by a user.
        
        Args:
            user_id: User ID
            session_id: Optional session ID to filter by
            
        Returns:
            List of Rating objects
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if session_id:
                cursor.execute('''
                    SELECT * FROM ratings 
                    WHERE user_id = ? AND session_id = ?
                    ORDER BY created_at DESC
                ''', (user_id, session_id))
            else:
                cursor.execute('''
                    SELECT * FROM ratings 
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                ''', (user_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [Rating.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            print(f"[!] Error getting ratings: {e}")
            return []
    
    def get_liked_movies(self, user_id: str, session_id: str = None) -> List[int]:
        """Get movie indices that user liked.
        
        Args:
            user_id: User ID
            session_id: Optional session ID to filter by
            
        Returns:
            List of movie indices
        """
        ratings = self.get_user_ratings(user_id, session_id)
        return [r.movie_index for r in ratings if r.rating > 0]
    
    def get_disliked_movies(self, user_id: str, session_id: str = None) -> List[int]:
        """Get movie indices that user disliked.
        
        Args:
            user_id: User ID
            session_id: Optional session ID to filter by
            
        Returns:
            List of movie indices
        """
        ratings = self.get_user_ratings(user_id, session_id)
        return [r.movie_index for r in ratings if r.rating < 0]
    
    # Session operations
    def create_session(self, session: Session) -> bool:
        """Create a new session.
        
        Args:
            session: Session object
            
        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            data = session.to_dict()
            cursor.execute('''
                INSERT INTO sessions (session_id, session_type, user_ids, created_at, state, conversation_history)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['session_id'], data['session_type'], data['user_ids'],
                  data['created_at'], data['state'], data['conversation_history']))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[!] Error creating session: {e}")
            return False
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session object or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM sessions WHERE session_id = ?', (session_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return Session.from_dict(dict(row))
            return None
            
        except Exception as e:
            print(f"[!] Error getting session: {e}")
            return None
    
    def update_session(self, session: Session) -> bool:
        """Update session data.
        
        Args:
            session: Session object with updated data
            
        Returns:
            True if successful
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            data = session.to_dict()
            cursor.execute('''
                UPDATE sessions 
                SET state = ?, conversation_history = ?
                WHERE session_id = ?
            ''', (data['state'], data['conversation_history'], data['session_id']))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[!] Error updating session: {e}")
            return False

