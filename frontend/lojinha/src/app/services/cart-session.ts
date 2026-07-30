import { Injectable } from '@angular/core';

const STORAGE_KEY = 'lojinha_session_id';

@Injectable({
  providedIn: 'root'
})
export class CartSessionService {
  private sessionId: string;

  constructor() {
    let stored = localStorage.getItem(STORAGE_KEY);

    if (!stored) {
      stored = crypto.randomUUID();
      localStorage.setItem(STORAGE_KEY, stored);
    }

    this.sessionId = stored;
  }

  getSessionId(): string {
    return this.sessionId;
  }
}
