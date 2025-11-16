# database/db.py
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

# Створюємо двигун (engine) для підключення до бази даних
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Створюємо клас SessionLocal, який буде фабрикою для сесій
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `Base` є базовим класом для моделей SQLAlchemy, який слугує
# основою для всіх ваших моделей даних.
Base = declarative_base()

# Функція-генератор для отримання сесії бази даних (використовується в FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()