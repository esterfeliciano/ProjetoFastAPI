from http import HTTPStatus


def create_product_payload(**overrides):
    payload = {
        'name': 'Teclado mecânico',
        'description': 'Teclado mecânico RGB switch marrom',
        'price': 250.90,
        'stock': 15,
        'category': 'periféricos',
    }
    payload.update(overrides)
    return payload


def test_create_product(client, token):
    response = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Teclado mecânico'
    assert response.json()['price'] == 250.90  # noqa: PLR2004


def test_create_product_already_exists(client, token):
    client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    )
    response = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_products(client, token):
    client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    )
    response = client.get('/products/')
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == 1


def test_read_product_by_id(client, token):
    created = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    ).json()

    response = client.get(f'/products/{created["id"]}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'Teclado mecânico'


def test_read_product_not_found(client):
    response = client.get('/products/999')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_product(client, token):
    created = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    ).json()

    response = client.put(
        f'/products/{created["id"]}',
        headers={'Authorization': f'Bearer {token}'},
        json={'price': 199.90},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['price'] == 199.90  # noqa: PLR2004
    assert response.json()['name'] == 'Teclado mecânico'


def test_update_product_not_found(client, token):
    response = client.put(
        '/products/999',
        headers={'Authorization': f'Bearer {token}'},
        json={'price': 199.90},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_product(client, token):
    created = client.post(
        '/products/',
        headers={'Authorization': f'Bearer {token}'},
        json=create_product_payload(),
    ).json()

    response = client.delete(
        f'/products/{created["id"]}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Product deleted successfully'}


def test_delete_product_not_found(client, token):
    response = client.delete(
        '/products/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
