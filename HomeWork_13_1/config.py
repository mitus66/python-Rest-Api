# config.py
from pydantic import EmailStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str # У вас в .env немає цього, але Cloudinary його потребує
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:8000"
    DATABASE_URL: str
    MAIL_USERNAME: EmailStr  # Зазвичай це EmailStr, а не просто str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str

    class Config:
        env_file = ".env"
        extra = "ignore"

# Інстанціюємо клас, щоб змінні завантажилися
settings = Settings()