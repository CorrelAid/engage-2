from .base import database_test


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


@database_test
async def test_get_projects(async_client, admin_details):
    async with async_client as ac:
        auth_cookie_header = await get_auth_cookie_header(ac, admin_details)
        response = await ac.get("/projects/", headers=auth_cookie_header)
        assert response.status_code == 200
        assert len(response.json()) >= 1


@database_test
async def test_project_crud(async_client, admin_details):
    project = {
        "title": "Inserted Project",
        "status": "running",
    }

    async with async_client as ac:
        auth_cookie_header = await get_auth_cookie_header(ac, admin_details)

        response = await ac.post("/projects/", headers=auth_cookie_header, json=project)
        assert response.status_code == 201

        project_id = response.json()["id"]

        response = await ac.get(f"/projects/{project_id}", headers=auth_cookie_header)
        assert response.status_code == 200
        assert response.json()["title"] == project["title"]
        assert response.json()["status"] == project["status"]
        assert response.json()["summary"] is None

        project["title"] = "Updated Project"
        project["summary"] = "Updated Summary"

        response = await ac.patch(
            f"/projects/{project_id}", headers=auth_cookie_header, json=project
        )
        response = await ac.get(f"/projects/{project_id}", headers=auth_cookie_header)
        assert response.status_code == 200
        assert response.json()["title"] == project["title"]
        assert response.json()["status"] == project["status"]
        assert response.json()["summary"] == project["summary"]

        response = await ac.delete(
            f"/projects/{project_id}", headers=auth_cookie_header
        )
        assert response.status_code == 204

        response = await ac.get(f"/projects/{project_id}", headers=auth_cookie_header)
        assert response.status_code == 404
