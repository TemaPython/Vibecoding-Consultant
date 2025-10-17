"""
Pydantic модели для API
"""

from pydantic import BaseModel
from typing import List, Optional, Literal

class SessionCreate(BaseModel):
    mode: Literal['single', 'duo']

class SessionResponse(BaseModel):
    sessionId: str
    referralLink: Optional[str] = None

class PreferencesRequest(BaseModel):
    sessionId: str
    userId: str
    preferences: str

class Movie(BaseModel):
    id: str
    title: str
    poster: str
    rating: float
    year: int
    actors: List[str]
    description: str
    okkoUrl: str
    genre: Optional[List[str]] = []

class LikeRequest(BaseModel):
    sessionId: str
    movieId: str
    userId: Optional[str] = None

class DislikeRequest(BaseModel):
    sessionId: str
    movieId: str
    userId: Optional[str] = None

class AIMessageRequest(BaseModel):
    sessionId: str
    message: str

class AIMessageResponse(BaseModel):
    response: str

class SessionStatus(BaseModel):
    ready: bool
    bothUsersReady: bool

