from pydantic import BaseModel


class CartItemSchema(BaseModel):
    product_name: str
    price: float
    quantity: int = 1


class CartItemPublic(CartItemSchema):
    id: int


class CartPublic(BaseModel):
    id: int
    items: list[CartItemPublic]


class CheckoutResponse(BaseModel):
    whatsapp_url: str
