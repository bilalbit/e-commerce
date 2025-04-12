import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated

from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from sqlmodel import Field, SQLModel


class TimeStampMixin(SQLModel):
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        exclude=True,
        nullable=False
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        exclude=True
    )


EthiopianPhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        supported_regions=["ET"],  # Only allow Ethiopian region
        default_region="ET",  # Default to Ethiopia
        number_format="E164",  # Standard format (e.g., +251912345678)
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
