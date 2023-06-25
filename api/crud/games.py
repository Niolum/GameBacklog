from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Genre, Game
from api.schemas import GameCreate, GameUpdate


async def create_game(db: AsyncSession, game: GameCreate):
    new_game = Game(
        title=game.title,
        developer=game.developer,
        publisher=game.publisher,
        date_release=game.date_release,
        image=game.image,
        user_id=game.user_id,
        genres=[]
    )
    db.add(new_game)
    await db.commit()
    for genre in game.genres:
        result = await db.execute(
            select(Genre)
            .where(Genre.id==genre.id)
        )
        new_game.genres.append(result.scalars().first())
    await db.commit()
    return new_game

async def get_game_by_title(db: AsyncSession, title: str):
    result = await db.execute(
        select(Game.id, Game.title)
        .where(Game.title==title)
    )
    return result.mappings().first()

async def get_game(db: AsyncSession, game_id: int):
    result = await db.execute(
        select(Game)
        .where(Game.id==game_id)
        .options(selectinload(Game.genres))
    )
    return result.scalars().first()

async def get_games(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Game)
        .order_by(Game.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Game.genres))
    )
    return result.scalars().fetchall()

async def delete_game(db: AsyncSession, game_id: int):
    await db.execute(
        delete(Game)
        .where(Game.id==game_id)
    )
    await db.commit()
    return True

async def is_users_game(db: AsyncSession, game_id: int, user_id: int):
    result = await db.execute(
        select(Game)
        .where(Game.id==game_id)
        .where(Game.user_id==user_id)
    )
    return result.scalars().first()

async def update_game(db: AsyncSession, game: Game, new_game: GameUpdate):
    game.title = new_game.title
    game.publisher = new_game.publisher
    game.developer = new_game.developer
    game.date_release = new_game.date_release
    await db.commit()
    return game

async def update_genres_for_game(db: AsyncSession, game: Game, genre: Genre):
    game.genres.append(genre)
    await db.commit()
    return game

async def clear_genres_for_game(db: AsyncSession, game: Game, genre: Genre):
    game.genres.remove(genre)
    await db.commit()
    return game

async def is_genre_in_game(db: AsyncSession, game_id: int, genre_id: int):
    result = await db.execute(
        select(Game)
        .join(Genre, Game.genres)
        .where(Game.id==game_id)
        .where(Genre.id==genre_id)
    )
    return result.scalars().first()