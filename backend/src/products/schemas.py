from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str


class ProductPublic(ProductSchema):
    id: int


class ProductList(BaseModel):
    products: list[ProductPublic]


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category: str | None = None
