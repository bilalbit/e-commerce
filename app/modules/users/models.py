import uuid
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.core.models import TimeStampMixin, EthiopianPhoneNumber

class RoleType(Enum):
    customer = "CUSTOMER"
    seller = "SELLER"
    admin = "ADMIN"

class UsersBase(TimeStampMixin):
    email: EmailStr = Field(index=True)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    phone_number: EthiopianPhoneNumber = Field(index=True)
    role: RoleType
    is_active: bool = Field(default=True)


class Users(UsersBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, index=True, default_factory=uuid.uuid4)
    password_hash: str


class UsersCreate(UsersBase):
    password: str = Field(min_length=8)


class UsersPublic(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: EthiopianPhoneNumber


class UsersUpdate(UsersBase):
    email: EmailStr | None = None
    password_hash: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone_number: EthiopianPhoneNumber | None = None
    is_active: bool | None = None
