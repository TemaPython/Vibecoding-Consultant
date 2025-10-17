@echo off
REM Скрипт для запуска только Frontend (без Backend)

echo ========================================
echo    Дайкинчик - Frontend Only
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

echo [OK] Node.js найден
echo.

REM Переход в папку frontend
cd frontend

REM Установка зависимостей если нужно
if not exist "node_modules" (
    echo Установка зависимостей...
    call npm install
)

echo.
echo ========================================
echo   Запуск Frontend...
echo ========================================
echo.
echo Frontend будет доступен на:
echo http://localhost:4200
echo.
echo ⚠️  Backend не запущен!
echo API запросы не будут работать.
echo.
echo Для остановки нажмите Ctrl+C
echo ========================================
echo.

REM Запуск
call npm start

pause

