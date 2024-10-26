from sqlalchemy import Result, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.core.database import User
from src.api.v1.schemas.user import  RegUserSch, OutUserSch, ORMUserSch
from src.api.v1.auth_utils import auth_utils
from src.api.v1.schemas.utils import to_pydantic


async def get_user(
        session: AsyncSession,
        email: str | None = None,
        uuid: str | None = None,
) -> ORMUserSch | None:
    stmt = select(User)
    if email:
        stmt = stmt.where(User.email == email)
    elif uuid:
        stmt = stmt.where(User.uuid == uuid)
    else:
        raise Exception(f"No email or uuid values were passed")
    result: Result = await session.execute(stmt)
    user: User = result.scalar()
    if user:
        return to_pydantic(user, ORMUserSch)
    else:
        return None


async def create_user(
        user: RegUserSch,
        session: AsyncSession
) -> OutUserSch:
    exists_user = await get_user(session=session, email=user.email)
    if exists_user:
        raise HTTPException(400, detail="User with this email exists")
    insert_stmt = insert(User).values(email=user.email, pwd_hash=auth_utils.hash_pwd(user.pwd))
    insert_result = await session.execute(insert_stmt)
    select_stmt = select(User).where(User.email == user.email)
    select_result = await session.execute(select_stmt)
    user = select_result.scalar()
    await session.commit()
    return to_pydantic(user, OutUserSch)
