import pytest
from api.app import app
from httpx import AsyncClient


@pytest.fixture()
def async_client():
    return AsyncClient(app=app, base_url="http://test")
