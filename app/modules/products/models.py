import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.core.models import TimeStampMixin

if TYPE_CHECKING:
    from app.modules import Categories, Reviews


class ProductsBase(SQLModel):
    name: str = Field(min_length=3, index=True)
    description: str = Field(max_length=500)
    price: Decimal = Field(decimal_places=2, index=True, ge=1)
    stock_quantity: int = Field(default=1, ge=1)
    is_available: bool = Field(default=True)
    category_id: uuid.UUID = Field(default=None, foreign_key="categories.id",
                                   index=True, ondelete="SET NULL", nullable=True)


class Products(ProductsBase, TimeStampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    seller_id: uuid.UUID | None = Field(foreign_key="sellers.id", ondelete="CASCADE")
    ##Relationships
    category: "Categories" = Relationship(back_populates="products")
    reviews: list["Reviews"] = Relationship(back_populates="products")


class ProductsCreate(ProductsBase):
    pass


class ProductsUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(decimal_places=2, default=None)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_available: bool | None = None
    category_id: uuid.UUID | None = None


class ProductsPublic(ProductsBase):
    id: uuid.UUID
