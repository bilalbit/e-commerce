import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated, Literal

from fastapi import Query
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from sqlmodel import Field, SQLModel

from app.core.config import get_settings


class TimeStampMixin(SQLModel):
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = Field(default=None, sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)})


class FilterParams(SQLModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


filter_query = Annotated[FilterParams, Query()]
PhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        supported_regions=get_settings().supported_regions,
        default_region=get_settings().default_region,
        number_format=get_settings().number_format
    )
]


class RoleType(Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"


class UserSchema(SQLModel):
    id: uuid.UUID
    username: str = Field(min_length=3)
    role: RoleType


class Token(SQLModel):
    access_token: str
    token_type: str
