from datetime import date

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column, MappedAsDataclass, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    pass


game_genre = Table("game_genre", Base.metadata,
                   Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True),
                   Column("genre_id", ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True))


backlog_game = Table("backlog_game", Base.metadata, 
                     Column("backlog_id", ForeignKey("backlogs.id", ondelete="CASCADE"), primary_key=True), 
                     Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True))


completegame_game = Table("completegame_game", Base.metadata, 
                          Column("complete_game_id", ForeignKey("completegames.id", ondelete="CASCADE"), primary_key=True),
                          Column("game_id", ForeignKey("games.id", ondelete="CASCADE"), primary_key=True))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    backlog: Mapped["Backlog"] = relationship("Backlog", backref="users", cascade="all, delete", passive_deletes=True)
    complete_game: Mapped["CompleteGame"] = relationship("CompleteGame", backref="users", cascade="all, delete", passive_deletes=True)
    games: Mapped[list["Game"] | None] = relationship()
    genres: Mapped[list["Genre"] | None] = relationship()


class Backlog(Base):
    __tablename__ = "backlogs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    games: Mapped[list["Game"]] = relationship(secondary=backlog_game)


class CompleteGame(Base):
    __tablename__ = "completegames"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    games: Mapped[list["Game"]] = relationship(secondary=completegame_game)


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    developer: Mapped[str] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(nullable=False)
    date_release: Mapped[date] = mapped_column(nullable=False)
    image: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    genres: Mapped[list["Genre"]] = relationship(secondary=game_genre)


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True, init=False)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
