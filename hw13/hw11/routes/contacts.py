from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from hw11.database.db import get_db
from hw11.schemas import ContactModel, ContactResponse
from hw11.repository import contacts as repository_contacts
from hw11.database.models import User
from hw11.services.auth import auth_service

from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/upcoming-birthdays", response_model=List[ContactResponse], description='No more than 5 requests per minute',
            dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.upcoming_birthdays(current_user, db)
    return contacts


@router.get("/", response_model=List[ContactResponse], description='No more than 5 requests per minute',
            dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description='No more than 5 requests per minute',
            dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def find_contact(db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user), first_name: str = None, last_name: str = None, email: str = None):
    contact = await repository_contacts.get_contact(db, current_user, first_name, last_name, email)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, description='No more than 3 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactResponse, description='No more than 3 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse, description='No more than 3 requests per minute',
            dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def remove_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
