import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from app.modules import Customers


class OrderItemBase(SQLModel):
    product_id: uuid.UUID = Field(foreign_key="products.id", index=True, ondelete="CASCADE")
    quantity: int = Field(ge=1)
    price_at_purchase: Decimal = Field(decimal_places=2)

class OrderItemPublic(OrderItemBase):
    id: uuid.UUID

class OrderItem(OrderItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    order_id: uuid.UUID = Field(foreign_key="orders.id", index=True, ondelete="CASCADE")

    # Relationship
    order: "Orders" = Relationship(back_populates="order_items")


class OrderStatus(Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderBase(SQLModel):
    customer_id: uuid.UUID = Field(foreign_key="customers.id", index=True, ondelete="CASCADE")
    order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_amount: Decimal = Field(ge=1, decimal_places=2)
    status: OrderStatus = Field(default=OrderStatus.pending)
    shipping_address: str = Field(default=None,min_length=3, max_length=255,nullable=True)


class Orders(OrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    ##relationship M-1
    # customer: "Customers" = Relationship(back_populates="orders", passive_deletes=True)
    order_items: list["OrderItem"] = Relationship(back_populates="order", passive_deletes="all")



class OrdersPublic(OrderBase):
    id: uuid.UUID
    order_items: list["OrderItemPublic"]
