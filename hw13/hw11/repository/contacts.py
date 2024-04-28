from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from hw11.database.models import Contact, User
from hw11.schemas import ContactModel
from datetime import date, timedelta


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


async def get_contact(db: Session, user: User, first_name: str = None, last_name: str = None, email: str = None) -> Contact:
    query = db.query(Contact)
    if first_name:
        query = query.filter(and_(Contact.first_name.ilike(
            f"%{first_name}%"), Contact.user_id == user.id))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.first()


async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name,
                      email=body.email, phone=body.phone, birthday=body.birthday, user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def upcoming_birthdays(user: User, db: Session) -> List[Contact]:
    today = date.today()
    end_date = today + timedelta(days=7)

    return db.query(Contact).filter(
        and_(
            Contact.user_id == user.id,
            Contact.birthday >= today,
            Contact.birthday <= end_date
        )
    ).all()
