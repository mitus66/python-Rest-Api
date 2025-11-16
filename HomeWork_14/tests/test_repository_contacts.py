# tests/test_repository_contacts.py

import datetime
from repository.contacts import create_contact, get_contacts, get_contact, update_contact, remove_contact
from schemas import ContactCreate, ContactUpdate
from database.models import User, Contact  # <-- Add this line

# tests/test_repository_contacts.py

import datetime
from datetime import date  # <-- Add this line
from repository.contacts import create_contact, get_contacts, get_contact, update_contact, remove_contact
from schemas import ContactCreate, ContactUpdate
from database.models import User, Contact

import datetime
from datetime import date # <-- Add this line
from repository.contacts import create_contact, get_contacts, get_contact, update_contact, remove_contact
from schemas import ContactCreate, ContactUpdate
from database.models import User, Contact

import datetime
from datetime import date
from repository.contacts import create_contact, get_contacts, get_contact, update_contact, remove_contact
from schemas import ContactCreate, ContactUpdate
from database.models import User, Contact


def create_user_and_contact_in_db(session):
    """
    Helper function to create a user and a contact for testing.
    """
    user = User(username="test_user", email="test@example.com", password="password", created_at=datetime.datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)

    # Now that the user exists and has an ID, create the contact
    contact_data = {
        "first_name": "Test",
        "last_name": "Contact",
        "email": "test_contact@example.com",
        "phone_number": "1234567890",
        "birthday": date(1990, 1, 1)
    }
    # Pass the owner_id directly
    contact = Contact(**contact_data, owner_id=user.id)
    session.add(contact)
    session.commit()
    session.refresh(contact)

    return user, contact


def test_create_contact(session):
    user = User(username="test_user", email="test@example.com", password="password", created_at=datetime.datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)

    body = ContactCreate(first_name="John", last_name="Doe", email="john@example.com", phone_number="1234567890",
                         birthday=datetime.date(1990, 1, 1))

    result = create_contact(body=body, user=user, db=session)

    assert result.first_name == body.first_name
    assert result.email == body.email
    assert hasattr(result, "id")


def test_get_contacts(session):
    user, contact = create_user_and_contact_in_db(session)

    result = get_contacts(user=user, db=session)

    assert len(result) == 1
    # Change the assertion to 'Test' to match the created contact
    assert result[0].first_name == "Test"


def test_get_contact_found(session):
    user, contact = create_user_and_contact_in_db(session)

    result = get_contact(contact_id=contact.id, user=user, db=session)

    assert result is not None
    assert result.id == contact.id


def test_get_contact_not_found(session):
    user, _ = create_user_and_contact_in_db(session)

    result = get_contact(contact_id=999, user=user, db=session)

    assert result is None


def test_update_contact_found(session):
    user, contact = create_user_and_contact_in_db(session)

    updated_data = ContactUpdate(first_name="Jane", last_name="Doe", phone_number="0987654321")

    result = update_contact(contact_id=contact.id, body=updated_data, user=user, db=session)

    assert result is not None
    assert result.first_name == "Jane"
    assert result.phone_number == "0987654321"


def test_update_contact_not_found(session):
    user, _ = create_user_and_contact_in_db(session)

    updated_data = ContactUpdate(first_name="Jane")

    result = update_contact(contact_id=999, body=updated_data, user=user, db=session)

    assert result is None


def test_remove_contact_found(session):
    user, contact = create_user_and_contact_in_db(session)

    result = remove_contact(contact_id=contact.id, user=user, db=session)

    assert result is not None
    assert result.id == contact.id

    # Перевіряємо, що контакт дійсно видалено з бази даних
    deleted_contact = session.query(Contact).filter_by(id=contact.id).first()
    assert deleted_contact is None


def test_remove_contact_not_found(session):
    user, _ = create_user_and_contact_in_db(session)

    result = remove_contact(contact_id=999, user=user, db=session)

    assert result is None