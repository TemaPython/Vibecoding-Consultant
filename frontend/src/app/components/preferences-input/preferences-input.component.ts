import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { StateService } from '../../services/state.service';

@Component({
  selector: 'app-preferences-input',
  templateUrl: './preferences-input.component.html',
  styleUrls: ['./preferences-input.component.scss']
})
export class PreferencesInputComponent implements OnInit {
  preferences = '';
  isLoading = false;
  sessionId: string | null = null;
  userId: string = 'user1';
  showAiDialog = false;
  isDuoMode = false;
  waitingForSecondUser = false;

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

    // Проверяем, есть ли sessionId в URL (для второго пользователя в duo режиме)
    this.route.params.subscribe(params => {
      if (params['sessionId']) {
        this.sessionId = params['sessionId'];
        this.userId = 'user2';
        this.isDuoMode = true;
      }
    });

    if (!this.sessionId) {
      this.router.navigate(['/']);
    }
  }

  onSubmit(): void {
    if (!this.preferences.trim() || !this.sessionId) {
      return;
    }

    // Если пользователь затрудняется или пишет очень мало, показываем AI диалог
    if (this.preferences.length < 10 || this.isUnclear()) {
      this.showAiDialog = true;
      return;
    }

    this.submitPreferences();
  }

  isUnclear(): boolean {
    const unclearPhrases = [
      'не знаю',
      'затрудняюсь',
      'что угодно',
      'всё равно',
      'любой',
      'посоветуй',
      'помоги',
      'хз'
    ];
    
    const lowerPrefs = this.preferences.toLowerCase();
    return unclearPhrases.some(phrase => lowerPrefs.includes(phrase));
  }

  submitPreferences(): void {
    if (!this.sessionId) return;

    this.isLoading = true;

    this.apiService.submitPreferences(this.sessionId, this.userId, this.preferences).subscribe({
      next: () => {
        if (this.isDuoMode && this.userId === 'user1') {
          // Первый пользователь в duo режиме - ожидаем второго
          this.waitingForSecondUser = true;
          this.checkBothUsersReady();
        } else {
          // Одиночный режим или второй пользователь - переходим к фильмам
          this.loadMovies();
        }
      },
      error: (error) => {
        console.error('Ошибка отправки предпочтений:', error);
        this.isLoading = false;
        alert('Произошла ошибка. Попробуйте снова.');
      }
    });
  }

  checkBothUsersReady(): void {
    if (!this.sessionId) return;

    const checkInterval = setInterval(() => {
      this.apiService.checkSessionStatus(this.sessionId!).subscribe({
        next: (status) => {
          if (status.bothUsersReady) {
            clearInterval(checkInterval);
            this.loadMovies();
          }
        },
        error: (error) => {
          console.error('Ошибка проверки статуса:', error);
          clearInterval(checkInterval);
          this.isLoading = false;
        }
      });
    }, 2000); // Проверяем каждые 2 секунды

    // Таймаут через 5 минут
    setTimeout(() => {
      clearInterval(checkInterval);
      if (this.waitingForSecondUser) {
        alert('Время ожидания истекло. Попробуйте снова.');
        this.router.navigate(['/']);
      }
    }, 300000);
  }

  loadMovies(): void {
    if (!this.sessionId) return;

    this.apiService.getMovieRecommendations(this.sessionId).subscribe({
      next: (movies) => {
        this.stateService.setMovies(movies);
        this.isLoading = false;
        this.router.navigate(['/movies', this.sessionId]);
      },
      error: (error) => {
        console.error('Ошибка загрузки фильмов:', error);
        this.isLoading = false;
        alert('Не удалось загрузить фильмы. Попробуйте снова.');
      }
    });
  }

  onAiDialogComplete(finalPreferences: string): void {
    this.preferences = finalPreferences;
    this.showAiDialog = false;
    this.submitPreferences();
  }

  onAiDialogCancel(): void {
    this.showAiDialog = false;
  }
}

