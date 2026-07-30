import { Injectable } from '@angular/core';

const STORAGE_PREFIX = 'lojinha_product_image_';

@Injectable({ providedIn: 'root' })
export class ProductImageService {
  saveImage(productId: number, base64: string): boolean {
    try {
      localStorage.setItem(`${STORAGE_PREFIX}${productId}`, base64);
      return true;
    } catch (err) {
      console.error('Erro ao salvar imagem no localStorage:', err);
      return false;
    }
  }

  getImage(productId: number): string | null {
    return localStorage.getItem(`${STORAGE_PREFIX}${productId}`);
  }

  removeImage(productId: number): void {
    localStorage.removeItem(`${STORAGE_PREFIX}${productId}`);
  }
}