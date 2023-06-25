from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Backlog, Game, backlog_game


async def create_backlog(db: AsyncSession, user_id: int):
    new_backlog = Backlog(
        user_id=user_id,
        games=[]
    )
    db.add(new_backlog)
    await db.commit()
    return new_backlog

async def get_backlog(db: AsyncSession, backlog_id: int):
    result = await db.execute(
        select(Backlog)
        .where(Backlog.id == backlog_id)
        .options(selectinload(Backlog.games).selectinload(Game.genres))
    )
    return result.scalars().first()

async def get_backlogs(db: AsyncSession, skip: int = 0, limit: int = 0):
    result = await db.execute(
        select(Backlog)
        .order_by(Backlog.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Backlog.games).selectinload(Game.genres))
    )
    return result.scalars().fetchall()

async def delete_backlog(db: AsyncSession, backlog_id: int):
    await db.execute(
        delete(Backlog)
        .where(Backlog.id==backlog_id)
    )
    await db.commit()
    return True

async def update_backlog(db: AsyncSession, backlog: Backlog, game: Game):
    backlog.games.append(game)
    await db.commit()
    return backlog

async def clear_backlog(db: AsyncSession, backlog: Backlog, game: Game):
    backlog.games.remove(game)
    await db.commit()
    return backlog

async def is_game_in_backlog(db: AsyncSession, game_id: int, backlog_id: int):
    result = await db.execute(
        select(Backlog)
        .join(Game, Backlog.games)
        .where(Game.id==game_id)
        .where(Backlog.id==backlog_id)
    )
    return result.scalars().first()