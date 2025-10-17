# Дайкинчик - Backend API

FastAPI бэкенд для приложения подбора фильмов.

## Установка

```bash
# Установка зависимостей
pip install -r requirements.txt
```

## Запуск

```bash
# Development режим
python main.py

# Или через uvicorn
uvicorn main:app --reload --port 8000
```

API будет доступно по адресу: `http://localhost:8000`

Документация Swagger: `http://localhost:8000/docs`

## Структура

```
backend/
├── api/
│   ├── services/           # Бизнес-логика
│   │   ├── session_service.py
│   │   ├── movie_service.py
│   │   └── ai_service.py
│   ├── models.py           # Pydantic модели
│   └── routes.py           # API эндпоинты
├── main.py                 # Точка входа
├── requirements.txt        # Зависимости
└── README.md
```

## API Endpoints

### Сессии

- `POST /api/session` - Создать сессию
  ```json
  {
    "mode": "single" | "duo"
  }
  ```

### Предпочтения

- `POST /api/preferences` - Сохранить предпочтения
  ```json
  {
    "sessionId": "uuid",
    "userId": "user1",
    "preferences": "Хочу комедию с Райаном Гослингом"
  }
  ```

### Фильмы

- `GET /api/movies/{sessionId}` - Получить рекомендации
- `POST /api/like` - Лайкнуть фильм
- `POST /api/dislike` - Дизлайкнуть фильм
- `GET /api/final/{sessionId}` - Финальная подборка

### ИИ

- `POST /api/ai-chat` - Диалог с ИИ
  ```json
  {
    "sessionId": "uuid",
    "message": "Не знаю что выбрать"
  }
  ```

### Статус

- `GET /api/session/{sessionId}/status` - Проверить статус сессии

## TODO

- [ ] Подключить PostgreSQL/MongoDB
- [ ] Интегрировать OpenAI/Claude для ИИ диалога
- [ ] Добавить базу данных фильмов
- [ ] Интегрировать Okko API
- [ ] Добавить Redis для сессий
- [ ] Добавить аутентификацию
- [ ] Добавить rate limiting
- [ ] Логирование
- [ ] Тесты

## Текущая реализация

⚠️ **Важно:** Сейчас используются mock данные!

- Сессии хранятся в памяти (при перезапуске теряются)
- Фильмы - тестовые данные с placeholder картинками
- ИИ чат - случайные заготовленные ответы

Для продакшена необходимо:
1. Подключить реальную БД
2. Добавить Redis для сессий
3. Интегрировать настоящий ИИ API
4. Подключить базу фильмов Okko

## Разработка

```bash
# Установка в dev режиме
pip install -r requirements.txt

# Запуск с автоперезагрузкой
uvicorn main:app --reload

# Проверка типов
mypy .
```

---

Создано для Okko Vibecoding Hackathon 2025

