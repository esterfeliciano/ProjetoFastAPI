from http import HTTPStatus
from urllib.parse import quote

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config.database_settings import get_session
from src.users.cart.models import CartItemModel, CartModel
from src.users.cart.schemas import (
    CartItemSchema,
    CartPublic,
    CheckoutResponse,
)

router = APIRouter(tags=['cart'])


class CheckoutSchema(BaseModel):
    payment_method: str = 'Pix'
    customer_name: str = 'Cliente'


def get_session_id(x_session_id: str = Header(alias='X-Session-Id')) -> str:
    return x_session_id


@router.post(
    '/cart/',
    status_code=HTTPStatus.CREATED,
    response_model=CartPublic,
)
def add_to_cart(
    item: CartItemSchema,
    session: Session = Depends(get_session),
    session_id: str = Depends(get_session_id),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.session_id == session_id)
    )

    if not cart:
        cart = CartModel(session_id=session_id)
        session.add(cart)
        session.commit()
        session.refresh(cart)

    db_item = CartItemModel(
        cart_id=cart.id,
        product_name=item.product_name,
        price=item.price,
        quantity=item.quantity,
    )

    session.add(db_item)
    session.commit()
    session.refresh(cart)

    return cart


@router.get(
    '/cart/',
    status_code=HTTPStatus.OK,
    response_model=CartPublic,
)
def get_cart(
    session: Session = Depends(get_session),
    session_id: str = Depends(get_session_id),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.session_id == session_id)
    )

    if not cart:
        return {'id': 0, 'items': []}

    return cart


@router.delete(
    '/cart/items/{item_id}',
    status_code=HTTPStatus.OK,
)
def remove_cart_item(
    item_id: int,
    session: Session = Depends(get_session),
    session_id: str = Depends(get_session_id),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.session_id == session_id)
    )

    if not cart:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Cart not found',
        )

    item = session.scalar(
        select(CartItemModel).where(
            CartItemModel.id == item_id,
            CartItemModel.cart_id == cart.id,
        )
    )

    if not item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Item not found in this cart',
        )

    session.delete(item)
    session.commit()

    return {'message': 'Item removed successfully'}


@router.post(
    '/cart/checkout',
    status_code=HTTPStatus.OK,
    response_model=CheckoutResponse,
)
def checkout_cart(
    checkout_data: CheckoutSchema | None = None,
    session: Session = Depends(get_session),
    session_id: str = Depends(get_session_id),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.session_id == session_id)
    )

    if not cart or not cart.items:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Cart is empty',
        )

    payment_method = checkout_data.payment_method if checkout_data else 'Pix'
    customer_name = checkout_data.customer_name if checkout_data else 'Cliente'

    mensagem = (
        'Olá! Gostaria de finalizar o meu pedido:\n\n'
        f'*Cliente:* {customer_name}\n'
        f'*Forma de Pagamento:* {payment_method}\n\n'
    )
    total = 0.0

    for item in cart.items:
        subtotal = item.price * item.quantity
        total += subtotal
        mensagem += (
            f'- {item.quantity}x {item.product_name} '
            f'(R$ {item.price:.2f} un) = R$ {subtotal:.2f}\n'
        )

    mensagem += f'\n*Total do Pedido: R$ {total:.2f}*'

    numero_whatsapp = '5581983960846'

    texto_codificado = quote(mensagem)
    whatsapp_url = (
        f'https://api.whatsapp.com/send?'
        f'phone={numero_whatsapp}&text={texto_codificado}'
    )

    for item in cart.items:
        session.delete(item)
    session.commit()

    return {'whatsapp_url': whatsapp_url}
