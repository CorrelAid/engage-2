from .base import database_test, get_auth_cookie_header


@database_test
async def test_get_comments(async_client, admin_details):
    async with async_client as ac:
        auth_cookie_header = await get_auth_cookie_header(ac, admin_details)
        response = await ac.get("/comments/", headers=auth_cookie_header)
        assert response.status_code == 200
        assert len(response.json()) >= 1


async def test_comments_crud_no_db(
    async_client, override_comment_store, override_active_user
):
    comment = {
        "text": "Interesting comment message",
    }

    async with async_client as ac:
        response = await ac.post("/comments/", json=comment)
        assert response.status_code == 201

        comment_id = response.json()["id"]

        response = await ac.get(f"/comments/{comment_id}")
        assert response.status_code == 200
        assert response.json()["text"] == comment["text"]
        assert response.json()["created_by"] is not None
        assert response.json()["updated_by"] is not None
        assert response.json()["created_at"] is not None
        assert response.json()["updated_at"] is not None

        comment["title"] = "Updated comment text"

        response = await ac.patch(f"/comments/{comment_id}", json=comment)
        assert response.status_code == 200

        response = await ac.get(f"/comments/{comment_id}")
        assert response.status_code == 200
        assert response.json()["text"] == comment["text"]
        assert response.json()["created_at"] != response.json()["updated_at"]

        response = await ac.delete(f"/comments/{comment_id}")
        assert response.status_code == 204

        response = await ac.get(f"/comments/{comment_id}")
        assert response.status_code == 404
