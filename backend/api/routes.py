"""
API роуты
"""

from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from .models import (
    SessionCreate, SessionResponse, PreferencesRequest,
    Movie, LikeRequest, DislikeRequest,
    AIMessageRequest, AIMessageResponse, SessionStatus
)
from .services.session_service import SessionService
from .services.movie_service import MovieService
from .services.ai_service import AIService

router = APIRouter()

# Инициализация сервисов
session_service = SessionService()
movie_service = MovieService()
ai_service = AIService()


@router.post("/session", response_model=SessionResponse)
async def create_session(data: SessionCreate):
    """Создать новую сессию"""
    session_id = str(uuid.uuid4())
    
    # Сохраняем сессию
    session_service.create_session(session_id, data.mode)
    
    # Для duo режима генерируем реферальную ссылку
    referral_link = None
    if data.mode == 'duo':
        referral_link = f"http://localhost:4200/preferences/{session_id}"
    
    return SessionResponse(
        sessionId=session_id,
        referralLink=referral_link
    )


@router.post("/preferences")
async def submit_preferences(data: PreferencesRequest):
    """Отправить предпочтения пользователя"""
    session_service.save_preferences(
        data.sessionId,
        data.userId,
        data.preferences
    )
    return {"status": "success"}


@router.get("/movies/{session_id}", response_model=List[Movie])
async def get_movies(session_id: str):
    """Получить рекомендации фильмов"""
    session = session_service.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Получаем рекомендации на основе предпочтений
    movies = await movie_service.get_recommendations(session)
    
    return movies


@router.post("/like")
async def like_movie(data: LikeRequest):
    """Лайкнуть фильм"""
    session_service.like_movie(
        data.sessionId,
        data.movieId,
        data.userId
    )
    return {"status": "success"}


@router.post("/dislike")
async def dislike_movie(data: DislikeRequest):
    """Дизлайкнуть фильм"""
    session_service.dislike_movie(
        data.sessionId,
        data.movieId,
        data.userId
    )
    return {"status": "success"}


@router.get("/final/{session_id}", response_model=List[Movie])
async def get_final_selection(session_id: str):
    """Получить финальную подборку"""
    session = session_service.get_session(session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Получаем лайкнутые фильмы
    movies = movie_service.get_final_movies(session)
    
    return movies


@router.post("/ai-chat", response_model=AIMessageResponse)
async def ai_chat(data: AIMessageRequest):
    """Диалог с ИИ"""
    response = await ai_service.chat(data.sessionId, data.message)
    
    return AIMessageResponse(response=response)


@router.get("/session/{session_id}/status", response_model=SessionStatus)
async def check_session_status(session_id: str):
    """Проверить статус сессии (для duo режима)"""
    status = session_service.check_status(session_id)
    
    return SessionStatus(
        ready=status['ready'],
        bothUsersReady=status['both_ready']
    )

