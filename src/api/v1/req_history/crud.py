from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete, Result

from src.api.v1.schemas.req_history import OutReqHistory, InReqHistory
from src.api.v1.schemas.utils import to_pydantic
from src.core.database.models import RequestHistory, User


async def create_history(
        history: InReqHistory,
        uuid: str,
        session: AsyncSession
) -> OutReqHistory | None:
    insert_stmt = insert(RequestHistory).values(
        uuid_user=uuid,
        name=history.name,
        url_card=history.url_card,
        url_img=history.url_img
    )
    await session.execute(insert_stmt)
    await session.commit()
    select_stmt = select(RequestHistory).where(RequestHistory.uuid_user == uuid).order_by(RequestHistory.id.desc()).limit(1)
    result: Result = await session.execute(select_stmt)
    req_history = result.scalar()
    if req_history:
        req_history_model = to_pydantic(req_history, OutReqHistory)
        return req_history_model
    else:
        raise HTTPException(500)



async def get_history_by_id(
        id: int,
        uuid: str,
        session: AsyncSession,
) -> OutReqHistory | None:
    select_stmt = select(RequestHistory).where(RequestHistory.uuid_user == uuid, RequestHistory.id == id).order_by(
        RequestHistory.id.desc())
    result: Result = await session.execute(select_stmt)
    req_history = result.scalar()
    if req_history:
        return to_pydantic(req_history, OutReqHistory)
    else:
        return None


async def get_history_all(
        uuid: str,
        session: AsyncSession,
) -> list[OutReqHistory] | None:
    select_stmt = select(RequestHistory).where(RequestHistory.uuid_user == uuid).order_by(RequestHistory.id.desc())
    result: Result = await session.execute(select_stmt)
    req_historys = result.scalars().all()
    if req_historys:
        return [to_pydantic(req_history, OutReqHistory) for req_history in req_historys]
    else:
        return None


async def delete_history(
        id: int,
        uuid: str,
        session: AsyncSession,
):
    delete_stmt = delete(RequestHistory).where(RequestHistory.uuid_user == uuid, RequestHistory.id == id)
    await session.execute(delete_stmt)
    await session.commit()
    history = await get_history_by_id(id, uuid, session)
    if history:
        return False
    else:
        return True
