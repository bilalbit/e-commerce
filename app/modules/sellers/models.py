import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.users.models import Users


class SellersBase(SQLModel):
    business_name: str = Field(min_length=3)
    business_address: str = Field(min_length=3)
    tax_id: str = Field(min_length=3)
    verified: bool = Field(default=False)


class Sellers(SellersBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id", index=True, unique=True, ondelete="CASCADE")

    user: "Users" = Relationship(back_populates="seller")


class SellersCreate(SellersBase):
    pass


class SellersUpdate(SQLModel):
    business_name: str | None = None
    business_address: str | None = None
    tax_id: str | None = None
    verified: bool | None = None
