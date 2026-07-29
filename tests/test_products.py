from http import HTTPStatus


def test_create_product(client, token):
    expected_price = 4500.00
    expected_name = 'Notebook Gamer'
    response = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': expected_name,
            'description': 'Notebook com placa de vídeo dedicada',
            'price': expected_price,
            'stock': 10,
            'category': 'Eletrônicos',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['name'] == expected_name
    assert data['price'] == expected_price
    assert 'id' in data


def test_create_product_already_exists(client, token):
    client.post(
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


def test_read_products(client, token):
    client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Produto Listagem',
            'description': 'Descrição teste',
            'price': 100.00,
            'stock': 5,
            'category': 'Geral',
        },
    )

    response = client.get('/products/')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'products' in data
    assert len(data['products']) > 0


def test_read_product_by_id(client, token):
    response_create = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Produto ID',
            'description': 'Descrição teste ID',
            'price': 150.00,
            'stock': 2,
            'category': 'Geral',
        },
    )
    product_id = response_create.json()['id']

    response = client.get(f'/products/{product_id}')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == product_id


def test_read_product_not_found(client):
    response = client.get('/products/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'


def test_update_product(client, token):
    response_create = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Produto Update',
            'description': 'Teste',
            'price': 500.00,
            'stock': 10,
            'category': 'Geral',
        },
    )
    product_id = response_create.json()['id']

    expected_price = 4200.00
    expected_stock = 8
    response = client.put(
        f'/products/{product_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'price': expected_price, 'stock': expected_stock},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['price'] == expected_price
    assert data['stock'] == expected_stock


def test_update_product_not_found(client, token):
    response = client.put(
        '/products/999',
        headers={'Authorization': f'Bearer {token}'},
        json={'price': 100.00},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Product not found'


def test_delete_product(client, token):
    response_create = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Produto Delete',
            'description': 'Teste',
            'price': 200.00,
            'stock': 5,
            'category': 'Geral',
        },
    )
    product_id = response_create.json()['id']

    response = client.delete(
        f'/products/{product_id}',
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
