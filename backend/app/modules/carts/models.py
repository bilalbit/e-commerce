import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from backend.app.core.models import TimeStampMixin

if TYPE_CHECKING:
    from backend.app.modules import Customers


class CartItemBase(SQLModel):
    cart_id: uuid.UUID = Field(unique=True,foreign_key="carts.id", ondelete="CASCADE", index=True)
    product_id: uuid.UUID = Field(unique=True, foreign_key="products.id", ondelete="SET NULL",
                                  index=True, nullable=True)
    quantity: int = Field(ge=1)
    added_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))


class CartItems(CartItemBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    cart: "Carts" = Relationship(back_populates="cart_items")


class Carts(TimeStampMixin, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.id", ondelete="CASCADE", unique=True,
                                   index=True)

    cart_items: list["CartItems"] = Relationship(back_populates="cart", passive_deletes="all")
    customer: "Customers" = Relationship(back_populates="cart")


class CartsCreate(SQLModel):
    product_id: uuid.UUID
    quantity: int = Field(ge=1)


class CartsPublic(SQLModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    cart_items: list["CartItems"]


class CartsUpdate(SQLModel):
    quantity: int = Field(ge=1)
