from sqlalchemy import Integer, Column, ForeignKey, String, Date, Table
from sqlalchemy.orm import relationship

from api.database import Base


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

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String)
    backlog = relationship("Backlog", uselist=False, backref="users")
    complete_game = relationship("CompleteGame", uselist=False, backref="users")
    games = relationship("Game", back_populates="user")
    genres = relationship("Genre", back_populates="user")


class Backlog(Base):
    __tablename__ = "backlogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    games = relationship("Game", secondary=backlog_game, back_populates="backlogs")


class CompleteGame(Base):
    __tablename__ = "completegames"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    games = relationship("Game", secondary=completegame_game, back_populates="games")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True, index=True)
    developer = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    date_release = Column(Date, nullable=False)
    image = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    genres = relationship("Genre", secondary=game_genre, back_populates="games")
    backlogs = relationship("Backlog", secondary=backlog_game, back_populates="games")
    complete_games = relationship("CompleteGame", secondary=completegame_game, back_populates="games")

    user = relationship("User", back_populates="recipes")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    games = relationship("Game", secondary=game_genre, back_populates="genres")

    user = relationship("User", back_populates="genres")
