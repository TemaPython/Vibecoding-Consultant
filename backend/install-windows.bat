@echo off
REM Установка зависимостей для Windows

echo ========================================
echo   Установка Backend зависимостей
echo ========================================
echo.

echo [1/3] Обновление pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo [2/3] Установка основных пакетов...
python -m pip install fastapi==0.104.1
python -m pip install uvicorn==0.24.0
python -m pip install pydantic==2.5.0
python -m pip install python-multipart==0.0.6

echo.
echo [3/3] Установка дополнительных пакетов...
python -m pip install click h11

echo.
echo ========================================
echo   ✅ Установка завершена!
echo ========================================
echo.

pause

