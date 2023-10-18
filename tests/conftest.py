import pytest

from app.main import create_app
from app.models import User


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def new_user():
    return User(id=10, name="TestName", token="testtoken")


@pytest.fixture()
def header():
    return {"api-key": "test"}
