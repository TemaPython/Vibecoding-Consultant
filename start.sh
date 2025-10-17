#!/bin/bash
# Скрипт для запуска Дайкинчик на Linux/Mac

echo "========================================"
echo "       Дайкинчик - Запуск"
echo "========================================"
echo ""

# Проверка Node.js
if ! command -v node &> /dev/null; then
    echo "[ОШИБКА] Node.js не установлен!"
    echo "Установите с https://nodejs.org/"
    exit 1
fi

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "[ОШИБКА] Python не установлен!"
    echo "Установите с https://www.python.org/"
    exit 1
fi

echo "[OK] Node.js и Python найдены"
echo ""

# Установка зависимостей если нужно
echo "Проверка зависимостей..."

if [ ! -d "backend/venv" ]; then
    echo "[1/4] Создание виртуального окружения Python..."
    cd backend
    python3 -m venv venv
    cd ..
fi

if [ ! -f "backend/venv/bin/activate" ]; then
    echo "[ОШИБКА] Не удалось создать виртуальное окружение"
    exit 1
fi

if [ ! -d "backend/venv/lib/python*/site-packages/fastapi" ]; then
    echo "[2/4] Установка зависимостей Backend..."
    cd backend
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "[3/4] Установка зависимостей Frontend..."
    cd frontend
    npm install
    cd ..
fi

echo "[4/4] Запуск серверов..."
echo ""

# Запуск Backend в фоне
echo "Запуск Backend на http://localhost:8000"
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Ждём 3 секунды
sleep 3

# Запуск Frontend в фоне
echo "Запуск Frontend на http://localhost:4200"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  ✅ Серверы запущены!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:4200"
echo "API docs: http://localhost:8000/docs"
echo ""
echo "Для остановки нажмите Ctrl+C"
echo "========================================"
echo ""

# Функция для остановки серверов
cleanup() {
    echo ""
    echo "Остановка серверов..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Готово!"
    exit 0
}

# Перехват сигнала остановки
trap cleanup INT TERM

# Ожидание
wait

