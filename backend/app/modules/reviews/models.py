import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship

from backend.app.core.models import TimeStampMixin

if TYPE_CHECKING:
    from backend.app.modules import Products


class ReviewBase(SQLModel):
    product_id: uuid.UUID = Field(foreign_key="products.id", index=True, ondelete="CASCADE")
    order_id: uuid.UUID = Field(foreign_key="orders.id", index=True, ondelete="CASCADE")
    rating: Decimal = Field(ge=1, le=10, decimal_places=2)
    comment: str = Field(default=None,max_items=255,nullable=True)


class Reviews(ReviewBase, TimeStampMixin, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.id", index=True, ondelete="SET NULL", nullable=True)


    products: "Products" = Relationship(back_populates="reviews", passive_deletes="CASCADE")

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(SQLModel):
    rating: Decimal | None = Field(default=None,ge=1, le=10, decimal_places=2)
    comment: str | None = Field(default=None,max_items=255,nullable=True)
