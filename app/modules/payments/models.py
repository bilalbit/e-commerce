import uuid
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel


class PaymentMethod(Enum):
    credit_card = "credit_card"
    debit_card = "debit_card"
    paypal = "paypal"
    payoneer = "payoneer"


class PaymentStatus(Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


class PaymentBase(SQLModel):
    order_id: uuid.UUID = Field(foreign_key="orders.id", unique=True, index=True)
    amount: Decimal = Field(decimal_places=2, ge=1)
    payment_method: PaymentMethod
    transaction_id: str = Field(unique=True)


class Payments(PaymentBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="customers.id", unique=True, index=True)
    status: PaymentStatus = Field(default=PaymentStatus.pending)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(SQLModel):
    status: PaymentStatus | None = None
