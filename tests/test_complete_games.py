import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_new_complete_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"id": 1, "user_id": 1, "games": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_new_complete_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_new_complete_game_400(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "User already has a completegame"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_all_complete_games(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = [{"id": 1, "user_id": 1, "games": []}]
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.get("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_all_complete_games_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_complete_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"id": 1, "user_id": 1, "games": []}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.get("/complete_games/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_get_complete_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/complete_games/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_complete_game_404(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "CompleteGame not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.get("/complete_games/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_add_game_to_complete_game(async_client):
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
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_add_game_to_complete_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_add_game_to_complete_game_404_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_add_game_to_complete_game_400_complete_game(async_client):
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
    test_answer = {"detail": "User has no comlpetegame"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_double_add_game_to_complete_game(async_client):
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
    test_answer = {"detail": "The game has already been added to the completegame"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_from_complete_game(async_client):
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
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/complete_games/", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    response = await async_client.put("/complete_games/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_from_complete_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.put("/complete_games/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_remove_from_complete_game_400_complete_game(async_client):
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
    test_answer = {"detail": "User has no completegame"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/complete_games/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_from_complete_game_404_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.put("/complete_games/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_game_is_not_in_complete_games(async_client):
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
    test_answer = {"detail": "This game is not in the completegame"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload) )
    response = await async_client.put("/complete_games/remove_game", headers={"Authorization": f"Bearer {token}"}, params={"game_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_complete_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"message": "CompleteGame has been deleted successfully"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    response = await async_client.delete("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_complete_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.delete("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_remove_complete_game_400_complete_game(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_answer = {"detail": "User has no completegame"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.delete("/complete_games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == test_answer