import uuid
from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

from backend.app.core.models import TimeStampMixin, PhoneNumber, RoleType, FileUrl

if TYPE_CHECKING:
    from backend.app.modules.customers.models import Customers
    from backend.app.modules import Sellers


class User_ImagesBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True, unique=True, ondelete="CASCADE")
    img_url: FileUrl


class User_Images(User_ImagesBase, table=True):
    id: uuid.UUID | None = Field(primary_key=True, index=True, default_factory=uuid.uuid4)
    img_url: str

    user: "Users" = Relationship(back_populates="user_profile", passive_deletes="all")

class UsersBase(SQLModel):
    username: str = Field(min_length=3, index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    phone_number: PhoneNumber = Field(index=True, unique=True)
    is_active: bool = Field(default=True)


class Users(UsersBase, TimeStampMixin, table=True):
    id: uuid.UUID | None = Field(primary_key=True, index=True, default_factory=uuid.uuid4)
    password_hash: str
    role: RoleType

    customer: "Customers" = Relationship(back_populates="user")
    seller: "Sellers" = Relationship(back_populates="user")
    user_profile: "User_Images" = Relationship(back_populates="user")



class UsersCreate(UsersBase):
    password: str = Field(min_length=8)
    role: RoleType | None = None


class UsersPublic(SQLModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: PhoneNumber
    role: RoleType

    user_profile: "User_Images" = None

class UsersUpdate(UsersBase):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    first_name: str | None = None
    last_name: str | None = None
    phone_number: PhoneNumber | None = None
    is_active: bool | None = None
