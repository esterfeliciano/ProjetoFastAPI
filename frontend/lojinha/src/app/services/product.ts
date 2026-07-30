import { Injectable } from '@angular/core';

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private products: Product[] = [
    { id: 1, name: 'Camiseta Preta', description: 'Algodão 100%', price: 59.9, stock: 12, category: 'Roupas' },
    { id: 2, name: 'Caneca Térmica', description: '450ml, inox', price: 39.9, stock: 30, category: 'Casa' },
    { id: 3, name: 'Boné Aba Reta', description: 'Ajustável', price: 49.9, stock: 0, category: 'Acessórios' },
  ];

  getProducts(): Product[] {
    return this.products;
  }
}