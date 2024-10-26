__all__ = (
    "user_router",
    "history_router",
)

from src.api.v1.user.view import router as user_router
from src.api.v1.req_history.view import router as history_router
