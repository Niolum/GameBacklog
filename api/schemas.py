from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class GenreBase(BaseModel):
    title: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class Genre(GenreBase):
    id: int


class GameBase(BaseModel):
    title: str
    developer: str
    publisher: str
    date_release: str
    image: str | None = None


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class Game(GameBase):
    id: int
    genres: list[Genre]


class Backlog(BaseModel):
    id: int
    user_id: int


class BacklogOut(Backlog):
    games: list[Game]


class CompleteGame(BaseModel):
    id: int
    user_id: int


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

    class Config:
        orm_mode: True

class UserOut(UserBase):
    id: int
    blacklog: BacklogOut | None
    complete_game: CompleteGameOut | None
    games: list[Game, None] | None
    genres: list[Genre, None] | None
