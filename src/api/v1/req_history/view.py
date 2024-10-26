from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.req_history import crud
from src.api.v1.auth_utils import auth_utils
from src.api.v1.schemas.ar_token import TokenInfo
from src.api.v1.schemas.utils import to_pydantic
from src.api.v1.schemas.req_history import OutReqHistory, InReqHistory
from src.core import settings
from src.core.database.db_helper import db_helper

router = APIRouter(tags=["History", ])

@router.get("/history/{id}", tags=[settings.ACCESS_TYPE.access])
async def get_history_by_id(
        id: int,
        uuid: str = Depends(auth_utils.uuid_dep),
        session: AsyncSession = Depends(db_helper.get_async_session)
) -> OutReqHistory | None:
    return await crud.get_history_by_id(id, uuid, session)

@router.get("/history", tags=[settings.ACCESS_TYPE.access])
async def get_history_all(
        uuid: str = Depends(auth_utils.uuid_dep),
        session: AsyncSession = Depends(db_helper.get_async_session),
) -> list[OutReqHistory] | None:
    return await crud.get_history_all(uuid, session)

@router.delete("/history/{id}", tags=[settings.ACCESS_TYPE.access])
async def delete_history(
        id: int,
        uuid: str = Depends(auth_utils.uuid_dep),
        session: AsyncSession = Depends(db_helper.get_async_session),
):
    is_dalete = await crud.delete_history(id, uuid, session)
    if is_dalete:
        raise HTTPException(200, "Success")
    else:
        raise HTTPException(500, "Internal Server Error")

@router.post("/history", tags=[settings.ACCESS_TYPE.access])
async def create_history(
        history: InReqHistory,
        uuid: str = Depends(auth_utils.uuid_dep),
        session: AsyncSession = Depends(db_helper.get_async_session),
):
    return await crud.create_history(history, uuid, session)
