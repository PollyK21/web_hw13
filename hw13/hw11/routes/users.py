from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from hw11.database.db import get_db
from hw11.database.models import User
from hw11.repository import users as repository_users
from hw11.services.auth import auth_service
from hw11.conf.config import settings
from hw11.schemas import UserDb

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    Endpoint to retrieve the current user.

    Parameters:
    - current_user (User): The current user obtained from the access token.

    Returns:
    - UserDb: The current user.
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    Endpoint to update the avatar of the current user.

    Parameters:
    - file (UploadFile): The image file to upload as the avatar.
    - current_user (User): The current user obtained from the access token.
    - db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
    - UserDb: The updated user with the new avatar.
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user
