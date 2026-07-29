from http import HTTPStatus


def cart_item_payload(**overrides):
    payload = {
        'product_name': 'Mouse sem fio',
        'price': 89.90,
        'quantity': 2,
    }
    payload.update(overrides)
    return payload


def test_add_to_cart_creates_cart(client, token):
    response = client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json=cart_item_payload(),
    )
    assert response.status_code == HTTPStatus.CREATED
    assert len(response.json()['items']) == 1
    assert response.json()['items'][0]['product_name'] == 'Mouse sem fio'


def test_add_multiple_items_to_same_cart(client, token):
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json=cart_item_payload(),
    )
    response = client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json=cart_item_payload(
            product_name='Teclado', price=150.0, quantity=1
        ),
    )
    assert response.status_code == HTTPStatus.CREATED
    assert len(response.json()['items']) == 2  # noqa: PLR2004


def test_get_empty_cart(client, token):
    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 0, 'items': []}


def test_get_cart_with_items(client, token):
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json=cart_item_payload(),
    )
    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['items']) == 1


def test_checkout_empty_cart_fails(client, token):
    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_checkout_cart_success(client, token):
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json=cart_item_payload(),
    )
    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
        json={'payment_method': 'Cartão'},
    )
    assert response.status_code == HTTPStatus.OK
    assert 'whatsapp_url' in response.json()
    assert 'api.whatsapp.com' in response.json()['whatsapp_url']


def test_checkout_clears_cart(client, token):
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json=cart_item_payload(),
    )
    client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
    )
    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.json()['items'] == []
