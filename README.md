## Features

- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.11)
  - JWT authentication using [OAuth2](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- **[PostgreSQL](https://www.postgresql.org/)** for the database
- **[SqlAlchemy](https://www.sqlalchemy.org/)** for ORM
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)** for database
  migrations
- **[Pytest](https://docs.pytest.org/en/latest/)** for backend tests
- **[Docker Compose](https://docs.docker.com/compose/)**

## Background

Very often we simply rely on our memory, without writing down the information we are interested in anywhere. 
This also applies to video games. I like video games and I have a list of games I would like to play. This list is constantly updated.
It's getting hard enough to remember everything.

I wrote this API that allows you to record games in the backlog (games that I want to play) or in the completegame (games that I have already completed)
The API allows you to register, log in, create genres for video games, create video games, add or remove game from the backlog or completegame.

## Quickstart

First, clone project

``` 
git clone https://github.com/Niolum/GameBacklog.git 
```

Then, create ``.env`` file. set environment variables and create database. 

Example ``.env``:

```
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/db_name"
SECRET_KEY = "some secret key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
TEST_DATABASE_URL = "postgresql+asyncpg://username:password@localhost/test_db_name"
```

Further, set up the virtual environment and the main dependencies from the ``requirements.txt``

```
python -m venv venv
source venv/bin/activate 
# or for windows
venv/Scripts/activate 
pip install -r requirements.txt
```

To run the web application in debug use:

```
alembic upgrade head
uvicorn main:app --reload
```


For start in docker-compose change ``DATABASE_URL`` in ``.env`` and start conteiners:

```
DATABASE_URL = "postgresql+asyncpg://username:some_password@backlogdb/some_name_db"
POSTGRES_USER=username
POSTGRES_PASSWORD=some_password
POSTGRES_DB=some_name_db
```

```
docker-compose up -d
```

## Run test

Tests for this project are defined in the tests/ folder.

To run all the tests of a project, simply run the pytest command:

```
pytest
```