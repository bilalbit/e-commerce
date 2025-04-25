import uuid
from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship


class WishlistsBase(SQLModel):
    customer_id: uuid.UUID = Field(foreign_key="customers.id", unique=True, index=True, ondelete="CASCADE")
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))


class Wishlists(WishlistsBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    wishlist_items: list["Wishlist_Items"] = Relationship(back_populates="wishlists",passive_deletes="all")


class WishlistPublic(WishlistsBase):
    id: uuid.UUID
    wishlist_items: list["Wishlist_Items"]


class Wishlist_ItemsBase(SQLModel):
    wishlist_id: uuid.UUID = Field(foreign_key="wishlists.id", index=True, ondelete="CASCADE")
    product_id: uuid.UUID = Field(foreign_key="products.id", index=True, ondelete="CASCADE")
    added_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), exclude=True)


class Wishlist_Items(Wishlist_ItemsBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True, index=True)

    wishlists: "Wishlists" = Relationship(back_populates="wishlist_items")
