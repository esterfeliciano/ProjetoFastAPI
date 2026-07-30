import { Component } from '@angular/core';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
}

@Component({
  selector: 'app-product-list',
  imports: [],
  templateUrl: './product-list.html',
  styleUrl: './product-list.css'
})
export class ProductList {
  products: Product[] = [
    { id: 1, name: 'Camiseta Preta', description: 'Algodão 100%', price: 59.9, stock: 12, category: 'Roupas' },
    { id: 2, name: 'Caneca Térmica', description: '450ml, inox', price: 39.9, stock: 30, category: 'Casa' },
    { id: 3, name: 'Boné Aba Reta', description: 'Ajustável', price: 49.9, stock: 0, category: 'Acessórios' },
  ];
}