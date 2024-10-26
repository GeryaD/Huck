from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core import settings


def uuid_dep(
        credantials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    payload = decode_jwt(credantials.credentials)
    return payload.get("sub")


def hash_pwd(pwd: str):
    salt = bcrypt.gensalt()
    pwd_bytes = pwd.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def match_pwd(pwd: str, hashed_pwd: bytes):
    return bcrypt.checkpw(pwd.encode("UTF-8"), hashed_pwd)


def decode_jwt(
        token: str | bytes,
        public_key: str | bytes = settings.app.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.app.JWT_ALGORITHM
) -> dict[str]:
    try:
        decoded = jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=algorithm
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            401,
            detail=f"invalid token error {e}"
        )
    return decoded


def encode_jwt(
        payload: dict,
        private_key: str | bytes = settings.app.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.app.JWT_ALGORITHM,
        expire_minutes: int = settings.app.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
):
    to_encode = payload.copy()
    utc_time_now = datetime.now(tz=timezone.utc)
    expire = utc_time_now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=utc_time_now
    )
    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm
    )
    return encoded


def create_jwt(token_data: dict, token_type: str, expire_minutes: int) -> str:
    jwt_payload = {"token": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=jwt_payload, expire_minutes=expire_minutes)


def create_refrash_tocken(jwt_payload: dict) -> str:
    """
    :jwt_payload = {
        "sub": str(user.uuid),
    }
    """
    return create_jwt(token_data=jwt_payload, token_type="refresh",
                      expire_minutes=settings.app.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)


def create_access_tocken(jwt_payload: dict) -> str:
    """
    :jwt_payload = {
        "sub": str(user.uuid),
        "username": user.email,
        "email": user.email,
        "activ": user.active,
    }
    """
    return create_jwt(token_data=jwt_payload, token_type="access",
                      expire_minutes=settings.app.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
