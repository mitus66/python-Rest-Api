# repository/contacts.py
import datetime
from typing import List, Optional

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from database.models import Contact, User
from schemas import ContactCreate, ContactUpdate


from database.models import Contact
from schemas import ContactCreate

def create_contact(body: ContactCreate, user: User, db: Session):
    # Create the Contact object by explicitly passing the fields.
    # This prevents unexpected fields like 'additional_data' from causing a TypeError.
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birthday=body.birthday,
        owner_id=user.id # Set the owner_id to link the contact to the user
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_contacts(user: User, db: Session) -> List[Contact]:
    """
    Retrieves all contacts for a specific user.

    :param user: The authenticated user object.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of Contact objects.
    :rtype: List[Contact]
    """
    return db.query(Contact).filter(Contact.owner_id == user.id).all()


def get_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    """
    Retrieves a single contact by its ID for a specific user.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The authenticated user object.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The Contact object if found, otherwise None.
    :rtype: Optional[Contact]
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.owner_id == user.id)).first()


def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Optional[Contact]:
    """
    Updates a contact for a specific user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param body: The updated data for the contact.
    :type body: ContactUpdate
    :param user: The authenticated user object.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated Contact object if found, otherwise None.
    :rtype: Optional[Contact]
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.owner_id == user.id)).first()
    if contact:
        # Update only the fields that are provided in the body
        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)

        db.commit()
        db.refresh(contact)
    return contact


def remove_contact(contact_id: int, user: User, db: Session) -> Optional[Contact]:
    """
    Removes a contact by its ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :type contact_id: int
    :param user: The authenticated user object.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed Contact object if found, otherwise None.
    :rtype: Optional[Contact]
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.owner_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact