"""
Сервис для управления сессиями
"""

from typing import Dict, Optional

class SessionService:
    def __init__(self):
        # В продакшене использовать Redis или БД
        self.sessions: Dict = {}
    
    def create_session(self, session_id: str, mode: str):
        """Создать новую сессию"""
        self.sessions[session_id] = {
            'id': session_id,
            'mode': mode,
            'user1_preferences': None,
            'user2_preferences': None,
            'liked_movies': [],
            'disliked_movies': [],
            'user1_likes': [],
            'user2_likes': []
        }
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Получить сессию по ID"""
        return self.sessions.get(session_id)
    
    def save_preferences(self, session_id: str, user_id: str, preferences: str):
        """Сохранить предпочтения пользователя"""
        if session_id not in self.sessions:
            return
        
        if user_id == 'user1':
            self.sessions[session_id]['user1_preferences'] = preferences
        else:
            self.sessions[session_id]['user2_preferences'] = preferences
    
    def like_movie(self, session_id: str, movie_id: str, user_id: Optional[str]):
        """Лайкнуть фильм"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        session['liked_movies'].append(movie_id)
        
        if user_id == 'user1':
            session['user1_likes'].append(movie_id)
        elif user_id == 'user2':
            session['user2_likes'].append(movie_id)
    
    def dislike_movie(self, session_id: str, movie_id: str, user_id: Optional[str]):
        """Дизлайкнуть фильм"""
        if session_id not in self.sessions:
            return
        
        self.sessions[session_id]['disliked_movies'].append(movie_id)
    
    def check_status(self, session_id: str) -> Dict:
        """Проверить статус сессии"""
        if session_id not in self.sessions:
            return {'ready': False, 'both_ready': False}
        
        session = self.sessions[session_id]
        
        if session['mode'] == 'single':
            ready = session['user1_preferences'] is not None
            return {'ready': ready, 'both_ready': ready}
        
        # Duo режим
        user1_ready = session['user1_preferences'] is not None
        user2_ready = session['user2_preferences'] is not None
        both_ready = user1_ready and user2_ready
        
        return {'ready': user1_ready, 'both_ready': both_ready}

