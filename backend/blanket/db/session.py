import asyncio
import weakref
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool, QueuePool

import blanket.io.env as env

PG_HOST = env.getenv("BLANKET_PG_HOST")
PG_PORT = env.getenv("BLANKET_PG_PORT")
PG_DB = env.getenv("BLANKET_PG_DB")

PG_SUPERUSER_USER = env.getenv("BLANKET_PG_SUPERUSER_USER")
PG_SUPERUSER_PASSWORD = env.getenv("BLANKET_PG_SUPERUSER_PASSWORD")
PG_ADMIN_USER = env.getenv("BLANKET_PG_ADMIN_USER")
PG_ADMIN_PASSWORD = env.getenv("BLANKET_PG_ADMIN_PASSWORD")
PG_API_USER = env.getenv("BLANKET_PG_API_USER")
PG_API_PASSWORD = env.getenv("BLANKET_PG_API_PASSWORD")


def get_postgres_uri(
    postgres_host: str,
    postgres_port: str,
    postgres_user: str,
    postgres_password: str,
    postgres_db: str,
    async_mode: bool = False,
) -> str:
    if any(
        [
            not postgres_host,
            not postgres_port,
            not postgres_user,
            not postgres_db,
        ]
    ):
        raise ValueError(
            "You must provide env variables BLANKET_PG_HOST, BLANKET_PG_PORT, BLANKET_PG_{ADMIN,API,SUPERUSER}_USER, BLANKET_PG_{ADMIN,API,SUPERUSER}_PASSWORD, BLANKET_PG_DB."
        )

    postgres_password = quote_plus(postgres_password or "")
    prefix = "postgresql+asyncpg://" if async_mode else "postgresql://"
    return f"{prefix}{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


def _create_async_engine(postgres_uri: str) -> AsyncEngine:
    return create_async_engine(
        postgres_uri,
        echo=env.getenv("BLANKET_SA_ECHO", "0") == "1",
        poolclass=AsyncAdaptedQueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
    )


def _create_sync_engine(postgres_uri: str) -> Engine:
    return create_engine(
        postgres_uri,
        echo=env.getenv("BLANKET_SA_ECHO", "0") == "1",
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
    )


@dataclass
class _LoopResources:
    engine: AsyncEngine
    sessionmaker: async_sessionmaker[AsyncSession]


_admin_resources: weakref.WeakKeyDictionary[AbstractEventLoop, _LoopResources] = (
    weakref.WeakKeyDictionary()
)
_api_resources: weakref.WeakKeyDictionary[AbstractEventLoop, _LoopResources] = (
    weakref.WeakKeyDictionary()
)

_SUPERUSER_POSTGRES_URI: str | None = None
_ADMIN_POSTGRES_URI: str | None = None
_API_POSTGRES_URI: str | None = None

_SUPERUSER_ENGINE: Engine | None = None


def get_admin_postgres_uri() -> str:
    global _ADMIN_POSTGRES_URI
    if _ADMIN_POSTGRES_URI is None:
        _ADMIN_POSTGRES_URI = get_postgres_uri(
            postgres_host=PG_HOST,
            postgres_port=PG_PORT,
            postgres_db=PG_DB,
            postgres_user=PG_ADMIN_USER,
            postgres_password=PG_ADMIN_PASSWORD,
            async_mode=True,
        )
    return _ADMIN_POSTGRES_URI


def get_api_postgres_uri() -> str:
    global _API_POSTGRES_URI
    if _API_POSTGRES_URI is None:
        _API_POSTGRES_URI = get_postgres_uri(
            postgres_host=PG_HOST,
            postgres_port=PG_PORT,
            postgres_db=PG_DB,
            postgres_user=PG_API_USER,
            postgres_password=PG_API_PASSWORD,
            async_mode=True,
        )
    return _API_POSTGRES_URI


def get_superuser_postgres_uri() -> str:
    global _SUPERUSER_POSTGRES_URI
    if _SUPERUSER_POSTGRES_URI is None:
        _SUPERUSER_POSTGRES_URI = get_postgres_uri(
            postgres_host=PG_HOST,
            postgres_port=PG_PORT,
            postgres_db=PG_DB,
            postgres_user=PG_SUPERUSER_USER,
            postgres_password=PG_SUPERUSER_PASSWORD,
            async_mode=False,
        )
    return _SUPERUSER_POSTGRES_URI


def get_superuser_engine() -> Engine:
    """Get a sync superuser engine for use with Alembic migrations."""
    global _SUPERUSER_ENGINE
    if _SUPERUSER_ENGINE is None:
        _SUPERUSER_ENGINE = _create_sync_engine(get_superuser_postgres_uri())
    return _SUPERUSER_ENGINE


def _get_admin_resources() -> _LoopResources:
    loop = asyncio.get_running_loop()
    if loop not in _admin_resources:
        engine = _create_async_engine(get_admin_postgres_uri())
        _admin_resources[loop] = _LoopResources(
            engine=engine,
            sessionmaker=async_sessionmaker(bind=engine, expire_on_commit=False),
        )
    return _admin_resources[loop]


def _get_api_resources() -> _LoopResources:
    loop = asyncio.get_running_loop()
    if loop not in _api_resources:
        engine = _create_async_engine(get_api_postgres_uri())
        _api_resources[loop] = _LoopResources(
            engine=engine,
            sessionmaker=async_sessionmaker(bind=engine, expire_on_commit=False),
        )
    return _api_resources[loop]


def get_admin_engine() -> AsyncEngine:
    return _get_admin_resources().engine


def get_admin_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return _get_admin_resources().sessionmaker


def get_api_engine() -> AsyncEngine:
    return _get_api_resources().engine


def get_api_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return _get_api_resources().sessionmaker


def get_admin_session() -> AsyncSession:
    """Get a new admin session. Use `async with` to ensure the session is closed."""
    return get_admin_sessionmaker()()


def get_api_session() -> AsyncSession:
    """Get a new API session. Use `async with` to ensure the session is closed."""
    return get_api_sessionmaker()()
