from pydantic import BaseModel


class Message(BaseModel):
    message: str


class ProdutoSchema(BaseModel):
    nome: str
    preco: float
    quantidade_estoque: int
    categoria: str | None = None


class ProdutoPublic(ProdutoSchema):
    id: int


class ProdutoDB(ProdutoSchema):
    id: int


class ProdutoList(BaseModel):
    produtos: list[ProdutoPublic]
