import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductService } from '../services/product';

@Component({
  selector: 'app-product-form',
  imports: [ReactiveFormsModule],
  templateUrl: './product-form.html',
  styleUrl: './product-form.css'
})
export class ProductForm {
  private fb = inject(FormBuilder);
  private productService = inject(ProductService);
  private router = inject(Router);

  imagePreview = signal<string | null>(null);
  errorMessage = signal<string | null>(null);
  saving = signal(false);

  form = this.fb.group({
    name: ['', Validators.required],
    description: ['', Validators.required],
    price: [0, [Validators.required, Validators.min(0.01)]],
    stock: [0, [Validators.required, Validators.min(0)]],
    category: ['', Validators.required],
  });

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    if (file.type !== 'image/png') {
      alert('Por enquanto só aceitamos arquivos PNG.');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      this.imagePreview.set(reader.result as string);
    };
    reader.readAsDataURL(file);
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const { name, description, price, stock, category } = this.form.value;
    this.saving.set(true);
    this.errorMessage.set(null);

    // Nota: o upload real da foto ainda não é suportado pelo backend.
    // O preview aqui é só visual, pra já deixar a UX pronta pro dia
    // em que a rota de upload de imagem existir na API.
    this.productService
      .addProduct({
        name: name!,
        description: description!,
        price: price!,
        stock: stock!,
        category: category!,
      })
      .subscribe({
        next: () => {
          this.saving.set(false);
          this.router.navigate(['/products']);
        },
        error: (err) => {
          this.saving.set(false);
          if (err.status === 400) {
            this.errorMessage.set('Já existe um produto com esse nome.');
          } else if (err.status === 401) {
            this.errorMessage.set('Sessão expirada. Faça login novamente.');
          } else {
            this.errorMessage.set('Não foi possível salvar o produto.');
          }
        },
      });
  }
}
