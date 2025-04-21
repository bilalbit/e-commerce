from fastapi import APIRouter

from app.dependencies import current_customer_dependency
from .services import *

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.post('/')
def add_review(review_data: ReviewCreate, customer: current_customer_dependency):
    return db_add_review(customer.id, review_data)


@router.get('/product/{id}')
def get_product_review(id: uuid.UUID):
    return db_get_product_review(id)


@router.patch('/reviews/{id}')
def update_review(id: uuid.UUID, review_data: ReviewUpdate, customer: current_customer_dependency):
    return db_update_review(id, customer.id, review_data)


@router.delete('/reviews/{id}')
def delete_review(id: uuid.UUID, customer: current_customer_dependency):
    return db_delete_review(id, customer.id)
