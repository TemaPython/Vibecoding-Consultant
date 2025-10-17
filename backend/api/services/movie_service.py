"""
Сервис для работы с фильмами
"""

from typing import List, Dict
import random

class MovieService:
    def __init__(self):
        # В продакшене подключить базу данных
        self.movies_db = self._init_mock_movies()
    
    def _init_mock_movies(self) -> List[Dict]:
        """Инициализация mock данных (заменить на реальную БД)"""
        return [
            {
                'id': '1',
                'title': 'Драйв',
                'poster': 'https://via.placeholder.com/300x450/ec4899/ffffff?text=Drive',
                'rating': 7.8,
                'year': 2011,
                'actors': ['Райан Гослинг', 'Кэри Маллиган'],
                'description': 'Таинственный голливудский каскадёр и автомеханик помогает своим клиентам скрыться от полиции после совершения преступления.',
                'okkoUrl': 'https://okko.tv/movie/drive',
                'genre': ['драма', 'триллер']
            },
            {
                'id': '2',
                'title': 'Ла-Ла Ленд',
                'poster': 'https://via.placeholder.com/300x450/f472b6/ffffff?text=La+La+Land',
                'rating': 8.0,
                'year': 2016,
                'actors': ['Райан Гослинг', 'Эмма Стоун'],
                'description': 'Себастьян и Миа влюблены друг в друга, но любовь в мире грёз стоит недёшево.',
                'okkoUrl': 'https://okko.tv/movie/la-la-land',
                'genre': ['мелодрама', 'мюзикл']
            },
            {
                'id': '3',
                'title': 'Начало',
                'poster': 'https://via.placeholder.com/300x450/db2777/ffffff?text=Inception',
                'rating': 8.8,
                'year': 2010,
                'actors': ['Леонардо ДиКаприо', 'Марион Котийяр'],
                'description': 'Специалист по краже корпоративных секретов из подсознания получает задание внедрить идею в чужой разум.',
                'okkoUrl': 'https://okko.tv/movie/inception',
                'genre': ['фантастика', 'триллер']
            },
            {
                'id': '4',
                'title': 'Интерстеллар',
                'poster': 'https://via.placeholder.com/300x450/f9a8d4/ffffff?text=Interstellar',
                'rating': 8.6,
                'year': 2014,
                'actors': ['Мэттью МакКонахи', 'Энн Хэтэуэй'],
                'description': 'Когда засуха приводит человечество к продовольственному кризису, команда исследователей отправляется сквозь червоточину в поисках нового дома.',
                'okkoUrl': 'https://okko.tv/movie/interstellar',
                'genre': ['фантастика', 'драма']
            },
            {
                'id': '5',
                'title': 'Оно',
                'poster': 'https://via.placeholder.com/300x450/ec4899/ffffff?text=IT',
                'rating': 7.3,
                'year': 2017,
                'actors': ['Билл Скарсгард', 'Джейден Либерер'],
                'description': 'Семеро подростков объединяются, чтобы уничтожить сверхъестественное существо, терроризирующее их город.',
                'okkoUrl': 'https://okko.tv/movie/it',
                'genre': ['ужасы', 'триллер']
            }
        ]
    
    async def get_recommendations(self, session: Dict) -> List[Dict]:
        """
        Получить рекомендации на основе предпочтений
        TODO: Интегрировать с ИИ для улучшения рекомендаций
        """
        # Пока возвращаем случайную выборку
        # В продакшене здесь должна быть логика фильтрации по предпочтениям
        recommendations = random.sample(self.movies_db, min(len(self.movies_db), 20))
        
        return recommendations
    
    def get_final_movies(self, session: Dict) -> List[Dict]:
        """Получить финальную подборку лайкнутых фильмов"""
        liked_ids = session['liked_movies']
        
        if session['mode'] == 'duo':
            # Для duo режима - только взаимные лайки
            user1_likes = set(session['user1_likes'])
            user2_likes = set(session['user2_likes'])
            mutual_likes = user1_likes.intersection(user2_likes)
            liked_ids = list(mutual_likes)
        
        # Получаем фильмы по ID
        final_movies = [
            movie for movie in self.movies_db
            if movie['id'] in liked_ids
        ]
        
        return final_movies

