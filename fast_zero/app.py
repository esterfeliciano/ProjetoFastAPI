from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    ProdutoDB,
    ProdutoList,
    ProdutoPublic,
    ProdutoSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post(
    '/produtos/',
    status_code=HTTPStatus.CREATED,
    response_model=ProdutoPublic,
)
def create_produto(produto: ProdutoSchema):
    produto_com_id = ProdutoDB(**produto.model_dump(), id=len(database) + 1)
    database.append(produto_com_id)
    return produto_com_id


@app.get('/produtos/', response_model=ProdutoList)
def read_produtos():
    return {'produtos': database}


@app.put('/produtos/{produto_id}', response_model=ProdutoPublic)
def update_produto(produto_id: int, produto: ProdutoSchema):
    if produto_id > len(database) or produto_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto not found'
        )

    produto_com_id = ProdutoDB(**produto.model_dump(), id=produto_id)
    database[produto_id - 1] = produto_com_id

    return produto_com_id


@app.delete('/produtos/{produto_id}', response_model=Message)
def delete_produto(produto_id: int):
    if produto_id > len(database) or produto_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Produto not found'
        )

    del database[produto_id - 1]

    return {'message': 'Produto deleted'}
