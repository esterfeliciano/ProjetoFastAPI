from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.products.router import router as products_router
from fast_zero.tasks.router import router as task_router
from fast_zero.backend.src.users.cart.router import router as cart_router
from fast_zero.backend.src.users.router import router as users_router

app = FastAPI()
app.include_router(task_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(cart_router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}
