import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export type TaskState = 'draft' | 'todo' | 'doing' | 'done' | 'trash';

export interface Task {
  id: number;
  title: string;
  description: string;
  state: TaskState;
}

export interface TaskInput {
  title: string;
  description: string;
  state: TaskState;
}

const API_URL = 'http://127.0.0.1:8000';

@Injectable({ providedIn: 'root' })
export class TaskService {
  private http = inject(HttpClient);

  getTasks(): Observable<Task[]> {
    return this.http
      .get<{ tasks: Task[] }>(`${API_URL}/tasks/`)
      .pipe(map((response) => response.tasks));
  }

  addTask(task: TaskInput): Observable<Task> {
    return this.http.post<Task>(`${API_URL}/tasks/`, task);
  }

  updateTask(id: number, changes: Partial<TaskInput>): Observable<Task> {
    return this.http.patch<Task>(`${API_URL}/tasks/${id}`, changes);
  }

  deleteTask(id: number): Observable<{ message: string }> {
    return this.http.delete<{ message: string }>(`${API_URL}/tasks/${id}`);
  }
}
