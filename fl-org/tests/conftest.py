import pytest
import sys
from app.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    print(sys.path)
    return app.test_client()