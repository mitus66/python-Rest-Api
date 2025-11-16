# from sqlalchemy import Column, Integer, String, Date
# from database import Base
#
# class Contact(Base):
#     __tablename__ = "contacts"
#
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String, index=True)
#     last_name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     phone_number = Column(String)
#     birthday = Column(Date)
#     additional_data = Column(String, nullable=True)

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    contacts = relationship("Contact", back_populates="owner")

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts")
