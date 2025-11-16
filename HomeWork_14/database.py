# database.py
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
# Завантажуємо змінні середовища з файлу .env
load_dotenv()

# Використовуємо змінну DATABASE_URL з .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Перевірка на випадок, якщо змінна не була знайдена
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функція-генератор для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()