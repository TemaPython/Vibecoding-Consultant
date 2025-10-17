import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { StateService } from '../../services/state.service';
import { Movie } from '../../models/movie.model';

@Component({
  selector: 'app-final-selection',
  templateUrl: './final-selection.component.html',
  styleUrls: ['./final-selection.component.scss']
})
export class FinalSelectionComponent implements OnInit {
  likedMovies: Movie[] = [];
  sessionId: string | null = null;
  isLoading = true;
  isDuoMode = false;

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
      this.isDuoMode = session.mode === 'duo';
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

    this.loadFinalSelection();
  }

  loadFinalSelection(): void {
    if (!this.sessionId) return;

    this.apiService.getFinalSelection(this.sessionId).subscribe({
      next: (movies) => {
        this.likedMovies = movies;
        this.isLoading = false;

        // Если нет лайкнутых фильмов в duo режиме, показываем сообщение
        if (this.isDuoMode && movies.length === 0) {
          // Можно показать диалог с предложением уточнить предпочтения
          console.log('Нет общих лайкнутых фильмов');
        }
      },
      error: (error) => {
        console.error('Ошибка загрузки финальной подборки:', error);
        this.isLoading = false;
      }
    });
  }

  openOkko(movie: Movie): void {
    if (movie.okkoUrl) {
      window.open(movie.okkoUrl, '_blank');
    }
  }

  startOver(): void {
    this.stateService.reset();
    this.router.navigate(['/']);
  }

  refineSelection(): void {
    // Вернуться к предпочтениям для уточнения
    this.router.navigate(['/preferences']);
  }
}

