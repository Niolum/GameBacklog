import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_create_user(async_client):
    test_request_payload = {"username": "test_user", "password": "qwerty"}
    test_response_payload = {"id": 1, "username": "test_user", "backlog": None, "complete_game": None, "games": [], "genres": []}
    response = await async_client.post("/users/register", content=json.dumps(test_request_payload))
    assert response.status_code == 200
    assert response.json() == test_response_payload


async def test_create_user_incorrect(async_client):
    test_request_payload = {"username": "test_user"}
    response = await async_client.post("/users/register", content=json.dumps(test_request_payload))
    assert response.status_code == 422


async def test_login(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)
    assert response.status_code == 200


async def test_login_incorrect(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    incorrect_data = {"username": "test_user", "password": "qwe"}
    test_answer = {'detail': 'Incorrect username or password'} 
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=incorrect_data)
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_users_me(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_response_payload = {"id": 1, "username": "test_user", "backlog": None, "complete_game": None, "games": [], "genres": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_response_payload


async def test_users_me_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_read_users(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_response_payload = [{"id": 1, "username": "test_user", "backlog": None, "complete_game": None, "games": [], "genres": []}]
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_response_payload


async def test_read_users_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_read_user(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_response_payload = {"id": 1, "username": "test_user", "backlog": None, "complete_game": None, "games": [], "genres": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.get("/users/test_user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_response_payload


async def test_read_user_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/users/test_user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_read_user_not_found(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.get("/users/another_user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


async def test_update_user(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_response_payload = {"id": 1, "username": "new_name_user", "backlog": None, "complete_game": None, "games": [], "genres": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    new_username = {"username": "new_name_user"}
    response = await async_client.put("/users/me", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(new_username))
    assert response.status_code == 200
    assert response.json() == test_response_payload


async def test_update_user_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    new_username = {"username": "new_name_user"}
    response = await async_client.put("/users/me", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(new_username))
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_update_user_is_exists(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    second_user = {"username": "another_user", "password": "qwerty"}
    test_answer = {"detail": "Username is already exists"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/register", content=json.dumps(second_user))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    new_username = {"username": "another_user"}
    response = await async_client.put("/users/me", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(new_username))
    assert response.status_code == 400
    assert response.json() == test_answer

async def test_delete_user(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"message": "User has been deleted successfully"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer

async def test_delete_user_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.delete("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer
