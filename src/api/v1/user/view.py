

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.user.crud import create_user, get_user
from src.api.v1.auth_utils import auth_utils
from src.api.v1.schemas.ar_token import TokenInfo
from src.api.v1.schemas.utils import to_pydantic
from src.api.v1.schemas.user import (RegUserSch,
                                     LoginUserSch,
                                     OutUserSch,
                                     ORMUserSch
                                     )
from src.core import settings
from src.core.database.db_helper import db_helper

#
router = APIRouter(prefix="/user", tags=["User", ], dependencies=[Depends(HTTPBearer(auto_error=False))])
"""
{
  "email": "test@test.com",
  "pwd": "qweQWE123!@#"
}
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImFjY2VzcyIsInN1YiI6IjhiZGQ4OTk3LTZkZmItNDAwOS1hMDE2LTMzYjRhZjNiMGUxYiIsInVzZXJuYW1lIjoidGVzdEB0ZXN0LmNvbSIsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSIsImFjdGl2ZSI6dHJ1ZSwiZXhwIjoxNzI5OTYyOTczLCJpYXQiOjE3MjczNzA5NzN9.k7RnU-JR9tDF4_0smVPuJh6WrNiv_8-LIH82ReUqadHMHJYqeGvd1u2IIT5SSymlQEchTh8FUzSU1tGYSN2xL82nqaIaDtrqrhg_PD-mal7lWk_ki2mxYJTgQ3gczB6cG3KFRhrHuxzYo_aNtKgQ3q-zKcRPHLb2by35Pyc4dHNB0uaxNOtM-V0RGeTpIn3DBGuLy0nj4CQz_CMJJmYUIR4sA_AyiLOnapQFDHp2oBGZxKUeZgnRb0ifiweGDynuF_XEd4pPHmA0WM0uBugwsEjq1djhxiE_3netKohkEw5E861KUaC_czo092runzsN0J24qbttr0hfgjmTsk1AsA",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6InJlZnJlc2giLCJzdWIiOiI4YmRkODk5Ny02ZGZiLTQwMDktYTAxNi0zM2I0YWYzYjBlMWIiLCJleHAiOjE3Mjk5NjI5NzQsImlhdCI6MTcyNzM3MDk3NH0.FCUgqKtOjuFJcdBXRPN8kxGH12NZgl_UvDIi9npfLwy3bLckh7gfNA9QEPYOc2FAGDGqVicZpf2BE2-cBTOSAcZueqysQdc4Zaa2JC-RAcC9m5QdbxjJyRlyuDTyO69-WGxjJg502z8u2lHICP8NQAX6CZX74mKkilGFYZF6BNV2tnv3GbbxCfmEYRR1pgzR-WK2_wa-nHVqJk6S9BHu-LqJVhsCdE-gkgEoEcutKP3JXb8MoNSI6ib_nD-tAbIRQeu6lEv8Z0eVl1sXhHPsh5hVmDHQ6jwnuLsiLk_KC-wJYIyEy42V0dKY49M5OAHGJ7Wirpw7-fe674BYX5bF0w",
  "token_type": "Bearer"
}

"""


@router.get("/me", tags=[settings.ACCESS_TYPE.access])
async def get_user_meta(
        uuid: str = Depends(auth_utils.uuid_dep, ),
        session: AsyncSession = Depends(db_helper.get_async_session)
) -> OutUserSch:
    user = await get_user(session, uuid=uuid)
    return to_pydantic(user, OutUserSch)


@router.post("/registration", tags=[settings.ACCESS_TYPE.neutral])
async def registration(
        user: RegUserSch,
        session: AsyncSession = Depends(db_helper.get_async_session)
) -> OutUserSch:
    return await create_user(user, session)


@router.post("/login", tags=[settings.ACCESS_TYPE.neutral])
async def login(
        user: LoginUserSch,
        session: AsyncSession = Depends(db_helper.get_async_session)
) -> TokenInfo:
    user_db: ORMUserSch = await get_user(session, email=user.email)
    if user_db and auth_utils.match_pwd(user.pwd, user_db.pwd_hash):
        return TokenInfo(
            access_token=auth_utils.create_access_tocken(
                jwt_payload={
                    "sub": str(user_db.uuid),
                    "username": user_db.email,
                    "email": user_db.email,
                    "active": user_db.active,
                }),
            refresh_token=auth_utils.create_refrash_tocken(
                jwt_payload={"sub": str(user_db.uuid)})
        )
    else:
        raise HTTPException(status_code=400, detail="invalid email or password")


@router.get("/refresh", response_model=TokenInfo, response_model_exclude_none=True, tags=[settings.ACCESS_TYPE.refresh])
async def refresh(
        uuid: str = Depends(auth_utils.uuid_dep),
        session: AsyncSession = Depends(db_helper.get_async_session)
) -> TokenInfo:
    user_db: ORMUserSch = await get_user(session, uuid=uuid)
    return TokenInfo(access_tocken=auth_utils.create_access_tocken(
        jwt_payload={
            "sub": str(user_db.uuid),
            "username": user_db.email,
            "email": user_db.email,
            "active": user_db.active,
        }), )
