import pytest
from settings import settings

database_test = pytest.mark.skipif(
    not settings.tests.test_database, reason="Database tests disabled"
)


async def get_auth_cookie_header(connected_async_client, admin_details):
    login_response = await connected_async_client.post(
        "/auth/login",
        data={
            "username": admin_details["email"],
            "password": admin_details["password"],
        },
    )
    assert login_response.status_code == 204
    return {"Cookie": login_response.headers["Set-Cookie"]}
