from datetime import date

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class GenreBase(BaseModel):
    user_id: int
    title: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    title: str
    developer: str
    publisher: str
    date_release: date
    image: str | None = None
    user_id: int
    genres: list[Genre]


class GameCreate(GameBase):
    pass


class GameUpdate(BaseModel):
    title: str
    developer: str
    publisher: str
    date_release: date


class Game(GameBase):
    id: int

    class Config:
        orm_mode = True



class Backlog(BaseModel):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True


class BacklogCreate(Backlog):
    pass


class BacklogOut(Backlog):
    games: list[Game]


class CompleteGame(BaseModel):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class CompleteGameOut(CompleteGame):
    games: list[Game]


class UserBase(BaseModel):
    username: str


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int | None
    backlog: Backlog | None
    complete_game: CompleteGame | None
    games: list[Game] = []
    genres: list[Genre] = []

    class Config:
        orm_mode = True
