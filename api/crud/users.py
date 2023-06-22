from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from api.models import User, Backlog, Game, CompleteGame, Genre
from api.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user_by_name(db: AsyncSession, username: str):
    result = await db.execute(select(User.id, User.username, User.hashed_password).where(User.username==username))
    user = result.first()
    return user

async def get_user_info(db: AsyncSession, username: str):
    result = await db.execute(
        select(User.id, User.username, User.backlog, User.complete_game, User.games, User.genres).
        join(Backlog, isouter=True).
        join(CompleteGame, isouter=True).
        join(Game, isouter=True).
        join(Genre, isouter=True).
        where(User.username==username)
    )
    user = result.first()
    return user

async def create_user(db: AsyncSession, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession):
    result = await db.execute(
        select(User.id, User.username, User.backlog, User.complete_game, User.games, User.genres).
        join(Backlog, isouter=True).
        join(CompleteGame, isouter=True).
        join(Game, isouter=True).
        join(Genre, isouter=True)
    )
    result = result.fetchall()
    users = [user._asdict() for user in result]
    return users

async def delete_user(db: AsyncSession, username: str):
    await db.execute(
        delete(User).
        where(User.username==username)
    )
    await db.commit()
    return True
