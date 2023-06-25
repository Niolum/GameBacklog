from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import GameCreate, User, Game
from api.crud import create_game, get_game_by_title, get_game, get_games, delete_game, is_users_game
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