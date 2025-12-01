from urllib.parse import quote_plus

import sqlalchemy as sa
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

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
):
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
        f"postgresql://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )


def get_engine(postgres_uri: str):
    return sa.create_engine(
        postgres_uri,
        echo=env.getenv("BLANKET_SA_ECHO", "0") == "1",
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
    )


_ADMIN_POSTGRES_URI: str | None = None
_API_POSTGRES_URI: str | None = None

_ADMIN_SESSION_LOCAL: sessionmaker | None = None
_API_SESSION_LOCAL: sessionmaker | None = None

_ADMIN_ENGINE: Engine | None = None
_API_ENGINE: Engine | None = None


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


def get_admin_engine() -> Engine:
    global _ADMIN_ENGINE
    if _ADMIN_ENGINE is None:
        _ADMIN_ENGINE = get_engine(get_admin_postgres_uri())
    return _ADMIN_ENGINE


def get_admin_sessionmaker() -> sessionmaker:
    global _ADMIN_SESSION_LOCAL
    if _ADMIN_SESSION_LOCAL is None:
        _ADMIN_SESSION_LOCAL = sessionmaker(bind=get_admin_engine())
    return _ADMIN_SESSION_LOCAL


def get_api_engine() -> Engine:
    global _API_ENGINE
    if _API_ENGINE is None:
        _API_ENGINE = get_engine(get_api_postgres_uri())
    return _API_ENGINE


def get_api_sessionmaker() -> sessionmaker:
    global _API_SESSION_LOCAL
    if _API_SESSION_LOCAL is None:
        _API_SESSION_LOCAL = sessionmaker(bind=get_api_engine())
    return _API_SESSION_LOCAL


def get_session() -> Session:
    """Get a new admin session. Caller is responsible for closing."""
    return get_admin_sessionmaker()()


def get_api_session() -> Session:
    """Get a new API session. Caller is responsible for closing."""
    return get_api_sessionmaker()()
