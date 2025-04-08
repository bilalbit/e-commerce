import uuid

from sqlmodel import Field, SQLModel


class CustomersBase(SQLModel):
    address_line1: str = Field(min_length=3,max_length=255)
    address_line2: str = Field(min_length=3,max_length=255)
    city: str = Field(min_length=3)
    state: str = Field(min_length=3)
    postalcode: str = Field(min_length=3,max_length=10)


class CustomersUpdate(SQLModel):
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postalcode: str | None = None


class Customers(CustomersBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: int | None = Field(foreign_key="users.id", index=True, unique=True, ondelete="CASCADE")
