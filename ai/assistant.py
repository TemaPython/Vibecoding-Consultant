"""AI assistant for movie recommendations."""
import json
from typing import List, Dict, Optional
from openai import OpenAI
import config
from ai import prompt_templates


class MovieAssistant:
    """AI assistant for conversing with users about movie preferences."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize assistant.
        
        Args:
            api_key: OpenAI API key
            model: Model name to use
        """
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model or config.OPENAI_MODEL
        
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history: List[Dict] = []
        
        # Initialize with system prompt
        self.conversation_history.append({
            "role": "system",
            "content": prompt_templates.SYSTEM_PROMPT
        })
    
    def send_message(self, user_message: str, user_name: str = "User") -> str:
        """Send a message and get response.
        
        Args:
            user_message: User's message
            user_name: User's name for context
            
        Returns:
            Assistant's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=config.TEMPERATURE
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            print(f"[!] Error getting AI response: {e}")
            return "Извините, произошла ошибка. Попробуйте еще раз."
    
    def get_initial_question(self, user_name: str = "User", is_collaborative: bool = False) -> str:
        """Get initial question to start conversation.
        
        Args:
            user_name: User's name
            is_collaborative: Whether this is a collaborative session
            
        Returns:
            Initial question
        """
        if is_collaborative:
            return f"Привет, {user_name}! Расскажи, какой актер, режиссер или жанр тебе интересен?"
        else:
            return f"Привет, {user_name}! Помогу тебе найти фильм для просмотра. Расскажи, что тебе интересно?"
    
    def ask_follow_up_about_genres(self, subject: str) -> str:
        """Ask follow-up question about genres.
        
        Args:
            subject: Actor, director, or other subject mentioned
            
        Returns:
            Follow-up question
        """
        return prompt_templates.FOLLOW_UP_GENRE.format(subject=subject)
    
    def extract_preferences(self) -> Dict:
        """Extract user preferences from conversation history.
        
        Returns:
            Dictionary with extracted preferences
        """
        # Format conversation history
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history 
            if msg['role'] != 'system'
        ])
        
        prompt = prompt_templates.EXTRACT_PREFERENCES_PROMPT.format(
            conversation_history=conversation_text
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts information and returns JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            preferences_text = response.choices[0].message.content
            
            # Try to parse JSON
            # Remove markdown code blocks if present
            if "```json" in preferences_text:
                preferences_text = preferences_text.split("```json")[1].split("```")[0]
            elif "```" in preferences_text:
                preferences_text = preferences_text.split("```")[1].split("```")[0]
            
            preferences = json.loads(preferences_text.strip())
            return preferences
            
        except Exception as e:
            print(f"[!] Error extracting preferences: {e}")
            return {}
    
    def analyze_ratings(self, liked_movies: List[Dict], disliked_movies: List[Dict]) -> str:
        """Analyze user's movie ratings to understand patterns.
        
        Args:
            liked_movies: List of movies user liked
            disliked_movies: List of movies user disliked
            
        Returns:
            Analysis text
        """
        # Format movie lists
        liked_text = "\n".join([
            f"- {m.get('serial_name', 'Unknown')} ({m.get('genres', 'N/A')})"
            for m in liked_movies
        ])
        
        disliked_text = "\n".join([
            f"- {m.get('serial_name', 'Unknown')} ({m.get('genres', 'N/A')})"
            for m in disliked_movies
        ])
        
        prompt = prompt_templates.ANALYZE_RATINGS_PROMPT.format(
            liked_movies=liked_text or "Нет",
            disliked_movies=disliked_text or "Нет"
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a movie preference analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"[!] Error analyzing ratings: {e}")
            return ""
    
    def create_query_embedding_text(self, preferences: Dict) -> str:
        """Create text for embedding from user preferences.
        
        Args:
            preferences: Dictionary with user preferences
            
        Returns:
            Text representation of preferences
        """
        parts = []
        
        if preferences.get('actors'):
            actors = ', '.join(preferences['actors']) if isinstance(preferences['actors'], list) else preferences['actors']
            parts.append(f"Актеры: {actors}")
        
        if preferences.get('directors'):
            directors = ', '.join(preferences['directors']) if isinstance(preferences['directors'], list) else preferences['directors']
            parts.append(f"Режиссеры: {directors}")
        
        if preferences.get('genres'):
            genres = ', '.join(preferences['genres']) if isinstance(preferences['genres'], list) else preferences['genres']
            parts.append(f"Жанры: {genres}")
        
        if preferences.get('mood'):
            parts.append(f"Настроение: {preferences['mood']}")
        
        if preferences.get('themes'):
            themes = ', '.join(preferences['themes']) if isinstance(preferences['themes'], list) else preferences['themes']
            parts.append(f"Темы: {themes}")
        
        if preferences.get('era'):
            parts.append(f"Эпоха: {preferences['era']}")
        
        if preferences.get('other'):
            parts.append(f"{preferences['other']}")
        
        return ". ".join(parts) if parts else "Фильмы"
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = [
            {
                "role": "system",
                "content": prompt_templates.SYSTEM_PROMPT
            }
        ]
    
    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history.
        
        Returns:
            List of conversation messages
        """
        return self.conversation_history.copy()

