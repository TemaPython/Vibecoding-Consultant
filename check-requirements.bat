@echo off
REM Скрипт для проверки установленных зависимостей

echo ========================================
echo    Проверка зависимостей
echo ========================================
echo.

REM Проверка Node.js
echo [1/2] Проверка Node.js...
where node >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Node.js установлен
    node --version
    npm --version
) else (
    echo ❌ Node.js НЕ установлен
    echo.
    echo Скачайте с: https://nodejs.org/
    echo Выберите LTS версию (зелёная кнопка)
)

echo.

REM Проверка Python
echo [2/2] Проверка Python...
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Python установлен
    python --version
) else (
    where py >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Python установлен (через py)
        py --version
    ) else (
        echo ❌ Python НЕ установлен
        echo.
        echo Скачайте с: https://www.python.org/downloads/
        echo ⚠️  При установке поставьте галочку "Add Python to PATH"
    )
)

echo.
echo ========================================
echo    Результат проверки
echo ========================================
echo.

where node >nul 2>nul
set NODE_OK=%ERRORLEVEL%

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    where py >nul 2>nul
)
set PYTHON_OK=%ERRORLEVEL%

if %NODE_OK% EQU 0 if %PYTHON_OK% EQU 0 (
    echo ✅ Всё установлено! Можете запускать start.bat
) else (
    if %NODE_OK% NEQ 0 (
        echo ❌ Нужно установить Node.js
    )
    if %PYTHON_OK% NEQ 0 (
        echo ❌ Нужно установить Python
    )
    echo.
    echo После установки:
    echo 1. Закройте это окно PowerShell
    echo 2. Откройте новое окно PowerShell
    echo 3. Запустите check-requirements.bat снова
)

echo ========================================
echo.
pause

