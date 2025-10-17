export interface Movie {
  id: string;
  title: string;
  poster: string;
  rating: number;
  year: number;
  actors: string[];
  description: string;
  okkoUrl: string;
  genre?: string[];
}

export interface UserPreferences {
  userId: string;
  preferences: string;
  mood?: string;
}

export interface Session {
  sessionId: string;
  mode: 'single' | 'duo';
  user1Preferences?: UserPreferences;
  user2Preferences?: UserPreferences;
  likedMovies: string[];
  dislikedMovies: string[];
  user1Likes?: string[];
  user2Likes?: string[];
}

export interface AIMessage {
  id: string;
  text: string;
  isAI: boolean;
  timestamp: Date;
}

