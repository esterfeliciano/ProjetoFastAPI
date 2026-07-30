import { Component, inject, signal, OnInit, computed } from '@angular/core';
import { CartService, Cart } from '../services/cart';

@Component({
  selector: 'app-cart-view',
  imports: [],
  templateUrl: './cart-view.html',
  styleUrl: './cart-view.css'
})
export class CartView implements OnInit {
  private cartService = inject(CartService);

  cart = signal<Cart>({ id: 0, items: [] });
  loading = signal(true);
  errorMessage = signal<string | null>(null);
  whatsappUrl = signal<string | null>(null);

  total = computed(() =>
    this.cart().items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.loading.set(true);
    this.cartService.getCart().subscribe({
      next: (cart) => {
        this.cart.set(cart);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Não foi possível carregar o carrinho.');
        this.loading.set(false);
      },
    });
  }

  finalizarPedido(): void {
    this.cartService.checkout('Pix', 'Cliente').subscribe({
      next: (response) => {
        this.whatsappUrl.set(response.whatsapp_url);
        this.cart.set({ id: 0, items: [] });
      },
      error: () => {
        this.errorMessage.set('Não foi possível finalizar o pedido. O carrinho está vazio?');
      },
    });
  }
}
