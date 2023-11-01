from .base import database_test


@database_test
async def test_login(async_client, admin_details):
    async with async_client as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "username": admin_details["email"],
                "password": admin_details["password"],
            },
        )
    assert response.status_code == 204


@database_test
async def test_login_bad_password(async_client, admin_details):
    async with async_client as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "username": admin_details["email"],
                "password": "bad_password",  # pragma: allowlist secret
            },
        )
    # fastapi_users returns 400 instead of 401 for bad password
    assert response.status_code == 400


@database_test
async def test_login_bad_username(async_client, admin_details):
    async with async_client as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "username": "bad_username",
                "password": admin_details["password"],
            },
        )
    # fastapi_users returns 400 instead of 401 for bad username
    assert response.status_code == 400


@database_test
async def test_authenticated_route(async_client, admin_details):
    async with async_client as ac:
        login_response = await ac.post(
            "/auth/login",
            data={
                "username": admin_details["email"],
                "password": admin_details["password"],
            },
        )
        assert login_response.status_code == 204
        response = await ac.get(
            "/auth/me",
            headers={"Cookie": login_response.headers["Set-Cookie"]},
        )
        assert response.status_code == 200
