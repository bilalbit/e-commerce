import uuid
from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.modules import Products


class CategoriesBase(SQLModel):
    name: str = Field(min_length=3)
    description: str = Field(max_length=500)


class Categories(CategoriesBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    parent_category_id: uuid.UUID | None = Field(default=None, foreign_key="categories.id", index=True, nullable=True,
                                                 ondelete="CASCADE")

    products: list["Products"] = Relationship(back_populates="category")


class CategoriesCreate(CategoriesBase):
    parent_category_id: uuid.UUID | None = None


class CategoriesUpdate(CategoriesBase):
    name: str | None = None
    description: str | None = None
