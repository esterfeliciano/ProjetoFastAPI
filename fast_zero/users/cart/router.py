from http import HTTPStatus
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.users.cart.models import CartItemModel, CartModel
from fast_zero.users.cart.schemas import (
    CartItemSchema,
    CartPublic,
    CheckoutResponse,
)
from fast_zero.config.database_settings import get_session
from fast_zero.users.models import User
from fast_zero.users.security import get_current_user

router = APIRouter(tags=['cart'])


@router.post(
    '/cart/',
    status_code=HTTPStatus.CREATED,
    response_model=CartPublic,
)
def add_to_cart(
    item: CartItemSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.user_id == current_user.id)
    )

    if not cart:
        cart = CartModel(user_id=current_user.id)
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
    current_user: User = Depends(get_current_user),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.user_id == current_user.id)
    )

    if not cart:
        return {'id': 0, 'items': []}

    return cart


@router.post(
    '/cart/checkout',
    status_code=HTTPStatus.OK,
    response_model=CheckoutResponse,
)
def checkout_cart(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    cart = session.scalar(
        select(CartModel).where(CartModel.user_id == current_user.id)
    )

    if not cart or not cart.items:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Cart is empty',
        )

    mensagem = (
        'Olá! Gostaria de finalizar o meu pedido:\n\n'
        f'*Cliente:* {current_user.username}\n\n'
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

    numero_whatsapp = '5581999999999'

    texto_codificado = quote(mensagem)
    whatsapp_url = (
        f'https://api.whatsapp.com/send?'
        f'phone={numero_whatsapp}&text={texto_codificado}'
    )

    for item in cart.items:
        session.delete(item)
    session.commit()

    return {'whatsapp_url': whatsapp_url}
