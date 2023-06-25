from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Genre
from api.schemas import GenreCreate, GenreUpdate


async def create_genre(db: AsyncSession, genre: GenreCreate):
    new_genre = Genre(
        title=genre.title,
        user_id=genre.user_id
    )
    db.add(new_genre)
    await db.commit()
    return new_genre

async def get_genre(db: AsyncSession, genre_id: int):
    result = await db.execute(
        select(Genre)
        .where(Genre.id==genre_id)
    )
    return result.scalars().first()

async def get_genre_by_title(db: AsyncSession, title: str):
    result = await db.execute(
        select(Genre)
        .where(Genre.title==title)
    )
    return result.scalars().first()

async def get_genres(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Genre)
        .order_by(Genre.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().fetchall()

async def delete_genre(db: AsyncSession, genre_id: int):
    await db.execute(
        delete(Genre)
        .where(Genre.id==genre_id)
    )
    await db.commit()
    return True

async def is_users_genre(db: AsyncSession, genre_id: int, user_id: int):
    result = await db.execute(
        select(Genre)
        .where(Genre.id==genre_id)
        .where(Genre.user_id==user_id)
    )
    return result.scalars().first()

async def update_genre(db: AsyncSession, genre: Genre, new_genre: GenreUpdate):
    genre.title = new_genre.title
    await db.commit()
    return genre
