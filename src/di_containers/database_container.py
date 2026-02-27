from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings.db_settings import AbstractDBConfig


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, config: AbstractDBConfig) -> AsyncEngine:
        return create_async_engine(
            url=config.dsn,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False} if "sqlite" in config.dsn else {},
        )

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
        )

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            print("injecting session")
            yield session
