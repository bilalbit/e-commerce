import uuid
from enum import Enum
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

from app.core.models import TimeStampMixin, PhoneNumber, RoleType

if TYPE_CHECKING:
    from app.modules.customers.models import Customers
    from app.modules import Sellers


class UsersBase(TimeStampMixin):
    username: str = Field(min_length=3, index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    phone_number: PhoneNumber = Field(index=True, unique=True)
    is_active: bool = Field(default=True)


class Users(UsersBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, index=True, default_factory=uuid.uuid4)
    password_hash: str
    role: RoleType

    customer: "Customers" = Relationship(back_populates="user")
    seller: "Sellers" = Relationship(back_populates="user")


class UsersCreate(UsersBase):
    password: str = Field(min_length=8)


class UsersPublic(SQLModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: PhoneNumber


class UsersUpdate(UsersBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    first_name: str | None = None
    last_name: str | None = None
    phone_number: PhoneNumber | None = None
    is_active: bool | None = None
