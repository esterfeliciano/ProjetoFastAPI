from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.config.database_settings import get_session
from fast_zero.users.models import User, table_registry
from fast_zero.users.security import get_password_hash


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password
    return user


@pytest.fixture
def token(client, user):
    attempts = [
        (
            '/users/token',
            {'username': user.username, 'password': user.clean_password},
        ),
        (
            '/users/token',
            {'username': user.email, 'password': user.clean_password},
        ),
        (
            '/token',
            {'username': user.username, 'password': user.clean_password},
        ),
        (
            '/token',
            {'username': user.email, 'password': user.clean_password},
        ),
    ]

    last_response = None

    for path, data in attempts:
        last_response = client.post(path, data=data)

        if last_response.status_code == HTTPStatus.OK:
            try:
                payload = last_response.json()
            except ValueError:
                payload = last_response.text

            if isinstance(payload, dict) and 'access_token' in payload:
                return payload['access_token']

    status_code = last_response.status_code if last_response else None
    body = last_response.text if last_response else None

    pytest.fail(
        'Não foi possível gerar o token.'
        f'último status={status_code}, '
        f'body={body}'
    )
