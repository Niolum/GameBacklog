from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import GameCreate, User, Game, GameUpdate
from api.crud import (
    create_game, 
    get_game_by_title, 
    get_game, 
    get_games, 
    delete_game, 
    is_users_game,
    update_game,
    update_genres_for_game,
    clear_genres_for_game,
    get_genre,
    is_genre_in_game
)
from api.utils import get_current_user, get_session


game_router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Npt Found"}}
)

@game_router.post("/", response_model=Game)
async def new_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    game: GameCreate
):
    db_game = await get_game_by_title(db=db, title=game.title)
    if db_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already a Game with this title"
        )
    if current_user.id != game.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id must be equal to the id of the current user"
        )
    new_game = await create_game(db=db, game=game)
    return new_game

@game_router.get("/{game_id}", response_model=Game)
async def game_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    game_id: int
):
    game = await get_game(db=db, game_id=game_id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not Found"
        )
    return game

@game_router.get("/", response_model=list[Game])
async def all_games(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100
):
    games = await get_games(db=db, skip=skip, limit=limit)
    if games is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Games not Found"
        )
    return games

@game_router.delete("/{game_id}")
async def remove_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    game_id: int
):
    game = await is_users_game(db=db, game_id=game_id, user_id=current_user.id)
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not Found"
        )
    
    await delete_game(db=db, game_id=game_id)
    data = {"message": "Game has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)

@game_router.put("/{game_id}", response_model=Game)
async def change_data_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    game_id: int,
    new_game: GameUpdate
):
    db_game = await get_game(db=db, game_id=game_id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not Found"
        )
    db_game = await is_users_game(db=db, game_id=game_id, user_id=current_user.id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The game does not belong to this user"
        )
    is_game_title = await get_game_by_title(db=db, title=new_game.title)
    if is_game_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already a Game with this title"
        )
    new_game = await update_game(db=db, game=db_game, new_game=new_game)
    return new_game

@game_router.patch("/{game_id}", response_model=Game)
async def add_genre_to_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    game_id: int,
    genre_id: int
):
    db_game = await is_genre_in_game(db=db, game_id=game_id, genre_id=genre_id)
    if db_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The genre has already been added to the game"
        )
    db_game = await get_game(db=db, game_id=game_id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not Found"
        )
    db_game = await is_users_game(db=db, game_id=game_id, user_id=current_user.id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The game does not belong to this user"
        )
    db_genre = await get_genre(db=db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not Found"
        )
    new_game = await update_genres_for_game(db=db, game=db_game, genre=db_genre)
    return new_game

@game_router.patch("/{game_id}/{genre_id}", response_model=Game)
async def remove_genre_from_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    game_id: int,
    genre_id: int
):
    db_game = await get_game(db=db, game_id=game_id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not Found"
        )
    db_game = await is_users_game(db=db, game_id=game_id, user_id=current_user.id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The game does not belong to this user"
        )
    db_game = await is_genre_in_game(db=db, game_id=game_id, genre_id=genre_id)
    if db_game is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This genre is not in the game"
        )
    db_genre = await get_genre(db=db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not Found"
        )
    new_game = await clear_genres_for_game(db=db, game=db_game, genre=db_genre)
    return new_game