import json
import pytest


pytestmark = pytest.mark.asyncio


async def test_new_game(async_client):
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
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_new_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    token = "qwerty"
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_new_game_is_title_exists(async_client):
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
    test_answer = {"detail": "There is already a Game with this title"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_new_game_wrong_user_id(async_client):
    test_login_payload = {"username": "test_user", "password": "qwerty"}
    test_game_payload = {
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 2,
        "genres": []
    }
    test_answer = {"detail": "user_id must be equal to the id of the current user"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_get_game(async_client):
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
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.get("/games/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_get_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/games/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_get_game_404(async_client):
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
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.get("/games/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_get_games(async_client):
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
    test_answer = [{
        "id": 1,
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }]
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.get("/games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_get_games_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.get("/games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_add_genre_to_game(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {
        "id": 1,
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": [{
            "id": 1,
            "user_id": 1,
            "title": "test_genre"
        }]
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_add_genre_to_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_add_genre_to_game_404_game(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/2", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_add_genre_to_game_404_genre(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"detail": "Genre not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 2})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_add_genre_to_game_wrong_user(async_client):
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
    test_login_payload_second_user = {"username": "another_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 2, "title": "test_genre"}
    test_answer = {"detail": "The game does not belong to this user"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload_second_user))
    response = await async_client.post("/users/token", data=test_login_payload_second_user)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))

    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_double_add_genre_to_game(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"detail": "The genre has already been added to the game"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_remove_genre_from_game(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {
        "id": 1,
        "title": "game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    response = await async_client.patch("/games/1/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_remove_genre_from_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.patch("/games/1/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_remove_genre_from_game_404_game(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1", headers={"Authorization": f"Bearer {token}"}, params={"genre_id": 1})
    response = await async_client.patch("/games/2/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_remove_genre_from_game_wrong_user(async_client):
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
    test_login_payload_second_user = {"username": "another_user", "password": "qwerty"}
    test_genre_payload = {"user_id": 2, "title": "test_genre"}
    test_answer = {"detail": "The game does not belong to this user"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload_second_user))
    response = await async_client.post("/users/token", data=test_login_payload_second_user)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))

    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_genre_not_in_game(async_client):
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
    test_genre_payload = {"user_id": 1, "title": "test_genre"}
    test_answer = {"detail": "This genre is not in the game"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/genres/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_genre_payload))
    response = await async_client.patch("/games/1/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_update_game(async_client):
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
    test_new_game_data_payload = {
        "title": "new_game",
        "developer": "new_developer",
        "publisher": "new_publisher",
        "date_release": "2023-06-27"
    }
    test_answer = {
        "id": 1,
        "title": "new_game",
        "developer": "new_developer",
        "publisher": "new_publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.put("/games/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_game_data_payload))
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_update_game_incorrect(async_client):
    test_new_game_data_payload = {
        "title": "new_game",
        "developer": "new_developer",
        "publisher": "new_publisher",
        "date_release": "2023-06-27"
    }
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.put("/games/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_game_data_payload))
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_update_game_404_game(async_client):
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
    test_new_game_data_payload = {
        "title": "new_game",
        "developer": "new_developer",
        "publisher": "new_publisher",
        "date_release": "2023-06-27"
    }
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.put("/games/2", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_game_data_payload))
    assert response.status_code == 404
    assert response.json() == test_answer


async def test_update_game_wrong_user(async_client):
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
    test_login_payload_second_user = {"username": "another_user", "password": "qwerty"}
    test_new_game_data_payload = {
        "title": "new_game",
        "developer": "new_developer",
        "publisher": "new_publisher",
        "date_release": "2023-06-27"
    }
    test_answer = {"detail": "The game does not belong to this user"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload_second_user))
    response = await async_client.post("/users/token", data=test_login_payload_second_user)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))

    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.put("/games/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_game_data_payload))
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_update_game_title_is_exists(async_client):
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
    test_second_game_payload = {
        "title": "new_game",
        "developer": "developer",
        "publisher": "publisher",
        "date_release": "2023-06-27",
        "image": "string",
        "user_id": 1,
        "genres": []
    }
    test_new_game_data_payload = {
        "title": "new_game",
        "developer": "new_developer",
        "publisher": "new_publisher",
        "date_release": "2023-06-27"
    }
    test_answer = {"detail": "There is already a Game with this title"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_second_game_payload))
    response = await async_client.put("/games/1", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_new_game_data_payload))
    assert response.status_code == 400
    assert response.json() == test_answer


async def test_delete_game(async_client):
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
    test_answer = {"message": "Game has been deleted successfully"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.delete("/games/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == test_answer


async def test_delete_game_incorrect(async_client):
    test_answer = {"detail": "Could not validate credentials"}
    token = "qwerty"
    response = await async_client.delete("/games/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json() == test_answer


async def test_delete_game_404(async_client):
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
    test_answer = {"detail": "Game not Found"}
    response = await async_client.post("/users/register", content=json.dumps(test_login_payload))
    response = await async_client.post("/users/token", data=test_login_payload)

    token = response.json()
    token = token["access_token"]
    response = await async_client.post("/games/", headers={"Authorization": f"Bearer {token}"}, content=json.dumps(test_game_payload))
    response = await async_client.delete("/games/2", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    assert response.json() == test_answer