import { Component } from '@angular/core';

type TaskState = 'draft' | 'todo' | 'doing' | 'done' | 'trash';

interface Task {
  id: number;
  title: string;
  description: string;
  state: TaskState;
}

@Component({
  selector: 'app-task-list',
  imports: [],
  templateUrl: './task-list.html',
  styleUrl: './task-list.css'
})
export class TaskList {
  tasks: Task[] = [
    { id: 1, title: 'Cadastrar produtos', description: 'Subir catálogo inicial', state: 'doing' },
    { id: 2, title: 'Configurar CORS', description: 'Liberar acesso do Angular', state: 'todo' },
    { id: 3, title: 'Criar componente de login', description: '', state: 'done' },
  ];
}