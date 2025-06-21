from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from blank.db.models import ProxyPattern
from blank.db.session import get_api_session


def get_db() -> Generator[Session, None, None]:
    with get_api_session() as session:
        yield session


def get_proxy_pattern(
    db: Annotated[Session, Depends(get_db)], pattern_id: int
) -> ProxyPattern:
    proxy_pattern = db.get(ProxyPattern, pattern_id)
    if not proxy_pattern:
        raise HTTPException(status_code=404, detail="Proxy pattern not found")
    return proxy_pattern
