"""Console UI for movie recommendation assistant."""
from typing import Dict, List, Optional
import config
from catalog.catalog_loader import CatalogLoader


class ConsoleUI:
    """Console user interface for the movie assistant."""
    
    def __init__(self, catalog: CatalogLoader):
        """Initialize console UI.
        
        Args:
            catalog: Catalog loader instance
        """
        self.catalog = catalog
        self.width = config.CONSOLE_WIDTH
    
    def print_header(self, text: str):
        """Print a header."""
        print("\n" + "=" * self.width)
        print(text.center(self.width))
        print("=" * self.width + "\n")
    
    def print_separator(self):
        """Print a separator line."""
        print("-" * self.width)
    
    def print_welcome(self):
        """Print welcome message."""
        self.print_header("AI Movie Recommendation Assistant")
        print("Добро пожаловать в ассистент по подбору фильмов!")
        print("Я помогу вам найти идеальный фильм для просмотра.\n")
    
    def get_session_type(self) -> str:
        """Ask user for session type.
        
        Returns:
            'single' or 'collaborative'
        """
        print("Выберите режим работы:")
        print("  1. Одиночный просмотр")
        print("  2. Совместный просмотр (2 человека)")
        
        while True:
            choice = input("\nВаш выбор (1 или 2): ").strip()
            if choice == '1':
                return 'single'
            elif choice == '2':
                return 'collaborative'
            else:
                print("Пожалуйста, введите 1 или 2")
    
    def get_user_name(self, prompt: str = "Введите ваше имя: ") -> str:
        """Get user name.
        
        Args:
            prompt: Prompt text
            
        Returns:
            User name
        """
        while True:
            name = input(prompt).strip()
            if name:
                return name
            print("Имя не может быть пустым")
    
    def print_assistant_message(self, message: str, user_name: str = "Ассистент"):
        """Print assistant message.
        
        Args:
            message: Message text
            user_name: Name to show
        """
        print(f"\n💬 {user_name}: {message}")
    
    def get_user_input(self, prompt: str = "Вы: ") -> str:
        """Get user input.
        
        Args:
            prompt: Input prompt
            
        Returns:
            User input
        """
        return input(f"\n{prompt}").strip()
    
    def print_movie_list(self, movie_indices: List[int], title: str = "Рекомендации"):
        """Print list of movies.
        
        Args:
            movie_indices: List of movie indices
            title: Title for the list
        """
        self.print_separator()
        print(f"\n{title}:\n")
        
        for i, idx in enumerate(movie_indices, 1):
            movie = self.catalog.get_movie_by_index(idx)
            if movie:
                self._print_movie_short(i, movie)
        
        self.print_separator()
    
    def _print_movie_short(self, number: int, movie: Dict):
        """Print short movie info.
        
        Args:
            number: Movie number in list
            movie: Movie dictionary
        """
        name = movie.get('serial_name', 'Unknown')
        genres = movie.get('genres', 'N/A')
        year = movie.get('release_date', 'N/A')
        
        print(f"{number}. {name}")
        print(f"   Жанры: {genres}")
        print(f"   Год: {year}")
        print()
    
    def print_movie_detailed(self, movie: Dict):
        """Print detailed movie info.
        
        Args:
            movie: Movie dictionary
        """
        print(f"\n📽️  {movie.get('serial_name', 'Unknown')}")
        print(f"   Жанры: {movie.get('genres', 'N/A')}")
        print(f"   Режиссер: {movie.get('director', 'N/A')}")
        print(f"   Актеры: {movie.get('actors', 'N/A')[:100]}...")
        print(f"   Страна: {movie.get('country', 'N/A')}")
        print(f"   Год: {movie.get('release_date', 'N/A')}")
        print(f"   Возраст: {movie.get('age_rating', 'N/A')}+")
        
        description = movie.get('description', '')
        if description:
            desc_short = description[:200] + "..." if len(description) > 200 else description
            print(f"   Описание: {desc_short}")
        
        print(f"   URL: {movie.get('url', 'N/A')}")
        print()
    
    def rate_movies(self, movie_indices: List[int]) -> Dict[int, bool]:
        """Ask user to rate movies.
        
        Args:
            movie_indices: List of movie indices to rate
            
        Returns:
            Dictionary mapping movie_index -> is_liked (True/False)
        """
        ratings = {}
        
        print("\nОцените каждый фильм:")
        print("  💚 - нравится (введите '+' или 'like')")
        print("  👎 - не нравится (введите '-' или 'dislike')")
        print("  ⏭️  - пропустить (нажмите Enter)\n")
        
        for idx in movie_indices:
            movie = self.catalog.get_movie_by_index(idx)
            if not movie:
                continue
            
            self._print_movie_short("", movie)
            
            while True:
                rating = input("Ваша оценка: ").strip().lower()
                
                if rating in ['+', 'like', 'l', 'да', 'нравится']:
                    ratings[idx] = True
                    print("💚 Добавлено в понравившиеся\n")
                    break
                elif rating in ['-', 'dislike', 'd', 'нет', 'не нравится']:
                    ratings[idx] = False
                    print("👎 Добавлено в непонравившиеся\n")
                    break
                elif rating == '':
                    print("⏭️  Пропущено\n")
                    break
                else:
                    print("Пожалуйста, введите '+', '-' или нажмите Enter для пропуска")
        
        return ratings
    
    def print_final_recommendations(
        self,
        user1_movies: List[int],
        user2_movies: List[int],
        intersection_movies: List[int],
        user1_name: str,
        user2_name: str
    ):
        """Print final collaborative recommendations.
        
        Args:
            user1_movies: Movies for user 1
            user2_movies: Movies for user 2
            intersection_movies: Movies for both users
            user1_name: User 1 name
            user2_name: User 2 name
        """
        self.print_header("Финальная подборка")
        
        if user1_movies:
            print(f"\n🎬 Специально для {user1_name} (30%):")
            print()
            for i, idx in enumerate(user1_movies, 1):
                movie = self.catalog.get_movie_by_index(idx)
                if movie:
                    self._print_movie_short(i, movie)
        
        if user2_movies:
            print(f"\n🎬 Специально для {user2_name} (30%):")
            print()
            for i, idx in enumerate(user2_movies, 1):
                movie = self.catalog.get_movie_by_index(idx)
                if movie:
                    self._print_movie_short(i, movie)
        
        if intersection_movies:
            print(f"\n🎬 Для совместного просмотра (40%):")
            print()
            for i, idx in enumerate(intersection_movies, 1):
                movie = self.catalog.get_movie_by_index(idx)
                if movie:
                    self._print_movie_short(i, movie)
        
        self.print_separator()
        print("\n✨ Приятного просмотра! ✨\n")
    
    def print_single_final_recommendations(self, movie_indices: List[int]):
        """Print final recommendations for single user.
        
        Args:
            movie_indices: List of movie indices
        """
        self.print_header("Ваша персональная подборка")
        
        for i, idx in enumerate(movie_indices, 1):
            movie = self.catalog.get_movie_by_index(idx)
            if movie:
                self.print_movie_detailed(movie)
        
        self.print_separator()
        print("\n✨ Приятного просмотра! ✨\n")
    
    def confirm_action(self, prompt: str) -> bool:
        """Ask user to confirm an action.
        
        Args:
            prompt: Confirmation prompt
            
        Returns:
            True if confirmed
        """
        response = input(f"{prompt} (да/нет): ").strip().lower()
        return response in ['да', 'yes', 'y', 'д', '+']
    
    def print_error(self, message: str):
        """Print error message.
        
        Args:
            message: Error message
        """
        print(f"\n❌ Ошибка: {message}\n")
    
    def print_info(self, message: str):
        """Print info message.
        
        Args:
            message: Info message
        """
        print(f"\nℹ️  {message}\n")
    
    def print_success(self, message: str):
        """Print success message.
        
        Args:
            message: Success message
        """
        print(f"\n✅ {message}\n")

