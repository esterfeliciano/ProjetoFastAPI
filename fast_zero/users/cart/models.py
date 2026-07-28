from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    relationship,
)

from fast_zero.users.models import (
    table_registry,  # Utiliza o mesmo registry do projeto
)


@mapped_as_dataclass(table_registry)
class CartModel:
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)

    items: Mapped[list['CartItemModel']] = relationship(
        init=False, back_populates='cart', cascade='all, delete-orphan'
    )


@mapped_as_dataclass(table_registry)
class CartItemModel:
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'))
    product_name: Mapped[str]
    price: Mapped[float]
    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped[CartModel] = relationship(init=False, back_populates='items')
