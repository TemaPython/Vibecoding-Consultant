import { Component, OnInit, HostListener } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { StateService } from '../../services/state.service';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-movie-card',
  templateUrl: './movie-card.component.html',
  styleUrls: ['./movie-card.component.scss']
})
export class MovieCardComponent implements OnInit {
  movies: Movie[] = [];
  currentIndex = 0;
  currentMovie: Movie | null = null;
  sessionId: string | null = null;
  userId: string = 'user1';
  
  // Для swipe анимации
  isDragging = false;
  startX = 0;
  startY = 0;
  currentX = 0;
  currentY = 0;
  
  moviesShown = 0;
  maxMovies = 20;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private apiService: ApiService,
    private stateService: StateService
  ) {}

  ngOnInit(): void {
    const session = this.stateService.getSession();
    
    if (session) {
      this.sessionId = session.sessionId;
    }

    this.route.params.subscribe(params => {
      if (params['sessionId']) {
        this.sessionId = params['sessionId'];
      }
    });

    if (!this.sessionId) {
      this.router.navigate(['/']);
      return;
    }

    this.loadMovies();
  }

  loadMovies(): void {
    this.movies = this.stateService.getMovies();
    
    if (this.movies.length === 0) {
      // Загружаем с сервера
      this.apiService.getMovieRecommendations(this.sessionId!).subscribe({
        next: (movies) => {
          this.movies = movies;
          this.stateService.setMovies(movies);
          this.currentMovie = this.movies[this.currentIndex];
        },
        error: (error) => {
          console.error('Ошибка загрузки фильмов:', error);
          alert('Не удалось загрузить фильмы');
          this.router.navigate(['/']);
        }
      });
    } else {
      this.currentMovie = this.movies[this.currentIndex];
    }
  }

  // Mouse events
  onMouseDown(event: MouseEvent): void {
    this.isDragging = true;
    this.startX = event.clientX;
    this.startY = event.clientY;
  }

  @HostListener('document:mousemove', ['$event'])
  onMouseMove(event: MouseEvent): void {
    if (!this.isDragging) return;

    this.currentX = event.clientX - this.startX;
    this.currentY = event.clientY - this.startY;

    const card = document.querySelector('.movie-card-active') as HTMLElement;
    if (card) {
      const rotation = this.currentX / 20;
      card.style.transform = `translate(${this.currentX}px, ${this.currentY}px) rotate(${rotation}deg)`;
      
      // Визуальная подсказка
      if (this.currentX > 50) {
        card.classList.add('like-hint');
        card.classList.remove('dislike-hint');
      } else if (this.currentX < -50) {
        card.classList.add('dislike-hint');
        card.classList.remove('like-hint');
      } else {
        card.classList.remove('like-hint', 'dislike-hint');
      }
    }
  }

  @HostListener('document:mouseup', ['$event'])
  onMouseUp(event: MouseEvent): void {
    if (!this.isDragging) return;

    const card = document.querySelector('.movie-card-active') as HTMLElement;
    
    if (Math.abs(this.currentX) > 100) {
      // Завершаем свайп
      if (this.currentX > 0) {
        this.likeMovie();
      } else {
        this.dislikeMovie();
      }
    } else {
      // Возвращаем карточку обратно
      if (card) {
        card.style.transition = 'transform 0.3s ease';
        card.style.transform = 'translate(0, 0) rotate(0deg)';
        card.classList.remove('like-hint', 'dislike-hint');
        
        setTimeout(() => {
          card.style.transition = '';
        }, 300);
      }
    }

    this.isDragging = false;
    this.currentX = 0;
    this.currentY = 0;
  }

  // Touch events
  onTouchStart(event: TouchEvent): void {
    this.isDragging = true;
    this.startX = event.touches[0].clientX;
    this.startY = event.touches[0].clientY;
  }

  @HostListener('document:touchmove', ['$event'])
  onTouchMove(event: TouchEvent): void {
    if (!this.isDragging) return;

    this.currentX = event.touches[0].clientX - this.startX;
    this.currentY = event.touches[0].clientY - this.startY;

    const card = document.querySelector('.movie-card-active') as HTMLElement;
    if (card) {
      const rotation = this.currentX / 20;
      card.style.transform = `translate(${this.currentX}px, ${this.currentY}px) rotate(${rotation}deg)`;
      
      if (this.currentX > 50) {
        card.classList.add('like-hint');
        card.classList.remove('dislike-hint');
      } else if (this.currentX < -50) {
        card.classList.add('dislike-hint');
        card.classList.remove('like-hint');
      } else {
        card.classList.remove('like-hint', 'dislike-hint');
      }
    }
  }

  @HostListener('document:touchend', ['$event'])
  onTouchEnd(event: TouchEvent): void {
    if (!this.isDragging) return;

    const card = document.querySelector('.movie-card-active') as HTMLElement;
    
    if (Math.abs(this.currentX) > 100) {
      if (this.currentX > 0) {
        this.likeMovie();
      } else {
        this.dislikeMovie();
      }
    } else {
      if (card) {
        card.style.transition = 'transform 0.3s ease';
        card.style.transform = 'translate(0, 0) rotate(0deg)';
        card.classList.remove('like-hint', 'dislike-hint');
        
        setTimeout(() => {
          card.style.transition = '';
        }, 300);
      }
    }

    this.isDragging = false;
    this.currentX = 0;
    this.currentY = 0;
  }

  likeMovie(): void {
    if (!this.currentMovie || !this.sessionId) return;

    const card = document.querySelector('.movie-card-active') as HTMLElement;
    if (card) {
      card.style.transition = 'transform 0.5s ease';
      card.style.transform = 'translate(150%, -50%) rotate(30deg)';
      card.classList.add('swiped-right');
    }

    this.apiService.likeMovie(this.sessionId, this.currentMovie.id, this.userId).subscribe({
      next: () => {
        this.stateService.addLikedMovie(this.currentMovie!.id);
        setTimeout(() => {
          this.nextMovie();
        }, 500);
      },
      error: (error) => {
        console.error('Ошибка лайка:', error);
        setTimeout(() => {
          this.nextMovie();
        }, 500);
      }
    });
  }

  dislikeMovie(): void {
    if (!this.currentMovie || !this.sessionId) return;

    const card = document.querySelector('.movie-card-active') as HTMLElement;
    if (card) {
      card.style.transition = 'transform 0.5s ease';
      card.style.transform = 'translate(-150%, -50%) rotate(-30deg)';
      card.classList.add('swiped-left');
    }

    this.apiService.dislikeMovie(this.sessionId, this.currentMovie.id, this.userId).subscribe({
      next: () => {
        setTimeout(() => {
          this.nextMovie();
        }, 500);
      },
      error: (error) => {
        console.error('Ошибка дизлайка:', error);
        setTimeout(() => {
          this.nextMovie();
        }, 500);
      }
    });
  }

  nextMovie(): void {
    this.moviesShown++;
    
    if (this.moviesShown >= this.maxMovies) {
      // Переход к финальному экрану
      this.router.navigate(['/final', this.sessionId]);
      return;
    }

    this.currentIndex++;
    
    if (this.currentIndex >= this.movies.length) {
      // Все фильмы просмотрены
      this.router.navigate(['/final', this.sessionId]);
      return;
    }

    this.currentMovie = this.movies[this.currentIndex];
    this.stateService.setCurrentMovieIndex(this.currentIndex);

    // Сброс стилей карточки
    setTimeout(() => {
      const card = document.querySelector('.movie-card-active') as HTMLElement;
      if (card) {
        card.style.transition = '';
        card.style.transform = '';
        card.classList.remove('swiped-left', 'swiped-right', 'like-hint', 'dislike-hint');
      }
    }, 100);
  }

  openOkko(): void {
    if (this.currentMovie && this.currentMovie.okkoUrl) {
      window.open(this.currentMovie.okkoUrl, '_blank');
    }
  }
}

