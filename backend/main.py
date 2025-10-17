"""
Дайкинчик - FastAPI Backend
Основной файл приложения
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(
    title="Дайкинчик API",
    description="API для подбора фильмов с использованием ИИ",
    version="1.0.0"
)

# CORS для работы с Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутов
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Дайкинчик API!",
        "docs": "/docs",
        "frontend": "http://localhost:4200"
    }

if __name__ == "__main__":
    import uvicorn
    print("🎬 Запуск Дайкинчик API...")
    print("📝 Документация: http://localhost:8000/docs")
    print("🎨 Frontend: http://localhost:4200")
    uvicorn.run(app, host="0.0.0.0", port=8000)

