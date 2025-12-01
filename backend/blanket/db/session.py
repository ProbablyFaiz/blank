import asyncio
import weakref
from asyncio import AbstractEventLoop
from dataclasses import dataclass
from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

import blanket.io.env as env

PG_HOST = env.getenv("BLANKET_PG_HOST")
PG_PORT = env.getenv("BLANKET_PG_PORT")
PG_DB = env.getenv("BLANKET_PG_DB")
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
            "You must provide env variables BLANKET_PG_HOST, BLANKET_PG_PORT, BLANKET_PG_{ADMIN,API}_USER, BLANKET_PG_{ADMIN,API}_PASSWORD, BLANKET_PG_DB."
        )

    postgres_password = quote_plus(postgres_password or "")
    return (
        f"postgresql+asyncpg://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )


def _create_engine(postgres_uri: str) -> AsyncEngine:
    return create_async_engine(
        postgres_uri,
        echo=env.getenv("BLANKET_SA_ECHO", "0") == "1",
        poolclass=AsyncAdaptedQueuePool,
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

_ADMIN_POSTGRES_URI: str | None = None
_API_POSTGRES_URI: str | None = None


def get_admin_postgres_uri() -> str:
    global _ADMIN_POSTGRES_URI
    if _ADMIN_POSTGRES_URI is None:
        _ADMIN_POSTGRES_URI = get_postgres_uri(
            postgres_host=PG_HOST,
            postgres_port=PG_PORT,
            postgres_db=PG_DB,
            postgres_user=PG_ADMIN_USER,
            postgres_password=PG_ADMIN_PASSWORD,
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
        )
    return _API_POSTGRES_URI


def _get_admin_resources() -> _LoopResources:
    loop = asyncio.get_running_loop()
    if loop not in _admin_resources:
        engine = _create_engine(get_admin_postgres_uri())
        _admin_resources[loop] = _LoopResources(
            engine=engine,
            sessionmaker=async_sessionmaker(bind=engine, expire_on_commit=False),
        )
    return _admin_resources[loop]


def _get_api_resources() -> _LoopResources:
    loop = asyncio.get_running_loop()
    if loop not in _api_resources:
        engine = _create_engine(get_api_postgres_uri())
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
