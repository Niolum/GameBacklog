from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import User, CompleteGameOut
from api.crud import create_complete_game, get_complete_game, get_complete_games, delete_complete_game
from api.utils import get_current_user, get_session


complete_game_router = APIRouter(
    prefix="/complete_games",
    tags=["complete_games"],
    responses={404: {"description": "Not Found"}}
)

@complete_game_router.post("/", response_model=CompleteGameOut)
async def new_complete_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    if current_user.complete_game:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a completegame"
        )
    
    complete_game = await create_complete_game(db=db, user_id=current_user.id)
    return complete_game

@complete_game_router.get("/{complete_game_id}", response_model=CompleteGameOut)
async def complete_game_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    complete_game_id: int
):
    complete_game = await get_complete_game(db=db, complete_game_id=complete_game_id)
    if complete_game is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CompleteGame not Found"
        )
    return complete_game

@complete_game_router.get("/", response_model=list[CompleteGameOut])
async def all_complete_games(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100
):
    complete_games = await get_complete_games(db=db, skip=skip, limit=limit)
    if complete_games is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CompleteGames not Found"
        )
    return complete_games

@complete_game_router.delete("/")
async def remove_complete_game(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    await delete_complete_game(db=db, complete_game_id=current_user.complete_game.id)
    data = {"message": "CompleteGame has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)