from http import HTTPStatus


def test_add_to_cart(client, token):
    response = client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Notebook Gamer',
            'price': 4500.00,
            'quantity': 1,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert 'id' in data
    assert len(data['items']) == 1
    assert data['items'][0]['product_name'] == 'Notebook Gamer'


def test_get_cart_empty(client, token):
    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['items'] == []


def test_get_cart_with_items(client, token):
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Mouse Gamer',
            'price': 150.00,
            'quantity': 2,
        },
    )

    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) > 0
    assert data['items'][0]['product_name'] == 'Mouse Gamer'


def test_checkout_cart_empty(client, token):
    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
        json={'payment_method': 'Pix'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Cart is empty'


def test_checkout_cart_success(client, token):
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Teclado Mecânico',
            'price': 350.00,
            'quantity': 1,
        },
    )

    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
        json={'payment_method': 'Cartão de Crédito'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'whatsapp_url' in data
    assert 'api.whatsapp.com' in data['whatsapp_url']
