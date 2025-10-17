# 📚 Навигация по проекту Дайкинчик

## 🎯 Быстрый доступ

### Начало работы
1. **[RUN_ME_FIRST.md](RUN_ME_FIRST.md)** ⭐ - НАЧНИТЕ ЗДЕСЬ
2. **[QUICK_START.md](QUICK_START.md)** - Подробные инструкции
3. **[README.md](README.md)** - Обзор проекта

### Документация
- **[FEATURES.md](FEATURES.md)** - Полный список возможностей
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Архитектура проекта
- **[FILES_CREATED.md](FILES_CREATED.md)** - Список файлов
- **[SUMMARY.md](SUMMARY.md)** - Итоги создания

### Для разработчиков
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Как контрибьютить
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Деплой в продакшн
- **[frontend/README.md](frontend/README.md)** - Frontend документация
- **[backend/README.md](backend/README.md)** - Backend документация

### Запуск
- **[start.bat](start.bat)** - Запуск на Windows
- **[start.sh](start.sh)** - Запуск на Linux/Mac

## 📂 Структура проекта

```
vibecoding 17.10.25/
│
├── 📱 frontend/              Angular приложение
│   ├── src/app/
│   │   ├── components/      6 компонентов
│   │   ├── services/        2 сервиса
│   │   └── models/          Типы данных
│   └── README.md
│
├── 🔧 backend/               FastAPI сервер
│   ├── api/
│   │   ├── services/        3 сервиса
│   │   ├── models.py        Pydantic модели
│   │   └── routes.py        API endpoints
│   └── README.md
│
├── 📖 Документация/
│   ├── README.md            Главный обзор
│   ├── RUN_ME_FIRST.md      Быстрый старт
│   ├── QUICK_START.md       Инструкции
│   ├── FEATURES.md          Функции
│   ├── PROJECT_STRUCTURE.md Архитектура
│   ├── SUMMARY.md           Итоги
│   ├── DEPLOYMENT.md        Деплой
│   ├── CONTRIBUTING.md      Контрибьюция
│   └── INDEX.md             ← Вы здесь
│
└── 🚀 Скрипты/
    ├── start.bat            Windows
    └── start.sh             Linux/Mac
```

## 🎨 Компоненты Frontend

1. **WelcomeComponent** - Выбор режима (один/вдвоём)
2. **PreferencesInputComponent** - Ввод предпочтений
3. **AiDialogComponent** - Диалог с ИИ
4. **MovieCardComponent** - Swipe карточки фильмов
5. **FinalSelectionComponent** - Итоговая подборка
6. **LoadingComponent** - Загрузка

## 🔌 API Endpoints

```
POST   /api/session              Создать сессию
POST   /api/preferences          Предпочтения
GET    /api/movies/:sessionId    Рекомендации
POST   /api/like                 Лайк
POST   /api/dislike              Дизлайк
GET    /api/final/:sessionId     Финал
POST   /api/ai-chat              AI чат
GET    /api/session/:id/status   Статус
```

## 🎯 Функционал

### ✅ Реализовано
- Swipe механика (touch + mouse)
- AI диалог с уточнениями
- Duo режим с реферальными ссылками
- Финальная подборка
- Розовый дизайн без смайликов
- Адаптивная верстка
- Анимации

### ⏳ TODO
- Интеграция OpenAI/Claude
- База данных фильмов
- Okko API
- Redis для сессий
- Деплой

## 🔗 Полезные ссылки

После запуска:
- **Frontend:** http://localhost:4200
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## 📊 Статистика

- **Файлов:** 50+
- **Строк кода:** ~4800
- **Компонентов:** 6
- **Сервисов:** 5
- **Документов:** 8

## 💖 Команда

- **Артём** - Backend & AI
- **Катя** - Design & Frontend
- **Елисей** - Frontend & Integration

---

**Проект создан для Okko Vibecoding Hackathon 2025**

🚀 Удачи!

