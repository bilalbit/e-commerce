import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.modules.users.models import UsersPublic

# if TYPE_CHECKING:
from app.modules import Users


class CustomersBase(SQLModel):
    address_line1: str = Field(min_length=3, max_length=255)
    address_line2: str = Field(default=None, min_length=3, max_length=255)
    city: str = Field(min_length=3)
    state: str = Field(min_length=3)
    postalcode: str = Field(min_length=3, max_length=10)


class Customers(CustomersBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id", index=True, unique=True, ondelete="CASCADE")

    user: "Users" = Relationship(back_populates="customer")


class CustomersCreate(CustomersBase):
    pass


class CustomersPublic(CustomersBase):
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postalcode: str | None = None


class CustomerPublicWithUser(UsersPublic):
    customer: CustomersPublic
# class CustomerPublicWithUser(CustomersPublic):
    # user: UsersPublic


class CustomersUpdate(SQLModel):
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postalcode: str | None = None
