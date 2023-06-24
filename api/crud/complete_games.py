from sqlalchemy import select, delete, insert
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import CompleteGame


async def create_complete_game(db: AsyncSession, user_id: int):
    complete_game = CompleteGame(
        user_id=user_id,
        games=[]
    )
    db.add(complete_game)
    await db.commit()
    return complete_game

async def get_complete_game(db: AsyncSession, complete_game_id: int):
    result = await db.execute(
        select(CompleteGame)
        .where(CompleteGame.id == complete_game_id)
    )
    return result.scalars().first()

async def get_complete_games(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(CompleteGame)
        .order_by(CompleteGame.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(CompleteGame.games))
    )
    return result.scalars().fetchall()

async def delete_complete_game(db: AsyncSession, complete_game_id: int):
    await db.execute(
        delete(CompleteGame)
        .where(CompleteGame.id==complete_game_id)
    )
    await db.commit()
    return True