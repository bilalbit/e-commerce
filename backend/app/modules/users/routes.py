from fastapi import APIRouter

from backend.app.database import db_session
from backend.app.dependencies import current_user_dependency
from .services import *

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get('/', response_model=UsersPublic)
def get_user_info(user: current_user_dependency, session_dep: db_session):
    return db_get_user_info(user["id"], session_dep)


@router.patch('/')
def update_user_profile(user_data: UsersUpdate,user:current_user_dependency):
    return db_update_profile(user_data,user["id"])


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_account(user:current_user_dependency):
    return db_delete_account(user["id"])


@router.post('/profile-photo')
async def add_profile_photo(pp_photo: UploadFile, user: current_user_dependency):
    image_urls = await db_add_profile_photo(pp_photo, user["id"])
    return {"message": "Images uploaded successfully", "image_urls": image_urls}


@router.delete("/profile-photo")
async def delete_profile_photo(user: current_user_dependency):
    await db_delete_profile_photo(user["id"])


@router.patch("/profile-photo")
async def update_profile_photo(pp_photo: UploadFile, user: current_user_dependency):
    await db_update_profile_photo(pp_photo, user["id"])
