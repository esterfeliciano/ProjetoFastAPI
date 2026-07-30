import { Component, inject, signal, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { ProductService, Product } from '../services/product';
import { CartService } from '../services/cart';
import { AuthService } from '../services/auth';
import { ProductImageService } from '../services/product-image';

@Component({
  selector: 'app-product-list',
  imports: [RouterLink],
  templateUrl: './product-list.html',
  styleUrl: './product-list.css'
})
export class ProductList implements OnInit {
  private productService = inject(ProductService);
  private cartService = inject(CartService);
  private productImageService = inject(ProductImageService);
  authService = inject(AuthService);

  products = signal<Product[]>([]);
  loading = signal(true);
  errorMessage = signal<string | null>(null);
  addedMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.loading.set(true);
    this.productService.getProducts().subscribe({
      next: (products) => {
        this.products.set(products);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Não foi possível carregar o catálogo. O backend está rodando?');
        this.loading.set(false);
      },
    });
  }

  getImage(productId: number): string | null {
    return this.productImageService.getImage(productId);
  }

  adicionarAoCarrinho(product: Product): void {
    this.cartService
      .addItem({
        product_name: product.name,
        price: product.price,
        quantity: 1,
      })
      .subscribe({
        next: () => {
          this.addedMessage.set(`${product.name} adicionado ao carrinho!`);
          setTimeout(() => this.addedMessage.set(null), 2000);
        },
        error: () => {
          this.addedMessage.set('Erro ao adicionar ao carrinho.');
        },
      });
  }

  removerProduto(product: Product): void {
    if (!confirm(`Remover "${product.name}" do catálogo?`)) return;

    this.productService.deleteProduct(product.id).subscribe({
      next: () => {
        this.productImageService.removeImage(product.id);
        this.products.update((current) => current.filter((p) => p.id !== product.id));
      },
      error: () => {
        this.errorMessage.set('Não foi possível remover o produto.');
      },
    });
  }
}