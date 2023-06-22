from datetime import date

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, MappedAsDataclass, DeclarativeBase


class Base(MappedAsDataclass, DeclarativeBase):
    pass


game_genre = Table("game_genre", Base.metadata,
                   Column("game_id", ForeignKey("games.id"), primary_key=True),
                   Column("genre_id", ForeignKey("genres.id"), primary_key=True))


backlog_game = Table("backlog_game", Base.metadata, 
                     Column("backlog_id", ForeignKey("backlogs.id"), primary_key=True), 
                     Column("game_id", ForeignKey("games.id"), primary_key=True))


completegame_game = Table("completegame_game", Base.metadata, 
                          Column("complete_game_id", ForeignKey("completegames.id"), primary_key=True),
                          Column("game_id", ForeignKey("games.id"), primary_key=True))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    backlog: Mapped["Backlog"] = relationship(back_populates="user", lazy="selectin")
    complete_game: Mapped["CompleteGame"] = relationship(back_populates="user", lazy="selectin")
    games: Mapped[list["Game"] | None] = relationship(lazy="selectin")
    genres: Mapped[list["Genre"] | None] = relationship(lazy="selectin")

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password


class Backlog(Base):
    __tablename__ = "backlogs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="backlog")
    games: Mapped[list["Game"]] = relationship(secondary=backlog_game)


class CompleteGame(Base):
    __tablename__ = "completegames"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="complete_game")
    games: Mapped[list["Game"]] = relationship(secondary=completegame_game)


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    developer: Mapped[str] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(nullable=False)
    date_release: Mapped[date] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="games")
    genres: Mapped[list["Genre"]] = relationship(secondary=game_genre, back_populates="games")
    backlogs: Mapped[list["Backlog"] | None] = relationship(secondary=backlog_game, back_populates="games")
    complete_games: Mapped[list["CompleteGame"] | None] = relationship(secondary=completegame_game, back_populates="games")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="genres")
    games: Mapped[list["Game"] | None] = relationship(secondary=game_genre, back_populates="genres")
