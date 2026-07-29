from http import HTTPStatus


def test_create_task(client, token):
    response = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Estudar FastAPI',
            'description': 'Terminar o CRUD de tasks',
            'state': 'todo',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['title'] == 'Estudar FastAPI'
    assert data['state'] == 'todo'
    assert 'id' in data


def test_list_tasks(client, token):
    response = client.get(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'tasks' in data


def test_patch_task(client, token):
    response_create = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Tarefa para atualizar',
            'description': 'Descrição antiga',
            'state': 'draft',
        },
    )
    task_id = response_create.json()['id']

    response = client.patch(
        f'/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Tarefa atualizada', 'state': 'doing'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['title'] == 'Tarefa atualizada'
    assert data['state'] == 'doing'


def test_delete_task(client, token):
    response_create = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Tarefa para deletar',
            'description': 'Descrição',
            'state': 'trash',
        },
    )
    task_id = response_create.json()['id']

    response = client.delete(
        f'/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Task has been deleted successfully.'
