import { Routes } from '@angular/router';
import { Home } from './home/home';
import { ProductList } from './product-list/product-list';
import { ProductForm } from './product-form/product-form';
import { CartView } from './cart-view/cart-view';
import { Login } from './login/login';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'products', component: ProductList },
  { path: 'products/new', component: ProductForm, canActivate: [authGuard] },
  { path: 'cart', component: CartView },
  { path: 'login', component: Login },
];
