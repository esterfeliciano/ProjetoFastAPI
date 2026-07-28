from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.users.router import router as users_router

app = FastAPI()

app.include_router(users_router)


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá Mundo!'}
