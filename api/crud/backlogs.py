from sqlalchemy import select, delete, insert
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Backlog, User, Game, backlog_game


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
        .options(selectinload(Backlog.games))
    )
    return result.scalars().first()

async def get_backlogs(db: AsyncSession, skip: int = 0, limit: int = 0):
    result = await db.execute(
        select(Backlog)
        .order_by(Backlog.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Backlog.games))
    )
    return result.scalars().fetchall()

async def delete_backlog(db: AsyncSession, backlog_id: int):
    await db.execute(
        delete(Backlog)
        .where(Backlog.id==backlog_id)
    )
    await db.commit()
    return True