from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.api.v1 import user_router
from src.core import settings
from src.core.middleware.process_time import ProcessTimeMiddleware
from src.core.middleware.token_pass import PassByTokenMiddleware
from src.core.settings import ACCESS_TYPE

# add group router

app = FastAPI()


# ping-pong router
@app.get("/ping", tags=["Ping-Pong", ACCESS_TYPE.neutral])
async def ping_pong():
    return "pong"


# Adding routers
routers: list[APIRouter] = [
    # doc_router,
    user_router,
]
for router in routers:
    app.include_router(router)


# Crete the dict of token_type_pass - uri
pass_uri = {
    settings.ACCESS_TYPE.access: (),
    settings.ACCESS_TYPE.neutral: (),
    settings.ACCESS_TYPE.refresh: (),
}

for route in app.router.__dict__["routes"]:
    if hasattr(route, "tags"):
        pass_uri[route.__dict__["tags"][-1]] += (route.__dict__["path"],)


# Middlewares
app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(PassByTokenMiddleware, pass_uri=pass_uri)
app.add_middleware(GZipMiddleware)


# Adding caching
@asynccontextmanager
async def lifespan():
    redis = aioredis.from_url(settings.redis.REDIS_URL, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
