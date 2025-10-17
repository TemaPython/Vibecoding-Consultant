# Структура проекта Дайкинчик

## Обзор

Дайкинчик - это приложение для умного подбора фильмов с использованием ИИ, разработанное для платформы Okko.

## Структура директорий

```
vibecoding 17.10.25/
├── frontend/                 # Angular приложение
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/  # UI компоненты
│   │   │   ├── models/      # TypeScript модели
│   │   │   ├── services/    # Сервисы (API, State)
│   │   │   └── ...
│   │   ├── assets/          # Статические файлы
│   │   ├── styles.scss      # Глобальные стили
│   │   └── index.html
│   ├── package.json
│   ├── angular.json
│   └── README.md
│
├── backend/                  # FastAPI приложение (Python)
│   ├── api/
│   │   ├── endpoints/       # API роуты
│   │   ├── models/          # Pydantic модели
│   │   └── services/        # Бизнес-логика
│   ├── database/            # База данных
│   ├── ai/                  # ИИ интеграция
│   ├── main.py              # Точка входа
│   └── requirements.txt
│
├── main.py                   # Текущий файл (для миграции)
├── main.html                 # Текущий файл (для миграции)
└── README.md                 # Главный README
```

## Компоненты Frontend

### 1. Welcome Component (Начальный экран)
- Выбор режима: один или вдвоём
- Создание сессии
- Генерация реферальной ссылки (для режима "вдвоём")

### 2. Preferences Input Component (Ввод предпочтений)
- Текстовое поле для ввода предпочтений
- Подсказки и примеры
- Определение неясных запросов
- Ожидание второго пользователя (duo режим)

### 3. AI Dialog Component (Диалог с ИИ)
- Чат-интерфейс
- Уточняющие вопросы
- Анимация печати
- Сбор детальных предпочтений

### 4. Movie Card Component (Карточка фильма)
- Swipe анимация
- Touch/Mouse поддержка
- Лайк/Дизлайк кнопки
- Информация о фильме
- Ссылка на Okko
- Прогресс бар

### 5. Final Selection Component (Финальная подборка)
- Список лайкнутых фильмов
- Грид с карточками
- Кнопки действий
- Пустое состояние (если нет совпадений)

### 6. Loading Component (Загрузка)
- Анимированный спиннер
- Кастомное сообщение

## Сервисы

### API Service
Отвечает за взаимодействие с бэкендом:
- `createSession()` - создание сессии
- `submitPreferences()` - отправка предпочтений
- `getMovieRecommendations()` - получение рекомендаций
- `likeMovie()` / `dislikeMovie()` - оценка фильмов
- `getFinalSelection()` - финальная подборка
- `sendAIMessage()` - чат с ИИ
- `checkSessionStatus()` - проверка статуса (duo режим)

### State Service
Управление глобальным состоянием приложения:
- Текущая сессия
- Список фильмов
- Индекс текущего фильма
- Лайкнутые фильмы
- Состояние загрузки

## Модели данных

### Movie
```typescript
{
  id: string;
  title: string;
  poster: string;
  rating: number;
  year: number;
  actors: string[];
  description: string;
  okkoUrl: string;
  genre?: string[];
}
```

### Session
```typescript
{
  sessionId: string;
  mode: 'single' | 'duo';
  user1Preferences?: UserPreferences;
  user2Preferences?: UserPreferences;
  likedMovies: string[];
  dislikedMovies: string[];
  user1Likes?: string[];
  user2Likes?: string[];
}
```

## Особенности реализации

### Swipe механика
- Поддержка mouse и touch событий
- Визуальная обратная связь (цветовая подсветка)
- Плавные анимации
- Возврат карточки при слабом свайпе

### Duo режим
1. Первый пользователь выбирает режим "вдвоём"
2. Генерируется уникальная реферальная ссылка
3. Ссылка копируется в буфер обмена
4. Второй пользователь переходит по ссылке
5. Оба вводят предпочтения
6. Система ждёт обоих пользователей
7. Генерируется смешанная подборка (30% + 30% + 40%)
8. Оба видят одинаковые фильмы
9. Финальная подборка - только взаимные лайки

### AI диалог
- Определение неясных запросов
- Автоматическое начало диалога
- Уточняющие вопросы
- Сбор полной информации
- Анимация "печатает..."
- Естественные ответы ("а, понял...")

### Анимации
- `fadeIn` - появление элементов
- `slideIn` / `slideOut` - swipe эффект
- `pulse` - пульсация
- Плавные transitions
- Transform эффекты

## Цветовая палитра (Розовая)

```scss
--pink-50: #fdf2f8;   // Фон
--pink-100: #fce7f3;  // Акценты
--pink-200: #fbcfe8;  // Границы
--pink-300: #f9a8d4;  // Ховеры
--pink-400: #f472b6;  // Градиенты
--pink-500: #ec4899;  // Основной
--pink-600: #db2777;  // Темнее
--white: #ffffff;     // Белый
```

## API Endpoints (Backend)

```
POST   /api/session              - Создать сессию
POST   /api/preferences          - Отправить предпочтения
GET    /api/movies/:sessionId    - Получить рекомендации
POST   /api/like                 - Лайкнуть фильм
POST   /api/dislike              - Дизлайкнуть фильм
GET    /api/final/:sessionId     - Финальная подборка
POST   /api/ai-chat              - Чат с ИИ
GET    /api/session/:id/status   - Статус сессии
```

## Технологический стек

### Frontend
- Angular 17
- Angular Material
- TypeScript
- SCSS
- RxJS

### Backend (требуется реализация)
- FastAPI (Python)
- PostgreSQL / MongoDB
- OpenAI API / LangChain
- Redis (для сессий)
- Okko API

## Следующие шаги

1. ✅ Frontend приложение создано
2. ⏳ Нужно создать FastAPI бэкенд
3. ⏳ Интегрировать ИИ (ChatGPT/Claude)
4. ⏳ Подключить базу данных с фильмами
5. ⏳ Интегрировать Okko API
6. ⏳ Деплой и тестирование

---

Создано командой: Артём, Катя, Елисей
Для Okko Vibecoding Hackathon 2025

