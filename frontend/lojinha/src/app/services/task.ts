import { Injectable } from '@angular/core';

export type TaskState = 'draft' | 'todo' | 'doing' | 'done' | 'trash';

export interface Task {
  id: number;
  title: string;
  description: string;
  state: TaskState;
}

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private tasks: Task[] = [
    { id: 1, title: 'Cadastrar produtos', description: 'Subir catálogo inicial', state: 'doing' },
    { id: 2, title: 'Configurar CORS', description: 'Liberar acesso do Angular', state: 'todo' },
    { id: 3, title: 'Criar componente de login', description: '', state: 'done' },
  ];

  getTasks(): Task[] {
    return this.tasks;
  }
}
