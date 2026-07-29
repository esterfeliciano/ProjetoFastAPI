from http import HTTPStatus


def task_payload(**overrides):
    payload = {
        'title': 'Estudar SQLAlchemy',
        'description': 'Revisar relacionamentos e queries',
        'state': 'todo',
    }
    payload.update(overrides)
    return payload


def test_create_task(client, token):
    response = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json=task_payload(),
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['title'] == 'Estudar SQLAlchemy'
    assert response.json()['state'] == 'todo'


def test_list_tasks_empty(client, token):
    response = client.get(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'tasks': []}


def test_list_tasks_returns_only_own_tasks(client, token, other_user, session):
    client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json=task_payload(),
    )

    other_login = client.post(
        '/token',
        data={
            'username': other_user.email,
            'password': other_user.clean_password,
        },
    )
    other_token = other_login.json()['access_token']

    response = client.get(
        '/tasks/',
        headers={'Authorization': f'Bearer {other_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'tasks': []}


def test_list_tasks_filter_by_state(client, token):
    client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json=task_payload(state='todo'),
    )
    client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json=task_payload(title='Outra tarefa', state='doing'),
    )

    response = client.get(
        '/tasks/?state=doing',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tasks']) == 1
    assert response.json()['tasks'][0]['title'] == 'Outra tarefa'


def test_patch_task(client, token):
    created = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json=task_payload(),
    ).json()

    response = client.patch(
        f'/tasks/{created["id"]}',
        headers={'Authorization': f'Bearer {token}'},
        json={'state': 'done'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['state'] == 'done'
    assert response.json()['title'] == 'Estudar SQLAlchemy'


def test_patch_task_not_found(client, token):
    response = client.patch(
        '/tasks/999',
        headers={'Authorization': f'Bearer {token}'},
        json={'state': 'done'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_task(client, token):
    created = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json=task_payload(),
    ).json()

    response = client.delete(
        f'/tasks/{created["id"]}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_delete_task_not_found(client, token):
    response = client.delete(
        '/tasks/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
