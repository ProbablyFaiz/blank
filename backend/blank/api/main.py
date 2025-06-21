"""
This file contains the FastAPI app and its routes. Note: As the project grows, you'll
want to use FastAPI's router feature to split the routes into separate files. This is easy;
so it's perfectly alright to keep all routes in this file until it becomes unwieldy.
"""

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from blank.api.deps import get_db, get_proxy_pattern
from blank.api.interfaces import (
    ProxyPatternCreate,
    ProxyPatternRead,
    ProxyPatternUpdate,
)
from blank.db.models import ProxyPattern

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/proxy_patterns",
    response_model=list[ProxyPatternRead],
    operation_id="listProxyPatterns",
)
def list_proxy_patterns(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(ProxyPattern)).all()


@app.post(
    "/proxy_patterns",
    response_model=ProxyPatternRead,
    operation_id="createProxyPattern",
)
def create_proxy_pattern(
    pattern: ProxyPatternCreate, db: Annotated[Session, Depends(get_db)]
):
    db_pattern = ProxyPattern(**pattern.model_dump())
    db.add(db_pattern)
    db.commit()
    db.refresh(db_pattern)
    return db_pattern


@app.get(
    "/proxy_patterns/{pattern_id}",
    response_model=ProxyPatternRead,
    operation_id="readProxyPattern",
)
def read_proxy_pattern(
    proxy_pattern: Annotated[ProxyPattern, Depends(get_proxy_pattern)],
):
    return proxy_pattern


@app.patch(
    "/proxy_patterns/{pattern_id}",
    response_model=ProxyPatternRead,
    operation_id="updateProxyPattern",
)
def update_proxy_pattern(
    pattern_update: ProxyPatternUpdate,
    proxy_pattern: Annotated[ProxyPattern, Depends(get_proxy_pattern)],
    db: Annotated[Session, Depends(get_db)],
):
    for field, value in pattern_update.model_dump(exclude_unset=True).items():
        setattr(proxy_pattern, field, value)

    db.commit()
    db.refresh(proxy_pattern)
    return proxy_pattern


@app.delete(
    "/proxy_patterns/{pattern_id}",
    status_code=204,
    operation_id="deleteProxyPattern",
)
def delete_proxy_pattern(
    proxy_pattern: Annotated[ProxyPattern, Depends(get_proxy_pattern)],
    db: Annotated[Session, Depends(get_db)],
):
    db.delete(proxy_pattern)
    db.commit()
