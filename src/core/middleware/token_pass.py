from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import jwt

from src.core import settings
from src.core.settings import ACCESS_TYPE


class PassByTokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware for pass by token with using tags of endpoints
    """

    def __init__(self, app: ASGIApp, pass_uri: dict[str, str]):
        super().__init__(app)
        self.pass_uri = pass_uri

    async def dispatch(self, request: Request, call_next):
        token = {"token": None}
        authorization = request.headers.get("authorization")

        if authorization:
            scheme, param = authorization.split(" ")
            token = self.decode_jwt(param)

        if (
                (token["token"] == ACCESS_TYPE.access and request.url.path not in self.pass_uri[ACCESS_TYPE.refresh]) or
                (token["token"] == ACCESS_TYPE.refresh and request.url.path in self.pass_uri[ACCESS_TYPE.refresh]) or
                (request.url.path.startswith(self.pass_uri[ACCESS_TYPE.neutral])) or
                (request.url.path in ["/docs", "/openapi.json"])
        ):
            return await call_next(request)
        else:
            return JSONResponse(status_code=403, content="log in or register")

    '''
    Copy of function from ..auth_utils.auth_utils :( 
    '''
    @staticmethod
    def decode_jwt(
            token: str | bytes,
            public_key: str | bytes = settings.app.PUBLIC_KEY_PATH.read_text(),
            algorithm: str = settings.app.JWT_ALGORITHM
    ):
        try:
            decoded = jwt.decode(
                jwt=token,
                key=public_key,
                algorithms=algorithm
            )
            return decoded
        except jwt.InvalidTokenError as e:
            return JSONResponse(status_code=401, content=f"log in or register {e}")

