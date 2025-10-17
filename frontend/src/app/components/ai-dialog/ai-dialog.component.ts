import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { AIMessage } from '../../models/movie.model';

@Component({
  selector: 'app-ai-dialog',
  templateUrl: './ai-dialog.component.html',
  styleUrls: ['./ai-dialog.component.scss']
})
export class AiDialogComponent implements OnInit {
  @Input() initialMessage: string = '';
  @Input() sessionId: string = '';
  @Output() complete = new EventEmitter<string>();
  @Output() cancel = new EventEmitter<void>();

  messages: AIMessage[] = [];
  currentMessage = '';
  isLoading = false;
  isTyping = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    // Добавляем начальное сообщение пользователя
    if (this.initialMessage) {
      this.addMessage(this.initialMessage, false);
    }

    // AI начинает диалог с уточняющим вопросом
    this.addAIGreeting();
  }

  addAIGreeting(): void {
    this.isTyping = true;
    
    setTimeout(() => {
      const greetings = [
        'А, понял! Давайте уточним - какое настроение сейчас? Хотите расслабиться или взбодриться?',
        'Хорошо, давайте подберём точнее! Предпочитаете что-то новое или классику?',
        'Отлично! А что насчёт жанра - что больше нравится?',
        'Понятно! Скажите, смотрите один или с кем-то? Это поможет подобрать лучше.'
      ];

      const greeting = greetings[Math.floor(Math.random() * greetings.length)];
      this.addMessage(greeting, true);
      this.isTyping = false;
    }, 1000);
  }

  addMessage(text: string, isAI: boolean): void {
    const message: AIMessage = {
      id: Date.now().toString(),
      text: text,
      isAI: isAI,
      timestamp: new Date()
    };

    this.messages.push(message);

    // Прокрутка вниз
    setTimeout(() => {
      this.scrollToBottom();
    }, 100);
  }

  sendMessage(): void {
    if (!this.currentMessage.trim() || this.isLoading) {
      return;
    }

    const userMessage = this.currentMessage;
    this.addMessage(userMessage, false);
    this.currentMessage = '';
    this.isLoading = true;
    this.isTyping = true;

    // Отправляем в API
    this.apiService.sendAIMessage(this.sessionId, userMessage).subscribe({
      next: (response) => {
        setTimeout(() => {
          this.addMessage(response.response, true);
          this.isLoading = false;
          this.isTyping = false;

          // Проверяем, достаточно ли информации собрано
          if (this.messages.length >= 6 || this.isEnoughInfo(response.response)) {
            setTimeout(() => {
              this.finishDialog();
            }, 1500);
          }
        }, 800);
      },
      error: (error) => {
        console.error('Ошибка AI чата:', error);
        this.isLoading = false;
        this.isTyping = false;
        
        // Фолбэк ответ
        setTimeout(() => {
          this.addMessage('Понял вас! Сейчас подберу фильмы.', true);
          setTimeout(() => {
            this.finishDialog();
          }, 1000);
        }, 500);
      }
    });
  }

  isEnoughInfo(response: string): boolean {
    const finishPhrases = [
      'отлично',
      'прекрасно',
      'понятно',
      'ясно',
      'достаточно',
      'подберу',
      'найду',
      'сейчас'
    ];

    const lowerResponse = response.toLowerCase();
    return finishPhrases.some(phrase => lowerResponse.includes(phrase));
  }

  finishDialog(): void {
    // Собираем все сообщения пользователя в одну строку
    const userMessages = this.messages
      .filter(m => !m.isAI)
      .map(m => m.text)
      .join(' ');

    this.complete.emit(userMessages);
  }

  onCancel(): void {
    this.cancel.emit();
  }

  scrollToBottom(): void {
    const chatContainer = document.querySelector('.messages-container');
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }
}

