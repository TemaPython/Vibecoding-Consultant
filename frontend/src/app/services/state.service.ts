import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Session, Movie } from '../models/movie.model';

@Injectable({
  providedIn: 'root'
})
export class StateService {
  private sessionSubject = new BehaviorSubject<Session | null>(null);
  public session$: Observable<Session | null> = this.sessionSubject.asObservable();

  private moviesSubject = new BehaviorSubject<Movie[]>([]);
  public movies$: Observable<Movie[]> = this.moviesSubject.asObservable();

  private currentMovieIndexSubject = new BehaviorSubject<number>(0);
  public currentMovieIndex$: Observable<number> = this.currentMovieIndexSubject.asObservable();

  private likedMoviesSubject = new BehaviorSubject<string[]>([]);
  public likedMovies$: Observable<string[]> = this.likedMoviesSubject.asObservable();

  private isLoadingSubject = new BehaviorSubject<boolean>(false);
  public isLoading$: Observable<boolean> = this.isLoadingSubject.asObservable();

  constructor() { }

  // Сессия
  setSession(session: Session): void {
    this.sessionSubject.next(session);
  }

  getSession(): Session | null {
    return this.sessionSubject.value;
  }

  // Фильмы
  setMovies(movies: Movie[]): void {
    this.moviesSubject.next(movies);
  }

  getMovies(): Movie[] {
    return this.moviesSubject.value;
  }

  // Текущий индекс фильма
  setCurrentMovieIndex(index: number): void {
    this.currentMovieIndexSubject.next(index);
  }

  getCurrentMovieIndex(): number {
    return this.currentMovieIndexSubject.value;
  }

  incrementMovieIndex(): void {
    this.currentMovieIndexSubject.next(this.currentMovieIndexSubject.value + 1);
  }

  // Лайкнутые фильмы
  addLikedMovie(movieId: string): void {
    const currentLiked = this.likedMoviesSubject.value;
    this.likedMoviesSubject.next([...currentLiked, movieId]);
  }

  getLikedMovies(): string[] {
    return this.likedMoviesSubject.value;
  }

  // Загрузка
  setLoading(isLoading: boolean): void {
    this.isLoadingSubject.next(isLoading);
  }

  isLoading(): boolean {
    return this.isLoadingSubject.value;
  }

  // Сброс состояния
  reset(): void {
    this.sessionSubject.next(null);
    this.moviesSubject.next([]);
    this.currentMovieIndexSubject.next(0);
    this.likedMoviesSubject.next([]);
    this.isLoadingSubject.next(false);
  }
}

