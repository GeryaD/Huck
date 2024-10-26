from asyncio import current_task
from contextlib import asynccontextmanager
from idlelib.iomenu import encoding
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    async_scoped_session,
                                    AsyncSession
                                    )

from src.core import settings


class DatabaseHelper:
    """
    DB helper with generator of async session
    """

    def __init__(self, url: str, echo: bool) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.close()


db_helper = DatabaseHelper(
    settings.db.MYSQL_URL,
    settings.db.SQL_ECHO,
)
