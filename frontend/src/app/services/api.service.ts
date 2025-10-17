import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Movie, UserPreferences } from '../models/movie.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api'; // FastAPI backend

  constructor(private http: HttpClient) { }

  // Создать сессию
  createSession(mode: 'single' | 'duo'): Observable<{ sessionId: string, referralLink?: string }> {
    return this.http.post<{ sessionId: string, referralLink?: string }>(`${this.apiUrl}/session`, { mode });
  }

  // Отправить предпочтения пользователя
  submitPreferences(sessionId: string, userId: string, preferences: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/preferences`, {
      sessionId,
      userId,
      preferences
    });
  }

  // Получить рекомендации фильмов
  getMovieRecommendations(sessionId: string): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/movies/${sessionId}`);
  }

  // Лайк фильма
  likeMovie(sessionId: string, movieId: string, userId?: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/like`, { sessionId, movieId, userId });
  }

  // Дизлайк фильма
  dislikeMovie(sessionId: string, movieId: string, userId?: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/dislike`, { sessionId, movieId, userId });
  }

  // Получить финальную подборку
  getFinalSelection(sessionId: string): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/final/${sessionId}`);
  }

  // Отправить сообщение в AI чат
  sendAIMessage(sessionId: string, message: string): Observable<{ response: string }> {
    return this.http.post<{ response: string }>(`${this.apiUrl}/ai-chat`, {
      sessionId,
      message
    });
  }

  // Проверить статус сессии (для duo режима)
  checkSessionStatus(sessionId: string): Observable<{ ready: boolean, bothUsersReady: boolean }> {
    return this.http.get<{ ready: boolean, bothUsersReady: boolean }>(`${this.apiUrl}/session/${sessionId}/status`);
  }
}

