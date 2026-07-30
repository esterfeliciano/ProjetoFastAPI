import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CartSessionService } from './cart-session';

export interface CartItemInput {
  product_name: string;
  price: number;
  quantity?: number;
}

export interface CartItem extends CartItemInput {
  id: number;
  quantity: number;
}

export interface Cart {
  id: number;
  items: CartItem[];
}

export interface CheckoutResponse {
  whatsapp_url: string;
}

const API_URL = 'http://127.0.0.1:8000';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private http = inject(HttpClient);
  private cartSession = inject(CartSessionService);

  private get headers(): HttpHeaders {
    return new HttpHeaders({
      'X-Session-Id': this.cartSession.getSessionId(),
    });
  }

  getCart(): Observable<Cart> {
    return this.http.get<Cart>(`${API_URL}/cart/`, { headers: this.headers });
  }

  addItem(item: CartItemInput): Observable<Cart> {
    return this.http.post<Cart>(`${API_URL}/cart/`, item, { headers: this.headers });
  }

  checkout(paymentMethod: string, customerName: string): Observable<CheckoutResponse> {
    return this.http.post<CheckoutResponse>(
      `${API_URL}/cart/checkout`,
      { payment_method: paymentMethod, customer_name: customerName },
      { headers: this.headers }
    );
  }
}
