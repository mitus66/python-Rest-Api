# crud.py
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from schemas import ContactCreate, ContactUpdate
from database.models import Contact, User as UserModel

def create_contact_for_user(db: Session, body: ContactCreate, user: UserModel):
    # Pass only the fields that exist in the SQLAlchemy model.
    # We use body.model_dump() with exclude={'owner'}
    # The 'owner' field in the schema should not be passed to the model
    db_contact = Contact(**body.model_dump(exclude_unset=True))
    db_contact.owner = user
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_user_contacts(db: Session, user: UserModel, skip: int = 0, limit: int = 100):
    return db.query(Contact).filter(Contact.owner_id == user.id).offset(skip).limit(limit).all()

def get_contact_by_id_for_user(db: Session, contact_id: int, user: UserModel):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()

def update_contact_for_user(db: Session, contact_id: int, user: UserModel, contact_update: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()
    if db_contact:
        for key, value in contact_update.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact_for_user(db: Session, contact_id: int, user: UserModel):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts_for_user(db: Session, query: Optional[str], user: UserModel):
    if query:
        search_pattern = f"%{query}%"
        return db.query(Contact).filter(
            (Contact.owner_id == user.id) &
            ( (Contact.first_name.ilike(search_pattern)) |
              (Contact.last_name.ilike(search_pattern)) |
              (Contact.email.ilike(search_pattern)) )
        ).all()
    return []

def get_upcoming_birthdays_for_user(db: Session, user: UserModel):
    today = date.today()
    upcoming = []
    contacts = db.query(Contact).filter(Contact.owner_id == user.id).all()
    for contact in contacts:
        bday_this_year = contact.birthday.replace(year=today.year)
        if bday_this_year < today:
            bday_this_year = bday_this_year.replace(year=today.year + 1)
        delta = bday_this_year - today
        if 0 <= delta.days <= 7:
            upcoming.append(contact)
    return upcoming