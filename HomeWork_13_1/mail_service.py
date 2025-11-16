# mail_service.py
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from auth import create_email_token
from config import settings
from jinja2 import Environment, FileSystemLoader

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