from http import HTTPStatus


def test_add_to_cart(client, token):
    expected_price = 99.90
    expected_quantity = 2
    expected_name = 'Camisa FastAPI'

    response = client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': expected_name,
            'price': expected_price,
            'quantity': expected_quantity,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['items'][0]['product_name'] == expected_name
    assert data['items'][0]['price'] == expected_price
    assert data['items'][0]['quantity'] == expected_quantity


def test_get_cart(client, token):
    expected_name = 'Caneca Teste'
    expected_price = 35.00
    expected_quantity = 1

    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': expected_name,
            'price': expected_price,
            'quantity': expected_quantity,
        },
    )

    response = client.get(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) > 0
    assert data['items'][0]['product_name'] == expected_name


def test_checkout_cart(client, token):
    expected_name = 'Adesivo'

    client.post(
        '/cart/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'product_name': expected_name,
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
    assert expected_name in data['whatsapp_url']


def test_checkout_empty_cart(client, token):
    response = client.post(
        '/cart/checkout',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Cart is empty'
