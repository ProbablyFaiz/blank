from collections.abc import AsyncGenerator
from typing import Annotated

import httpx
import sqlalchemy as sa
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_auth0 import Auth0, Auth0User
from redis.asyncio import Redis as AsyncRedis
from sqlalchemy.ext.asyncio import AsyncSession

import blanket.io.env as env
from blanket.db.models import Task, User
from blanket.db.redis import get_redis_client
from blanket.db.session import get_api_session

auth = Auth0(
    domain=env.getenv("BLANKET_AUTH0_DOMAIN"),
    api_audience=env.getenv("BLANKET_AUTH0_AUDIENCE"),
    lazy_init=True,
)

security = HTTPBearer()


async def _get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_api_session() as session:
        yield session


def get_user_email(token: str) -> str:
    url = f"https://{auth.domain}/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    client = httpx.Client()
    response = client.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()["email"]


async def get_or_create_user(
    auth0_user: Auth0User,
    token: str,
    db: AsyncSession,
) -> User:
    stmt = sa.select(User).where(User.auth0_sub == auth0_user.id)
    user = await db.scalar(stmt)

    if not user:
        # Check for existing user with matching email but null auth0_id
        email = get_user_email(token)
        stmt = sa.select(User).where(User.email == email, User.auth0_sub.is_(None))
        user = await db.scalar(stmt)
        if user:
            user.auth0_sub = auth0_user.id
            await db.commit()
            await db.refresh(user)
            return user

        # For now, we don't allow users to sign up unles we've already added them
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_token(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    return creds.credentials


async def get_current_user(
    auth0_user: Annotated[Auth0User, Security(auth.get_user)],
    token: Annotated[str, Depends(get_token)],
    db: Annotated[AsyncSession, Depends(_get_db)],
) -> User:
    user = await get_or_create_user(auth0_user, token, db)
    return user


async def set_user_context(db: AsyncSession, user: User) -> None:
    """Set PostgreSQL session variables for RLS policies."""
    await db.execute(sa.text("SELECT set_current_user(:uid)"), {"uid": user.id})


def get_unauthenticated_db(
    db: Annotated[AsyncSession, Depends(_get_db)],
) -> AsyncSession:
    return db


async def get_user_db(
    db: Annotated[AsyncSession, Depends(_get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> AsyncSession:
    await set_user_context(db, user)
    return db


def get_redis() -> AsyncRedis:
    return get_redis_client()


async def get_task(db: Annotated[AsyncSession, Depends(_get_db)], task_id: int) -> Task:
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
