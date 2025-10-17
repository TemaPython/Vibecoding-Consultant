"""Configuration file for AI Movie Assistant."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # or "text-embedding-3-large"

# Database Configuration
DATABASE_PATH = "data/users.db"
EMBEDDINGS_CACHE_PATH = "data/embeddings_cache.pkl"
SESSIONS_DIR = "data/sessions"

# Catalog Configuration
CATALOG_PATH = "catalog_okko.parquet"

# Recommendation Engine Configuration
RECOMMENDATION_SPLIT = {
    "user1_preference": 0.30,  # 30% фильмы для пользователя 1
    "user2_preference": 0.30,  # 30% фильмы для пользователя 2
    "intersection": 0.40       # 40% пересечение интересов
}

# Number of movies to recommend
INITIAL_RECOMMENDATIONS_COUNT = 10  # Фильмы для первичной оценки
FINAL_RECOMMENDATIONS_COUNT = 15    # Итоговая подборка

# Embedding Configuration
EMBEDDING_DIMENSION = 1536  # для text-embedding-3-small
SIMILARITY_THRESHOLD = 0.7  # Минимальное сходство для пересечений

# AI Assistant Configuration
MAX_CONVERSATION_TURNS = 5  # Максимум обменов в диалоге
TEMPERATURE = 0.7           # Креативность ассистента

# Console UI Configuration
CONSOLE_WIDTH = 80

