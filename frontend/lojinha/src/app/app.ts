import { Component } from '@angular/core';
import { ProductList } from './product-list/product-list';
import { TaskList } from './task-list/task-list';

@Component({
  selector: 'app-root',
  imports: [ProductList, TaskList],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected title = 'lojinha';
}
