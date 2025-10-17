# 🚀 Деплой Дайкинчик

## Варианты деплоя

### 1. Vercel (Frontend) + Render (Backend)

#### Frontend на Vercel

```bash
# Установить Vercel CLI
npm i -g vercel

# Перейти в папку frontend
cd frontend

# Деплой
vercel --prod
```

**Настройки Vercel:**
- Build Command: `npm run build`
- Output Directory: `dist/daikinchik`
- Framework: Angular

#### Backend на Render

1. Создать аккаунт на https://render.com
2. New > Web Service
3. Подключить GitHub репозиторий
4. Настройки:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend`

### 2. Railway (Full Stack)

```bash
# Установить Railway CLI
npm i -g @railway/cli

# Войти
railway login

# Инициализировать
railway init

# Деплой Backend
cd backend
railway up

# Деплой Frontend
cd ../frontend
railway up
```

### 3. Docker

#### Dockerfile для Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile для Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18 as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build --prod

FROM nginx:alpine
COPY --from=build /app/dist/daikinchik /usr/share/nginx/html
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
  
  frontend:
    build: ./frontend
    ports:
      - "4200:80"
    depends_on:
      - backend
```

### 4. Heroku

#### Backend
```bash
cd backend
heroku create daikinchik-api
heroku buildpacks:set heroku/python
git push heroku main
```

#### Frontend
```bash
cd frontend
heroku create daikinchik-app
heroku buildpacks:set heroku/nodejs
git push heroku main
```

## Переменные окружения

### Backend (.env)
```env
# API Keys
OPENAI_API_KEY=your_key_here
OKKO_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Redis
REDIS_URL=redis://host:6379

# CORS
FRONTEND_URL=https://daikinchik.vercel.app
```

### Frontend (environment.prod.ts)
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://daikinchik-api.render.com/api'
};
```

## Настройка базы данных

### PostgreSQL на Supabase

1. Создать проект на https://supabase.com
2. Получить DATABASE_URL
3. Создать таблицы:

```sql
CREATE TABLE movies (
  id UUID PRIMARY KEY,
  title VARCHAR(255),
  poster TEXT,
  rating DECIMAL(3,1),
  year INTEGER,
  actors TEXT[],
  description TEXT,
  okko_url TEXT,
  genre TEXT[]
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  mode VARCHAR(10),
  user1_preferences TEXT,
  user2_preferences TEXT,
  liked_movies TEXT[],
  disliked_movies TEXT[],
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Мониторинг и логи

### Sentry (ошибки)

```bash
npm install @sentry/angular @sentry/tracing
```

```typescript
// frontend/src/main.ts
import * as Sentry from "@sentry/angular";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  integrations: [
    new Sentry.BrowserTracing(),
  ],
  tracesSampleRate: 1.0,
});
```

### LogRocket (сессии)

```bash
npm install logrocket
```

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl ${{ secrets.RENDER_DEPLOY_HOOK }}
  
  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npm i -g vercel
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## SSL/HTTPS

Все современные платформы (Vercel, Render, Railway) автоматически предоставляют SSL сертификаты.

## Масштабирование

### Кэширование
- Redis для сессий
- CDN для статики (Cloudflare)

### База данных
- Индексы на часто используемые поля
- Connection pooling
- Read replicas

### Backend
- Увеличить количество workers: `--workers 4`
- Async endpoints
- Background tasks (Celery)

## Чеклист перед деплоем

- [ ] Обновить API URLs в environment.prod.ts
- [ ] Настроить CORS для продакшн домена
- [ ] Добавить переменные окружения
- [ ] Настроить SSL
- [ ] Подключить мониторинг ошибок
- [ ] Настроить логирование
- [ ] Добавить rate limiting
- [ ] Оптимизировать изображения
- [ ] Включить compression
- [ ] Протестировать на разных устройствах

---

**Рекомендуемый стек для продакшена:**
- Frontend: Vercel
- Backend: Render или Railway
- Database: Supabase
- Redis: Upstash
- Monitoring: Sentry
- Analytics: Google Analytics

💖 Удачного деплоя!

