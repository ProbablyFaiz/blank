from urllib.parse import quote_plus

import rl.utils.io
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

PG_HOST = rl.utils.io.getenv("BLANK_PG_HOST")
PG_PORT = rl.utils.io.getenv("BLANK_PG_PORT")
PG_DB = rl.utils.io.getenv("BLANK_PG_DB")

ADMIN_PG_USER = rl.utils.io.getenv("BLANK_ADMIN_PG_USER")
ADMIN_PG_PASSWORD = rl.utils.io.getenv("BLANK_ADMIN_PG_PASSWORD")

API_PG_USER = rl.utils.io.getenv("BLANK_API_PG_USER")
API_PG_PASSWORD = rl.utils.io.getenv("BLANK_API_PG_PASSWORD")


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
            "You must provide env variables BLANK_PG_HOST, BLANK_PG_PORT, BLANK_{ADMIN/API}_PG_USER, BLANK_{ADMIN/API}_PG_PASSWORD, BLANK_PG_DB."
        )

    postgres_password = quote_plus(postgres_password or "")
    return (
        f"postgresql://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )


def get_engine(postgres_uri: str):
    return sa.create_engine(
        postgres_uri,
        echo=rl.utils.io.getenv("SA_ECHO", "0") == "1",
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_pre_ping=True,
    )


ADMIN_POSTGRES_URI = get_postgres_uri(
    postgres_host=PG_HOST,
    postgres_port=PG_PORT,
    postgres_db=PG_DB,
    postgres_user=ADMIN_PG_USER,
    postgres_password=ADMIN_PG_PASSWORD,
)
API_POSTGRES_URI = get_postgres_uri(
    postgres_host=PG_HOST,
    postgres_port=PG_PORT,
    postgres_db=PG_DB,
    postgres_user=API_PG_USER,
    postgres_password=API_PG_PASSWORD,
)


ADMIN_ENGINE = get_engine(ADMIN_POSTGRES_URI)
API_ENGINE = get_engine(API_POSTGRES_URI)

AdminSessionLocal = sessionmaker(bind=ADMIN_ENGINE)
ApiSessionLocal = sessionmaker(bind=API_ENGINE)


def get_session() -> Session:
    """Get a new admin session. Caller is responsible for closing."""
    return AdminSessionLocal()


def get_api_session() -> Session:
    """Get a new API session. Caller is responsible for closing."""
    return ApiSessionLocal()
