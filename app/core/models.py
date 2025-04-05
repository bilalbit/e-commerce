from datetime import datetime, timezone
from typing import Union,Annotated

from sqlmodel import Field, SQLModel
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

class TimeStampMixin(SQLModel):
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        exclude=True,
        nullable=False
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
        exclude=True
    )


EthiopianPhoneNumber = Annotated[
    str,
    PhoneNumberValidator(
        supported_regions=["ET"],  # Only allow Ethiopian region
        default_region="ET",       # Default to Ethiopia
        number_format="E164",      # Standard format (e.g., +251912345678)
    )
]


