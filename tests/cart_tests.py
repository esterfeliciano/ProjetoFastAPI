from http import HTTPStatus


def test_add_to_cart(client, token):
    response = client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Camisa FastAPI',
            'price': 99.90,
            'quantity': 2,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['items'][0]['product_name'] == 'Camisa FastAPI'
    assert data['items'][0]['price'] == 99.90
    assert data['items'][0]['quantity'] == 2


def test_get_cart(client, token):
    # Adiciona um item primeiro
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Caneca Teste',
            'price': 35.00,
            'quantity': 1,
        },
    )

    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) > 0
    assert data['items'][0]['product_name'] == 'Caneca Teste'


def test_checkout_cart(client, token):
    # Adiciona item para poder fechar o pedido
    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': 'Adesivo',
            'price': 10.00,
            'quantity': 3,
        },
    )

    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'whatsapp_url' in data
    assert 'api.whatsapp.com/send' in data['whatsapp_url']
    assert 'Adesivo' in data['whatsapp_url']


def test_checkout_empty_cart(client, token):
    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Cart is empty'