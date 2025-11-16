# mail_service.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from auth import create_email_token # <-- Цей імпорт залишаємо
from config import settings

# Правильне місце для імпорту.
# Функція create_email_token тепер буде доступна всьому модулю mail_service.py
from auth import create_email_token

def send_verification_email(user, url):
    # Тепер цей імпорт не потрібен, оскільки він уже зроблений зверху
    # from auth import create_email_token

    try:
        token = create_email_token({"sub": user.email})
        # ... інший код для надсилання листа ...
    except Exception as e:
        print(f"Помилка при створенні токена або відправці листа: {e}")

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

env = Environment(loader=FileSystemLoader('templates'))

async def send_email_verification(email: EmailStr, username: str, host: str):
    try:
        token_verification = create_email_token({"sub": email})
        template = env.get_template('email_verification.html')
        html = template.render({"username": username, "host": host, "token": token_verification})

        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            body=html,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        print(e)