from app.database import session
from .models import *
from app.core.services import get_record_by_id


def db_get_categories():
    with session:
        return session.query(Categories).all()

def db_get_categories_by_id(id:uuid.UUID):
    with session:
        return get_record_by_id(id, Categories,"Category")

def db_add_categories(categories_data: CategoriesCreate):
    with session:
        db_categories = Categories.model_validate(categories_data)
        session.add(db_categories)
        session.commit()
        session.refresh(db_categories)
        return db_categories

def db_update_categories(id:uuid.UUID, categories_data: CategoriesUpdate):
    with session:
        db_categories = db_get_categories_by_id(id)
        categories_update = categories_data.model_dump(exclude_unset=True)
        db_categories.sqlmodel_update(categories_update)
        session.add(db_categories)
        session.commit()
        session.refresh(db_categories)
        return db_categories
def db_delete_categories(id:uuid.UUID):
    with session:
        db_categories = db_get_categories_by_id(id)
        session.delete(db_categories)
        session.commit()
