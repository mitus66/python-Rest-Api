# connect.py
import os
from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()  # Це завантажить змінні з .env

# ... інші налаштування

MONGO_URI = os.getenv("MONGO_URI")
connect(host=MONGO_URI)

