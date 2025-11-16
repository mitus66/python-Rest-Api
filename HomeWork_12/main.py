from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, Base, get_db
from models import Contact
from schemas import Contact as ContactSchema, ContactCreate, ContactUpdate
import crud

app = FastAPI(
    title="Contacts API",
    description="REST API для зберігання та управління контактами з FastAPI та SQLAlchemy.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

@app.post("/contacts/", response_model=ContactSchema)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_email(db, email=contact.email)
    if db_contact:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=List[ContactSchema])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = Query(None, min_length=1, description="Search by first name, last name, or email"),
    db: Session = Depends(get_db)
):
    if query:
        contacts = crud.search_contacts(db, query)
    else:
        contacts = crud.get_contacts(db, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=ContactSchema)
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=ContactSchema)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/birthdays/", response_model=List[ContactSchema])
def upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = crud.get_upcoming_birthdays(db)
    return contacts