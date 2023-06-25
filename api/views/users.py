import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv

from api.schemas import Token, User, UserCreate, UserUpdate
from api.database import get_session
from api.utils import authenticate_user, create_access_token, get_current_user
from api.crud import get_user_by_name, create_user, get_users, delete_user, update_user


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@user_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_session)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/register", response_model=User)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_name(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already exists"
        )
    new_user = await create_user(db=db, user=user)
    return new_user

@user_router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):  
    user = await get_user_by_name(db=db, username=current_user.username)
    return user

@user_router.get("/", response_model=list[User])
async def read_users(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100
):
    return await get_users(db=db, skip=skip, limit=limit)

@user_router.get("/{username}", response_model=User)
async def read_user(
    username: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    user = await get_user_by_name(db=db, username=username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not Found"
        )
    return user

@user_router.delete("/me")
async def user_delete(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    await delete_user(db=db, username=current_user.username)
    data ={"message": "User has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)

@user_router.put("/me", response_model=User)
async def user_change_username(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    user: UserUpdate
):
    user_db = await get_user_by_name(db=db, username=user.username)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already exists"
        )
    user = await update_user(db=db, user=current_user, new_user=user)
    return user