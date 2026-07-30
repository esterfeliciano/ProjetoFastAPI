import { Component, inject, signal, OnInit } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { TaskService, Task } from '../services/task';

@Component({
  selector: 'app-task-list',
  imports: [ReactiveFormsModule],
  templateUrl: './task-list.html',
  styleUrl: './task-list.css'
})
export class TaskList implements OnInit {
  private taskService = inject(TaskService);
  private fb = inject(FormBuilder);

  tasks = signal<Task[]>([]);
  loading = signal(true);
  errorMessage = signal<string | null>(null);

  form = this.fb.group({
    title: ['', Validators.required],
    description: [''],
  });

  ngOnInit(): void {
    this.loadTasks();
  }

  loadTasks(): void {
    this.loading.set(true);
    this.taskService.getTasks().subscribe({
      next: (tasks) => {
        this.tasks.set(tasks);
        this.loading.set(false);
      },
      error: () => {
        this.errorMessage.set('Não foi possível carregar as tarefas.');
        this.loading.set(false);
      },
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const { title, description } = this.form.value;

    this.taskService
      .addTask({
        title: title!,
        description: description ?? '',
        state: 'todo',
      })
      .subscribe({
        next: (task) => {
          this.tasks.update((current) => [...current, task]);
          this.form.reset();
        },
        error: () => {
          this.errorMessage.set('Não foi possível criar a tarefa.');
        },
      });
  }

  marcarComoConcluida(task: Task): void {
    this.taskService.updateTask(task.id, { state: 'done' }).subscribe({
      next: (updated) => {
        this.tasks.update((current) =>
          current.map((t) => (t.id === updated.id ? updated : t))
        );
      },
    });
  }

  excluirTarefa(task: Task): void {
    this.taskService.deleteTask(task.id).subscribe({
      next: () => {
        this.tasks.update((current) => current.filter((t) => t.id !== task.id));
      },
    });
  }
}
