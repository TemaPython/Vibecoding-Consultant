<<<<<<< HEAD
"""
Дайкинчик - Устаревший файл

⚠️ ВНИМАНИЕ: Этот файл больше не используется!

Новая структура проекта:
- Frontend: ./frontend/ (Angular приложение)
- Backend: ./backend/ (FastAPI сервер)

Для запуска проекта см. QUICK_START.md
"""

def main():
    print("=" * 60)
    print("🎬 Добро пожаловать в Дайкинчик!")
    print("=" * 60)
    print()
    print("⚠️  Этот файл устарел и больше не используется.")
    print()
    print("📂 Новая структура проекта:")
    print("   - Frontend (Angular): ./frontend/")
    print("   - Backend (FastAPI):  ./backend/")
    print()
    print("🚀 Быстрый старт:")
    print()
    print("   1. Backend:")
    print("      cd backend")
    print("      pip install -r requirements.txt")
    print("      python main.py")
    print()
    print("   2. Frontend (в новом терминале):")
    print("      cd frontend")
    print("      npm install")
    print("      npm start")
    print()
    print("📖 Подробнее см. QUICK_START.md")
    print()
    print("=" * 60)
    print("💖 Команда: Артём, Катя, Елисей")
    print("🏆 Okko Vibecoding Hackathon 2025")
    print("=" * 60)
=======
"""AI Movie Recommendation Assistant - Main Entry Point."""
import sys
from catalog.catalog_loader import CatalogLoader
from embeddings.embedding_manager import EmbeddingManager
from embeddings.vector_store import VectorStore
from database.db_manager import DatabaseManager
from recommender.recommendation_engine import RecommendationEngine
from cli.console_ui import ConsoleUI
from cli.session_manager import SessionManager
import config


def initialize_system():
    """Initialize all system components.
    
    Returns:
        Tuple of (catalog, engine, session_manager, ui)
    """
    print("[i] Инициализация системы...")
    
    # Check API key
    if not config.OPENAI_API_KEY:
        print("\n❌ Ошибка: OpenAI API ключ не найден!")
        print("Создайте файл .env и добавьте: OPENAI_API_KEY=your_key_here")
        sys.exit(1)
    
    # Initialize catalog
    print("[i] Загрузка каталога фильмов...")
    catalog = CatalogLoader()
    catalog.load_catalog()
    
    # Initialize embedding manager and vector store
    print("[i] Инициализация системы embeddings...")
    embedding_manager = EmbeddingManager()
    vector_store = VectorStore()
    
    # Initialize database
    db_manager = DatabaseManager()
    
    # Initialize recommendation engine
    engine = RecommendationEngine(catalog, embedding_manager, vector_store)
    
    # Load or generate embeddings
    print("[i] Загрузка embeddings...")
    engine.initialize_embeddings()
    
    # Initialize session manager
    session_manager = SessionManager(db_manager, engine)
    
    # Initialize UI
    ui = ConsoleUI(catalog)
    
    print("[+] Система готова!\n")
    
    return catalog, engine, session_manager, ui


def run_single_session(session_manager: SessionManager, ui: ConsoleUI):
    """Run single user session.
    
    Args:
        session_manager: Session manager instance
        ui: Console UI instance
    """
    # Get user name
    user_name = ui.get_user_name()
    
    # Create session
    session, user, assistant = session_manager.create_single_session(user_name)
    
    # Start conversation
    ui.print_assistant_message(
        assistant.get_initial_question(user_name),
        "Ассистент"
    )
    
    # Conversation loop
    for turn in range(config.MAX_CONVERSATION_TURNS):
        user_input = ui.get_user_input(f"{user_name}: ")
        
        if not user_input:
            continue
        
        response = assistant.send_message(user_input, user_name)
        ui.print_assistant_message(response, "Ассистент")
    
    # Extract preferences
    print("\n[i] Анализирую ваши предпочтения...")
    preferences = assistant.extract_preferences()
    
    # Get initial recommendations
    print("[i] Подбираю фильмы...")
    movie_indices = session_manager.get_initial_recommendations(
        preferences,
        count=config.INITIAL_RECOMMENDATIONS_COUNT
    )
    
    # Show movies and get ratings
    ui.print_movie_list(movie_indices, "Предлагаю посмотреть эти фильмы")
    ratings = ui.rate_movies(movie_indices)
    
    # Save ratings
    liked_movies = []
    disliked_movies = []
    
    for movie_idx, is_like in ratings.items():
        session_manager.add_rating(user.user_id, session.session_id, movie_idx, is_like)
        if is_like:
            liked_movies.append(movie_idx)
        else:
            disliked_movies.append(movie_idx)
    
    # Get final recommendations
    print("\n[i] Формирую финальную подборку...")
    final_movies = session_manager.get_refined_recommendations(
        preferences,
        liked_movies,
        disliked_movies,
        count=config.FINAL_RECOMMENDATIONS_COUNT
    )
    
    # Show final recommendations
    ui.print_single_final_recommendations(final_movies)
    
    # Complete session
    session_manager.update_session_state(session.session_id, 'completed')


def run_collaborative_session(session_manager: SessionManager, ui: ConsoleUI):
    """Run collaborative session for two users.
    
    Args:
        session_manager: Session manager instance
        ui: Console UI instance
    """
    # Get user names
    user1_name = ui.get_user_name("Введите имя первого пользователя: ")
    user2_name = ui.get_user_name("Введите имя второго пользователя: ")
    
    # Create session
    session, user1, user2, assistant1, assistant2 = session_manager.create_collaborative_session(
        user1_name, user2_name
    )
    
    ui.print_info(f"Сессия создана для {user1_name} и {user2_name}")
    
    # User 1 conversation
    ui.print_header(f"Опрос: {user1_name}")
    ui.print_assistant_message(
        assistant1.get_initial_question(user1_name, is_collaborative=True),
        "Ассистент"
    )
    
    for turn in range(config.MAX_CONVERSATION_TURNS):
        user_input = ui.get_user_input(f"{user1_name}: ")
        if not user_input:
            continue
        response = assistant1.send_message(user_input, user1_name)
        ui.print_assistant_message(response, "Ассистент")
    
    # Ask follow-up about genres for user 1
    if any('актер' in msg['content'].lower() or 'actor' in msg['content'].lower() 
           for msg in assistant1.conversation_history if msg['role'] == 'user'):
        follow_up = assistant1.ask_follow_up_about_genres("этими актерами")
        ui.print_assistant_message(follow_up, "Ассистент")
        user_input = ui.get_user_input(f"{user1_name}: ")
        if user_input:
            assistant1.send_message(user_input, user1_name)
    
    preferences1 = assistant1.extract_preferences()
    
    # User 2 conversation
    ui.print_header(f"Опрос: {user2_name}")
    ui.print_assistant_message(
        assistant2.get_initial_question(user2_name, is_collaborative=True),
        "Ассистент"
    )
    
    for turn in range(config.MAX_CONVERSATION_TURNS):
        user_input = ui.get_user_input(f"{user2_name}: ")
        if not user_input:
            continue
        response = assistant2.send_message(user_input, user2_name)
        ui.print_assistant_message(response, "Ассистент")
    
    # Ask follow-up about genres for user 2
    if any('актер' in msg['content'].lower() or 'actor' in msg['content'].lower() 
           for msg in assistant2.conversation_history if msg['role'] == 'user'):
        follow_up = assistant2.ask_follow_up_about_genres("этими актерами")
        ui.print_assistant_message(follow_up, "Ассистент")
        user_input = ui.get_user_input(f"{user2_name}: ")
        if user_input:
            assistant2.send_message(user_input, user2_name)
    
    preferences2 = assistant2.extract_preferences()
    
    # Get recommendations for both users
    print("\n[i] Подбираю фильмы для оценки...")
    
    # Get movies for user 1 to rate
    movies1 = session_manager.get_initial_recommendations(
        preferences1,
        count=config.INITIAL_RECOMMENDATIONS_COUNT
    )
    
    ui.print_header(f"Оценка фильмов: {user1_name}")
    ui.print_movie_list(movies1, f"Фильмы для {user1_name}")
    ratings1 = ui.rate_movies(movies1)
    
    liked1 = []
    disliked1 = []
    for movie_idx, is_like in ratings1.items():
        session_manager.add_rating(user1.user_id, session.session_id, movie_idx, is_like)
        if is_like:
            liked1.append(movie_idx)
        else:
            disliked1.append(movie_idx)
    
    # Get movies for user 2 to rate
    movies2 = session_manager.get_initial_recommendations(
        preferences2,
        count=config.INITIAL_RECOMMENDATIONS_COUNT
    )
    
    ui.print_header(f"Оценка фильмов: {user2_name}")
    ui.print_movie_list(movies2, f"Фильмы для {user2_name}")
    ratings2 = ui.rate_movies(movies2)
    
    liked2 = []
    disliked2 = []
    for movie_idx, is_like in ratings2.items():
        session_manager.add_rating(user2.user_id, session.session_id, movie_idx, is_like)
        if is_like:
            liked2.append(movie_idx)
        else:
            disliked2.append(movie_idx)
    
    # Get final collaborative recommendations
    print("\n[i] Формирую финальную подборку с учетом пересечений...")
    final_recs = session_manager.get_collaborative_recommendations(
        preferences1,
        preferences2,
        liked1,
        liked2,
        disliked1,
        disliked2,
        count=config.FINAL_RECOMMENDATIONS_COUNT
    )
    
    # Show final recommendations
    ui.print_final_recommendations(
        final_recs['user1'],
        final_recs['user2'],
        final_recs['intersection'],
        user1_name,
        user2_name
    )
    
    # Complete session
    session_manager.update_session_state(session.session_id, 'completed')


def main():
    """Main entry point."""
    try:
        # Initialize system
        catalog, engine, session_manager, ui = initialize_system()
        
        # Welcome message
        ui.print_welcome()
        
        # Get session type
        session_type = ui.get_session_type()
        
        # Run appropriate session
        if session_type == 'single':
            run_single_session(session_manager, ui)
        else:
            run_collaborative_session(session_manager, ui)
        
    except KeyboardInterrupt:
        print("\n\n[i] Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

>>>>>>> 8f0c73f5ef4a36f855ace42799739395e1ba72df

if __name__ == "__main__":
    main()


