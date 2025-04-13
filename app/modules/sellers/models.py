import uuid

from sqlmodel import Field, Relationship, SQLModel

from app.modules.users.models import Users, UsersPublic


class SellersBase(SQLModel):
    business_name: str = Field(min_length=3)
    business_address: str = Field(min_length=3)
    tax_id: str = Field(min_length=3)


class Sellers(SellersBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    verified: bool = Field(default=False)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="users.id", index=True, unique=True, ondelete="CASCADE")

    user: "Users" = Relationship(back_populates="seller")


class SellersCreate(SellersBase):
    pass


class SellersPublic(SellersBase):
    business_name: str | None = None
    business_address: str | None = None
    tax_id: str | None = None
    verified: bool | None = None


class SellersPublicWithUsers(UsersPublic):
    seller: SellersPublic


class SellersUpdate(SQLModel):
    business_name: str | None = None
    business_address: str | None = None
    tax_id: str | None = None
