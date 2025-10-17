"""
Сервис для работы с ИИ
"""

import random

class AIService:
    def __init__(self):
        # TODO: Подключить OpenAI/Claude API
        self.conversations = {}
    
    async def chat(self, session_id: str, message: str) -> str:
        """
        Чат с ИИ для уточнения предпочтений
        TODO: Интегрировать с реальным ИИ (OpenAI, Claude, etc.)
        """
        
        # Mock ответы для демонстрации
        responses = [
            "А, понял! Скажите, вам нравятся фильмы с глубоким смыслом или просто развлечься хотите?",
            "Отлично! А как насчёт актёров? Есть любимые?",
            "Понятно! Предпочитаете новинки последних лет или классику?",
            "Хорошо, я понял ваши предпочтения. Сейчас подберу идеальные фильмы!",
            "Ага, интересно! А настроение какое - расслабиться или взбодриться?",
            "Супер! Думаю, у меня есть для вас отличные варианты. Готовы смотреть?",
            "Замечательно! Ещё один вопрос: хотите что-то атмосферное или динамичное?"
        ]
        
        # Сохраняем историю разговора
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            'role': 'user',
            'content': message
        })
        
        # Генерируем ответ
        # В продакшене здесь должен быть вызов API ИИ
        response = random.choice(responses)
        
        self.conversations[session_id].append({
            'role': 'assistant',
            'content': response
        })
        
        return response

