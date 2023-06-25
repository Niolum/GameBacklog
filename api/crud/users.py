from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from passlib.context import CryptContext

from api.models import User, Backlog, Game, CompleteGame
from api.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_name(db: AsyncSession, username: str):
    result = await db.execute(
        select(User)
        .where(User.username==username)
        .options(selectinload(User.backlog).selectinload(Backlog.games).selectinload(Game.genres))
        .options(selectinload(User.complete_game).selectinload(CompleteGame.games).selectinload(Game.genres))
        .options(selectinload(User.games).selectinload(Game.genres))
        .options(selectinload(User.genres))
    )
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        backlog=None,
        complete_game=None,
        games=[],
        genres=[]
    )
    db.add(new_user)
    await db.commit()
    return new_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(User)
        .order_by(User.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(User.backlog).selectinload(Backlog.games).selectinload(Game.genres))
        .options(selectinload(User.complete_game).selectinload(CompleteGame.games).selectinload(Game.genres))
        .options(selectinload(User.games).selectinload(Game.genres))
        .options(selectinload(User.genres))
    )
    return result.scalars().fetchall()

async def delete_user(db: AsyncSession, username: str):
    await db.execute(
        delete(User).
        where(User.username==username)
    )
    await db.commit()
    return True

async def update_user(db: AsyncSession, user: User, new_user: UserUpdate):
    user.username = new_user.username
    await db.commit()
    return user
