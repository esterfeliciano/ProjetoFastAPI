from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_produto(client):
    response = client.post(
        '/produtos/',
        json={
            'nome': 'Teclado mecânico',
            'preco': 250.90,
            'quantidade_estoque': 15,
            'categoria': 'periféricos',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'nome': 'Teclado mecânico',
        'preco': 250.90,
        'quantidade_estoque': 15,
        'categoria': 'periféricos',
    }


def test_read_produtos(client):
    response = client.get('/produtos/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'produtos': [
            {
                'id': 1,
                'nome': 'Teclado mecânico',
                'preco': 250.90,
                'quantidade_estoque': 15,
                'categoria': 'periféricos',
            }
        ]
    }


def test_update_produto(client):
    response = client.put(
        '/produtos/1',
        json={
            'nome': 'Teclado mecânico RGB',
            'preco': 279.90,
            'quantidade_estoque': 12,
            'categoria': 'periféricos',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['nome'] == 'Teclado mecânico RGB'


def test_delete_produto(client):
    response = client.delete('/produtos/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Produto deleted'}
