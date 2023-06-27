import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_new_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"id": 1, "user_id": 1, "games": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_new_backlog_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_new_backlog_400(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "User already has a backlog"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_all_backlogs(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = [{"id": 1, "user_id": 1, "games": []}]
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.get("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_all_backlogs_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"id": 1, "user_id": 1, "games": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.get("/backlogs/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_get_backlog_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/backlogs/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_backlog_404(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Backlog not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.get("/backlogs/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_add_game_to_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_answer = {
        "id": 1, 
        "user_id": 1, 
        "games": [{
            "id": 1,
            "title": "game",
            "developer": "developer",
            "publisher": "publisher",
            "date_release": "2023-06-27",
            "image": "string",
            "user_id": 1,
            "genres": []
        }]
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_add_game_to_backlog_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_add_game_to_backlog_404_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_add_game_to_backlog_400_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_answer = {"detail": "User has no backlog"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_double_add_game_to_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_answer = {"detail": "The game has already been added to the backlog"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_from_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_answer = {
        "id": 1, 
        "user_id": 1, 
        "games": []
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/backlogs/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    response = await async_client.put("/backlogs/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_from_backlog_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.put("/backlogs/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_remove_from_backlog_400_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_answer = {"detail": "User has no backlog"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/backlogs/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_from_backlog_404_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.put("/backlogs/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_game_is_not_in_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_answer = {"detail": "This game is not in the backlog"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/backlogs/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"message": "Backlog has been deleted successfully"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.delete("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_backlog_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.delete("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_remove_backlog_400_backlog(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "User has no backlog"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.delete("/backlogs/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == test_answer