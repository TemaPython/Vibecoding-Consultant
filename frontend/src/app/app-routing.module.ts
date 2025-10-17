import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { PreferencesInputComponent } from './components/preferences-input/preferences-input.component';
import { MovieCardComponent } from './components/movie-card/movie-card.component';
import { FinalSelectionComponent } from './components/final-selection/final-selection.component';

const routes: Routes = [
  { path: '', component: WelcomeComponent },
  { path: 'preferences', component: PreferencesInputComponent },
  { path: 'preferences/:sessionId', component: PreferencesInputComponent },
  { path: 'movies', component: MovieCardComponent },
  { path: 'movies/:sessionId', component: MovieCardComponent },
  { path: 'final', component: FinalSelectionComponent },
  { path: 'final/:sessionId', component: FinalSelectionComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

