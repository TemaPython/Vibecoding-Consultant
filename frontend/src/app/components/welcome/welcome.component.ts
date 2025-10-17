import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { StateService } from '../../services/state.service';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.scss']
})
export class WelcomeComponent {
  isLoading = false;

  constructor(
    private router: Router,
    private apiService: ApiService,
    private stateService: StateService
  ) {
    // Сброс состояния при возврате на главную
    this.stateService.reset();
  }

  selectMode(mode: 'single' | 'duo'): void {
    this.isLoading = true;
    
    this.apiService.createSession(mode).subscribe({
      next: (response) => {
        const session = {
          sessionId: response.sessionId,
          mode: mode,
          likedMovies: [],
          dislikedMovies: [],
          user1Likes: [],
          user2Likes: []
        };

        this.stateService.setSession(session);

        if (mode === 'duo' && response.referralLink) {
          // Показываем реферальную ссылку для режима вдвоём
          this.showReferralLink(response.referralLink, response.sessionId);
        } else {
          // Переход к вводу предпочтений
          this.router.navigate(['/preferences']);
        }
        
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Ошибка создания сессии:', error);
        this.isLoading = false;
        alert('Произошла ошибка. Попробуйте снова.');
      }
    });
  }

  showReferralLink(link: string, sessionId: string): void {
    // Временно используем alert, позже можно заменить на модальное окно
    const message = `Скопируйте ссылку и отправьте второму пользователю:\n\n${link}\n\nОжидайте, пока второй пользователь присоединится...`;
    
    // Копируем в буфер обмена
    navigator.clipboard.writeText(link).then(() => {
      alert(message + '\n\n✓ Ссылка скопирована в буфер обмена!');
      // Переход к вводу предпочтений
      this.router.navigate(['/preferences', sessionId]);
    }).catch(() => {
      alert(message);
      this.router.navigate(['/preferences', sessionId]);
    });
  }
}

