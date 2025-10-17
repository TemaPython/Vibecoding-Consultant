# 🤝 Как контрибьютить в Дайкинчик

## Добро пожаловать!

Спасибо за интерес к проекту! Мы рады любой помощи.

## 📋 С чего начать

1. **Fork** репозитория
2. **Clone** на свой компьютер
3. Создайте **новую ветку**: `git checkout -b feature/amazing-feature`
4. Внесите изменения
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. Создайте **Pull Request**

## 🎯 Что можно улучшить

### Высокий приоритет
- [ ] Интеграция с OpenAI/Claude для AI диалога
- [ ] Подключение реальной базы данных фильмов
- [ ] Интеграция с Okko API
- [ ] Добавление Redis для сессий
- [ ] Улучшение рекомендательного алгоритма

### Средний приоритет
- [ ] Добавление тестов (Jest, Karma)
- [ ] Оптимизация производительности
- [ ] Добавление анимаций
- [ ] Улучшение мобильной версии
- [ ] Добавление темной темы

### Низкий приоритет
- [ ] PWA функционал
- [ ] Push уведомления
- [ ] Социальные шаринги
- [ ] История просмотров
- [ ] Favorites система

## 🎨 Гайдлайны по дизайну

### Цвета
Используйте розовую палитру:
- Primary: `#ec4899`
- Secondary: `#f472b6`
- Background: `#fdf2f8`

### Иконки
- Без смайликов!
- Material Icons предпочтительны
- Минималистичный стиль

### Анимации
- Плавные transitions (0.3s ease)
- Transform вместо position
- 60 FPS

## 💻 Код стайл

### TypeScript/Angular
```typescript
// Используйте строгую типизацию
interface Movie {
  id: string;
  title: string;
}

// Arrow functions
const getMovie = (id: string): Movie => {
  // ...
}

// Async/await
async fetchMovies(): Promise<Movie[]> {
  // ...
}
```

### Python/FastAPI
```python
# Type hints обязательны
def get_movie(movie_id: str) -> Movie:
    pass

# Async endpoints
@router.get("/movies/{id}")
async def get_movie(id: str) -> Movie:
    pass
```

### CSS/SCSS
```scss
// BEM naming
.movie-card {
  &__title {
    // ...
  }
  
  &--active {
    // ...
  }
}

// Переменные для цветов
.button {
  background: var(--pink-500);
}
```

## 🧪 Тестирование

### Frontend (Angular)
```typescript
describe('MovieCardComponent', () => {
  it('should create', () => {
    expect(component).toBeTruthy();
  });
  
  it('should like movie on swipe right', () => {
    // test implementation
  });
});
```

### Backend (FastAPI)
```python
def test_create_session():
    response = client.post("/api/session", json={"mode": "single"})
    assert response.status_code == 200
    assert "sessionId" in response.json()
```

## 📝 Commit Messages

Используйте conventional commits:

```
feat: добавить AI диалог
fix: исправить swipe на мобильных
docs: обновить README
style: поправить отступы
refactor: рефакторинг movie service
test: добавить тесты для API
chore: обновить зависимости
```

## 🔍 Code Review

Перед PR убедитесь:
- [ ] Код следует стайл гайдам
- [ ] Все тесты проходят
- [ ] Нет console.log в production коде
- [ ] Документация обновлена
- [ ] Commit messages понятные

## 🐛 Баг репорты

При создании issue укажите:
1. **Описание** - что происходит
2. **Ожидаемое поведение** - что должно быть
3. **Шаги воспроизведения**
4. **Скриншоты** (если применимо)
5. **Окружение** (браузер, OS, версии)

## 💡 Feature requests

Перед предложением новой фичи:
1. Проверьте существующие issues
2. Опишите use case
3. Объясните почему это важно
4. Предложите реализацию (опционально)

## 📚 Документация

При изменении функционала обновите:
- README.md
- Комментарии в коде
- API документацию
- FEATURES.md

## 🎓 Полезные ресурсы

- [Angular Documentation](https://angular.io/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Material Design](https://material.io/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 👥 Команда

Свяжитесь с нами:
- **Артём** - Backend & AI
- **Катя** - Design & Frontend
- **Елисей** - Frontend & Integration

## 📄 Лицензия

Продолжая контрибьютить, вы соглашаетесь что ваш код будет под той же лицензией что и проект.

---

💖 Спасибо за ваш вклад в Дайкинчик!

