from http import HTTPStatus


def test_create_product(client, token):
    response = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Notebook Gamer',
            'description': 'Notebook com placa de vídeo dedicada',
            'price': 4500.00,
            'stock': 10,
            'category': 'Eletrônicos',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == 'Notebook Gamer'
    assert data['price'] == 4500.00
    assert 'id' in data


def test_create_product_already_exists(client, token):
    response = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Notebook Gamer',
            'description': 'Outra descrição',
            'price': 4000.00,
            'stock': 5,
            'category': 'Eletrônicos',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Product already exists'


def test_read_products(client):
    response = client.get('/products/')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'products' in data
    assert len(data['products']) > 0


def test_read_product_by_id(client):
    response = client.get('/products/1')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == 1


def test_read_product_not_found(client):
    response = client.get('/products/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'


def test_update_product(client, token):
    response = client.put(
        '/products/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'price': 4200.00, 'stock': 8},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['price'] == 4200.00
    assert data['stock'] == 8


def test_update_product_not_found(client, token):
    response = client.put(
        '/products/999',
        headers={'Authorization': f'Bearer {token}'},
        json={'price': 100.00},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'


def test_delete_product(client, token):
    response = client.delete(
        '/products/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'Product deleted successfully'


def test_delete_product_not_found(client, token):
    response = client.delete(
        '/products/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'