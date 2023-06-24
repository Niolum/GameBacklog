from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import User, BacklogOut
from api.crud import create_backlog, get_backlog, get_backlogs, delete_backlog
from api.utils import get_current_user, get_session


backlog_router = APIRouter(
    prefix="/backlogs",
    tags=["backlogs"],
    responses={404: {"description": "Not found"}},
)

@backlog_router.post("/", response_model=BacklogOut)
async def new_backlog(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    if current_user.backlog:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a backlog"
        )
    
    id = current_user.id
    new_backlog = await create_backlog(db=db, user_id=id)
    return new_backlog

@backlog_router.get("/{backlog_id}", response_model=BacklogOut)
async def backlog_by_id(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    backlog_id: int
):
    backlog = await get_backlog(db=db, backlog_id=backlog_id)
    if backlog is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backlog not Found"
        )
    return backlog

@backlog_router.get("/", response_model=list[BacklogOut])
async def all_backlogs(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    skip: int = 0,
    limit: int = 100
):
    backlogs = await get_backlogs(db=db, skip=skip, limit=limit)
    if backlogs is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backlogs not Found"
        )
    return backlogs

@backlog_router.delete("/")
async def remove_backlog(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_session)]
):
    await delete_backlog(db=db, backlog_id=current_user.backlog.id)
    data = {"message": "Backlog has been deleted successfully"}
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)
