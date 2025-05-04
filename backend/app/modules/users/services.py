from fastapi import HTTPException, status, UploadFile
from sqlmodel import select, Session

from backend.app.core.config import get_settings
from backend.app.core.utils import hash_password
from backend.app.database import session, supabase
from .models import *

bucket_name = get_settings().bucket_name  # Your Supabase bucket name must be from.env


def db_get_user_by_phone(phone_number: str):
    with session:
        return session.query(Users).where(Users.phone_number == phone_number).first()


def db_get_user_info(user_id: uuid.UUID, db_session: Session):
    db_user = db_session.get(Users, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


def db_update_profile(user_data: UsersUpdate, user_id: uuid.UUID):
    with session:
        extra_data = {}
        if user_data.password is not None:
            extra_data = {"password_hash": hash_password(user_data.password)}
        db_user = db_get_user_info(user_id)
        updated_user = user_data.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(updated_user, update=extra_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def db_delete_account():
    with session:
        db_user = db_get_user_info(session)
        session.delete(db_user)
        session.commit()


async def db_add_profile_photo(photo: UploadFile, user_id: uuid.UUID):
    with session:
        db_user_image = session.exec(
            select(User_Images).where(User_Images.user_id == user_id)
        ).first()
        if db_user_image:
            return await db_update_profile_photo(photo, user_id)
        pp_photo = await photo.read()
        file_extension = photo.filename.split('.')[-1]
        file_name = f"{user_id}.{file_extension}"
        file_path = f"user-profile-image/{file_name}"
        try:
            response = (
                supabase.storage
                .from_(bucket_name)
                .upload(
                    file=pp_photo,
                    path=file_path
                )
            )
            print(response)
            img_url = response.path
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error uploading image {photo.filename}: {str(e)}"
            )
        db_user_image = User_Images(img_url=response.path, user_id=user_id)
        session.add(db_user_image)
        session.commit()
        return img_url


async def db_delete_profile_photo(user_id: uuid.UUID):
    with session:
        db_user_image = session.exec(
            select(User_Images).where(User_Images.user_id == user_id)
        ).first()
        if db_user_image:
            print("db_user_image")
            print(db_user_image)
            try:
                (
                    supabase.storage
                    .from_(bucket_name)
                    .remove(
                        [str(db_user_image.img_url)]
                    )
                )


            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error removing image: {str(e)}"
                )
            session.delete(db_user_image)
            session.commit()
            return None
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )


async def db_update_profile_photo(photo: UploadFile, user_id: uuid.UUID):
    with session:
        db_user_image = session.exec(
            select(User_Images).where(User_Images.user_id == user_id)
        ).first()
        if db_user_image:
            f = await photo.read()
            file_extension = photo.filename.split('.')[-1]
            file_name = f"{user_id}.{file_extension}"
            file_path = f"user-profile-image/{file_name}"
            try:
                (
                    supabase.storage
                    .from_(bucket_name)
                    .update(
                        file=f,
                        path=file_path,
                        file_options={"cache-control": "3600", "upsert": "true"}
                    )
                )


            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error updating image: {str(e)}"
                )
            return None
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
