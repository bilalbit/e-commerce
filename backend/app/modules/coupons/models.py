import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship

from backend.app.core.models import TimeStampMixin


class DiscountType(Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"


class CouponsBase(TimeStampMixin):
    code: str = Field(unique=True, index=True, max_length=20)
    discount_type: DiscountType
    discount_value: Decimal = Field(decimal_places=2,ge=1)
    min_purchase: Decimal = Field(decimal_places=2,ge=1)
    max_users: int = Field(ge=1)
    expiry_date: datetime


class Coupons(CouponsBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    is_active: bool = Field(default=True)
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    usage_count: int = Field(default=0,ge=0)

    coupon_usages: list["Coupon_Usage"] = Relationship(back_populates="coupon")


class CouponsCreate(CouponsBase):
    pass


class CouponsUpdate(SQLModel):
    code: str | None = None
    discount_type: DiscountType | None = None
    discount_value: float | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    max_users: int | None = None
    used_count: int | None = None
    is_active: bool | None = None


class Coupon_UsageBase(SQLModel):
    coupon_id: uuid.UUID = Field(foreign_key="coupons.id", index=True)
    order_id: uuid.UUID = Field(foreign_key="orders.id", index=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.id", index=True)
    used_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Coupon_Usage(Coupon_UsageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    coupon: Coupons = Relationship(back_populates="coupon_usages")
class CouponApply(SQLModel):
    code: str = Field(max_length=20)
    order_id: uuid.UUID
