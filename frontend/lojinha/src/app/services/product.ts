import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
}

export interface ProductInput {
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
}

const API_URL = 'http://127.0.0.1:8000';

@Injectable({ providedIn: 'root' })
export class ProductService {
  private http = inject(HttpClient);

  getProducts(): Observable<Product[]> {
    return this.http
      .get<{ products: Product[] }>(`${API_URL}/products/`)
      .pipe(map((response) => response.products));
  }

  addProduct(product: ProductInput): Observable<Product> {
    return this.http.post<Product>(`${API_URL}/products/`, product);
  }

  deleteProduct(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${API_URL}/products/${id}`);
  }
}
