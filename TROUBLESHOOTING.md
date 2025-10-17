# 🔧 Решение проблем

## Проблема: "pip" не распознано

### Причина
Python не установлен или не добавлен в PATH Windows.

### Решение 1: Установка Python

1. **Скачайте Python:**
   - https://www.python.org/downloads/
   - Версия 3.8 или выше

2. **При установке:**
   - ✅ **Обязательно** поставьте галочку **"Add Python to PATH"**
   - Нажмите "Install Now"

3. **После установки:**
   - Закройте все окна PowerShell
   - Откройте новое окно PowerShell
   - Проверьте: `python --version`

### Решение 2: Использовать python -m pip

Если Python установлен, но pip не работает:

```powershell
# Вместо:
pip install -r requirements.txt

# Используйте:
python -m pip install -r requirements.txt

# Или:
py -m pip install -r requirements.txt
```

### Решение 3: Запустить только Frontend

Пока разбираетесь с Python, можете запустить Frontend:

```powershell
# Запустить скрипт
start-frontend-only.bat

# Или вручную:
cd frontend
npm install
npm start
```

Frontend откроется на http://localhost:4200
(API запросы не будут работать без Backend)

## Проблема: "node" не распознано

### Решение

1. **Скачайте Node.js:**
   - https://nodejs.org/
   - Выберите LTS версию

2. **Установите:**
   - Следуйте инструкциям установщика
   - Node.js автоматически добавится в PATH

3. **Проверьте:**
   ```powershell
   node --version
   npm --version
   ```

## Проблема: Порт 4200 занят

### Решение

```powershell
# Найти процесс на порту 4200
netstat -ano | findstr :4200

# Убить процесс (замените PID на ID из предыдущей команды)
taskkill /PID <PID> /F

# Или запустить на другом порту
ng serve --port 4300
```

## Проблема: Порт 8000 занят

### Решение

```powershell
# Найти процесс
netstat -ano | findstr :8000

# Убить процесс
taskkill /PID <PID> /F

# Или запустить на другом порту
uvicorn main:app --port 8001
```

## Проблема: CORS ошибки

### Причина
Backend и Frontend на разных портах.

### Решение
Убедитесь что в `backend/main.py` указан правильный CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Проблема: npm install не работает

### Решение

```powershell
# Очистить кэш
npm cache clean --force

# Удалить node_modules
rmdir /s /q node_modules
del package-lock.json

# Переустановить
npm install
```

## Проблема: Angular CLI не найден

### Решение

```powershell
# Установить глобально
npm install -g @angular/cli

# Или использовать npx
npx ng serve
```

## Проблема: Модуль не найден в Python

### Решение

```powershell
# Активировать виртуальное окружение
cd backend
python -m venv venv
.\venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt
```

## Проблема: Браузер не открывается

### Решение

Откройте вручную:
- Frontend: http://localhost:4200
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Проблема: "Access denied" при установке

### Решение

Запустите PowerShell от имени администратора:
1. Win + X
2. "Windows PowerShell (администратор)"
3. Запустите команды установки

## Проблема: Политика выполнения скриптов

Если получаете ошибку при запуске .bat файлов:

```powershell
# Разрешить выполнение скриптов (от администратора)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Проблема: Git конфликты

### Решение

```powershell
# Посмотреть статус
git status

# Отменить изменения
git restore .

# Или сохранить изменения
git stash
git pull
git stash pop
```

## Проблема: Медленная работа

### Решение

1. **Проверьте антивирус** - добавьте папки проекта в исключения
2. **Закройте лишние программы**
3. **Очистите кэш:**
   ```powershell
   # Angular
   rm -r frontend/.angular/cache
   
   # Python
   find . -type d -name __pycache__ -delete
   ```

## Нужна помощь?

1. Проверьте документацию:
   - [README.md](README.md)
   - [QUICK_START.md](QUICK_START.md)
   - [RUN_ME_FIRST.md](RUN_ME_FIRST.md)

2. Проверьте логи:
   - Backend: в консоли где запущен Python
   - Frontend: в консоли где запущен npm
   - Браузер: F12 → Console

3. Создайте Issue на GitHub с:
   - Описанием проблемы
   - Скриншотом ошибки
   - Версиями (node --version, python --version)
   - Операционной системой

---

💖 Удачи в решении проблем!

