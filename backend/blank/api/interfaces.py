import math
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, computed_field

from blank.db.models import PatternType


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


DataT = TypeVar("DataT")


class PaginatedBase(ApiModel, Generic[DataT]):
    items: list[DataT]
    total: int
    page: int
    size: int

    @computed_field
    def next_page(self) -> int | None:
        return self.page + 1 if self.page * self.size < self.total else None

    @computed_field
    def num_pages(self) -> int:
        return math.ceil(self.total / self.size) if self.size > 0 else 0


class ProxyPatternCreate(ApiModel):
    pattern: str
    enabled: bool = True


class ProxyPatternBase(ApiModel):
    id: int
    enabled: bool
    pattern_type: PatternType


class ProxyPatternRead(ProxyPatternBase):
    pattern: str
    created_at: datetime
    updated_at: datetime


class ProxyPatternItem(ProxyPatternBase):
    pass


class ProxyPatternUpdate(ApiModel):
    pattern: str | None = None
    enabled: bool | None = None
