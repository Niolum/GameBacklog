import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_new_genre(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"id": 1, "user_id": 1, "title": "test_genre"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_new_genre_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    token = "qwerty"
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_new_genre_is_exists(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"detail": "There is already a Genre with this title"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_get_genre(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"id": 1, "user_id": 1, "title": "test_genre"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.get("/genres/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_get_genre_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/genres/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_genre_404(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Genre not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.get("/genres/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_get_genres(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = [{"id": 1, "user_id": 1, "title": "test_genre"}]
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.get("/genres/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_get_genres_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/genres/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_update_genre(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_new_title_genre = {"title": "new_title", "user_id": 1}
    test_answer = {"id": 1, "user_id": 1, "title": "new_title"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.put("/genres/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_title_genre))
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_update_genre_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    test_new_title_genre = {"title": "new_title", "user_id": 1}
    token = "qwerty"
    response = await async_client.put("/genres/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_title_genre))
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_update_genre_404(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_new_title_genre = {"title": "new_title", "user_id": 1}
    test_answer = {"detail": "Genre not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.put("/genres/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_title_genre))
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_update_genre_400(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_login_payload_second_user = {"username": "another_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_new_title_genre = {"title": "new_title", "user_id": 1}
    test_answer = {"detail": "Genre does not belong to this user"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload_second_user))
    response = await async_client.post("/users/token", data=test_login_payload_second_user)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))

    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)
    token = response.json()
    token = token["access_token"]
    response = await async_client.put("/genres/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_title_genre))
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_delete_genre(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"message": "Genre has been deleted successfully"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.delete("/genres/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_delete_genre_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.delete("/genres/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_delete_genre_404(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Genre not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.delete("/genres/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == test_answer
