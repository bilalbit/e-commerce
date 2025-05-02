from typing import Annotated

from fastapi import APIRouter, File

from backend.app.database import db_session
from backend.app.dependencies import current_seller_dependency
from .services import *

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def add_product(product_data: ProductsCreate,seller: current_seller_dependency):
    return db_add_product(product_data,seller.id)


@router.get('/', response_model=list[ProductsPublic])
def get_products(filter_q: filter_query, db_session_dep: db_session):
    return db_get_products(filter_q, db_session_dep)
@router.get('/{id}')
def get_products_by_id(id: uuid.UUID):
    return db_get_products_by_id(id)

@router.patch('/{id}')
def update_product(id: uuid.UUID,product_data: ProductsUpdate,seller: current_seller_dependency):
    return db_update_product(id,product_data,seller.id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: uuid.UUID,seller: current_seller_dependency):
    return db_delete_product(id,seller.id)


@router.post('/images/{id}', status_code=status.HTTP_201_CREATED)
async def add_product_images(id: uuid.UUID,
                             product_image: Annotated[list[UploadFile], File(description="images of product")],
                             seller: current_seller_dependency):
    if len(product_image) > 6:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="product Images must be less than 6 images")
    try:
        image_urls = await db_add_product_images(id, product_image, seller.id)
        return {"message": "Images uploaded successfully", "image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/image/{product_id}', status_code=status.HTTP_201_CREATED)
async def add_product_image(product_id: uuid.UUID,
                            product_image: Annotated[UploadFile, File(description="image of product")],
                            seller: current_seller_dependency, is_primary: bool = False):
    try:
        image_urls = await db_add_product_image(product_id, product_image, is_primary, seller.id)
        return {"message": "Images uploaded successfully", "image_urls": image_urls}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch('/image/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def update_product_image(id: uuid.UUID,
                               product_image: Annotated[UploadFile, File(description="image of product")],
                               seller: current_seller_dependency):
    try:
        await db_update_product_image(id, product_image, seller.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete('/image/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(id: uuid.UUID, seller: current_seller_dependency):
    try:
        await db_delete_product_image(id, seller.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete('/images/{product_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def clear_product_image(product_id: uuid.UUID, seller: current_seller_dependency):
    try:
        await db_clear_product_image(product_id, seller.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
