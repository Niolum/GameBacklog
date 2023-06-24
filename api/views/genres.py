from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import GenreCreate, User, Genre
from api.crud import create_genre, get_genre, get_genres, delete_genre, get_genre_by_title, is_users_genre
from api.utils import get_current_user, get_session


genre_router = APIRouter(
    prefix="/genres",
    tags=["genres"],
    responses={404: {"description": "Not Found"}}
)

@genre_router.post("/", response_model=Genre)
async def new_genre(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    genre: GenreCreate
):
    db_genre = await get_genre_by_title(db=db, title=genre.title)
    if db_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already a Genre with this title"
        )
    if current_user.id != genre.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id must be equal to the id of the current user"
        )
    new_genre = await create_genre(db=db, genre=genre)
    return new_genre

@genre_router.get("/{genre_id}", response_model=Genre)
async def genre_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    genre_id: int
):
    genre = await get_genre(db=db, genre_id=genre_id)
    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not Found"
        )
    return genre

@genre_router.get("/", response_model=list[Genre])
async def all_genres(
    currnet_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100
):
    genres = await get_genres(db=db, skip=skip, limit=limit)
    if genres is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genres not Found"
        )
    return genres

@genre_router.delete("/{genre_id}")
async def remove_genre(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    genre_id: int
):
    genre = await is_users_genre(db=db, genre_id=genre_id, user_id=current_user.id)
    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not Found"
        )
    
    await delete_genre(db=db, genre_id=genre_id)
    data = {"message": "Genre has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)