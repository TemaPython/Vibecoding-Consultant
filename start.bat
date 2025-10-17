@echo off
REM Скрипт для запуска Дайкинчик на Windows

echo ========================================
echo        Дайкинчик - Запуск
echo ========================================
echo.

REM Проверка Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Node.js не установлен!
    echo Скачайте с https://nodejs.org/
    pause
    exit /b 1
)

REM Проверка Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Python не установлен!
    echo Скачайте с https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Node.js и Python найдены
echo.

REM Установка зависимостей если нужно
echo Проверка зависимостей...

if not exist "backend\venv" (
    echo [1/4] Создание виртуального окружения Python...
    cd backend
    python -m venv venv
    cd ..
)

if not exist "backend\venv\Lib\site-packages\fastapi" (
    echo [2/4] Установка зависимостей Backend...
    cd backend
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
)

if not exist "frontend\node_modules" (
    echo [3/4] Установка зависимостей Frontend...
    cd frontend
    call npm install
    cd ..
)

echo [4/4] Запуск серверов...
echo.

REM Запуск Backend в новом окне
echo Запуск Backend на http://localhost:8000
start "Дайкинчик - Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python main.py"

REM Ждём 3 секунды
timeout /t 3 /nobreak >nul

REM Запуск Frontend в новом окне
echo Запуск Frontend на http://localhost:4200
start "Дайкинчик - Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo   ✅ Серверы запущены!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:4200
echo API docs: http://localhost:8000/docs
echo.
echo Для остановки закройте окна серверов
echo ========================================
echo.

pause

