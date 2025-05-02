from fastapi import HTTPException, status, UploadFile
from sqlmodel import select, Session

from backend.app.core.models import filter_query
from backend.app.core.services import get_record_by_id
from backend.app.database import session, supabase
from .models import *

bucket_name = "e-commerce"  # Your Supabase bucket name must be from.env


def db_add_product(product_data: ProductsCreate, seller_id: uuid.UUID):
    with session:
        db_product = Products.model_validate(product_data, update={"seller_id": seller_id})
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


def db_get_products(filter_q: filter_query, db_session: Session):
    statement = select(Products).offset(filter_q.offset).limit(filter_q.limit).order_by(filter_q.order_by)
    product = db_session.exec(statement).all()
    return product


def db_get_products_by_id(id: uuid.UUID):
    with session:
        return get_record_by_id(id, Products, "products")


def db_update_product(id: uuid.UUID, product_data: ProductsUpdate, seller_id: uuid.UUID):
    with session:
        db_product = db_get_products_by_id(id)
        product_update = product_data.model_dump(exclude_unset=True)
        if seller_id != db_product.seller_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You are not authorized to perform this action.")
        db_product.sqlmodel_update(product_update)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        return db_product


def db_update_product_stock_quantity(id: uuid.UUID, quantity: int):
    with session:
        db_product = db_get_products_by_id(id)
        if db_product.stock_quantity < quantity:
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Insufficient stock")
        db_product.stock_quantity -= quantity
        session.add(db_product)
        session.commit()


def db_delete_product(id: uuid.UUID, seller_id: uuid.UUID):
    with session:
        db_product = db_get_products_by_id(id)
        if seller_id != db_product.seller_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="You are not authorized to perform this action.")
        session.delete(db_product)
        session.commit()


def db_get_seller_product(product_id: uuid.UUID, seller_id: uuid.UUID, db_session: Session = session):
    with db_session:
        db_product = session.exec(
            select(Products).where(
                Products.id == product_id,
                Products.seller_id == seller_id
            )
        ).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product


async def db_add_product_image(product_id: uuid.UUID, product_image: UploadFile, is_primary: bool,
                               seller_id: uuid.UUID):
    with session:
        db_get_seller_product(product_id, seller_id, session)
        file_extension = product_image.filename.split('.')[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"product-images/{product_id}/{file_name}"
        if is_primary:  ##
            db_product_image = session.exec(select())
        file_content = await product_image.read()
        try:
            response = supabase.storage.from_(bucket_name).upload(
                file_path,
                file_content
            )
            img_url = response.path

            # Get the public URL for the uploaded image

            # Create Product_Images record
            db_product_image = Product_Images(
                product_id=product_id,
                image_url=img_url,
                is_primary=is_primary  # Set the first image as primary
            )
            session.add(db_product_image)
            session.commit()

        except Exception as e:
            pass
            # Clean up any uploaded images if an error occurs
            supabase.storage.from_(bucket_name).remove(img_url)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading image {product_image.filename}: {str(e)}"
            )
        return img_url


async def db_add_product_images(product_id: uuid.UUID, product_images: list[UploadFile], seller_id: uuid.UUID):
    with session:
        db_get_seller_product(product_id, seller_id, session)
        image_urls = []
        db_product_images = []
        # Upload each image to Supabase Storage
        for index, image in enumerate(product_images):
            # Generate a unique file name
            file_extension = image.filename.split('.')[-1]
            file_name = f"{uuid.uuid4()}.{file_extension}"
            file_path = f"product-images/{product_id}/{file_name}"  # Organize by product ID

            # Read file content
            file_content = await image.read()

            # Upload to Supabase Storage
            try:
                response = supabase.storage.from_(bucket_name).upload(
                    file_path,
                    file_content
                )

                # Get the public URL for the uploaded image
                image_urls.append(response.path)

                # Create Product_Images record
                db_product_images = Product_Images(
                    product_id=product_id,
                    image_url=response.path,
                    is_primary=(index == 0)  # Set the first image as primary
                )

            except Exception as e:
                pass
                # Clean up any uploaded images if an error occurs
                for uploaded_path in image_urls:
                    supabase.storage.from_(bucket_name).remove(uploaded_path)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error uploading image {image.filename}: {str(e)}"
                )

        # Commit the database transaction
        session.add_all(db_product_images)
        session.commit()
        return image_urls


async def db_delete_product_image(id: uuid.UUID, seller_id: uuid.UUID):
    with session:
        db_product_image = session.get(Product_Images, id)
        if not db_product_image or db_product_image.product.seller_id != seller_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        supabase.storage.from_(bucket_name).remove([db_product_image.image_url])

        session.delete(db_product_image)
        session.commit()


async def db_update_product_image(id: uuid.UUID, product_image: UploadFile, seller_id: uuid.UUID):
    with session:
        db_product_image = session.get(Product_Images, id)
        if not db_product_image or db_product_image.product.seller_id != seller_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        file_content = await product_image.read()
        print(db_product_image.image_url)
        response = supabase.storage.from_(bucket_name).update(
            file=file_content,
            path=db_product_image.image_url,
        )
        return response.fullPath


async def db_clear_product_image(id: uuid.UUID, seller_id: uuid.UUID):
    with session:
        db_product = session.get(Products, id)
        if not db_product or db_product.seller_id != seller_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        supabase.storage.from_(bucket_name).remove([str(id)])
        db_product.product_images = None
        session.add(db_product)
        session.commit()
