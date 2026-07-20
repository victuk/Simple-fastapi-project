from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig,  FastMail, MessageSchema, MessageType, NameEmail
from os import getenv
from pydantic import BaseModel, EmailStr
from typing import cast

load_dotenv()

config = ConnectionConfig(
    MAIL_USERNAME=cast(str, getenv("EMAIL_USER", "default@username.com")),
    MAIL_PASSWORD=cast(str, getenv("EMAIL_PASS", "default_password")),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM=cast(str, getenv("EMAIL_USER", "default@user.com")),
    MAIL_SSL_TLS=True,
    MAIL_STARTTLS=False
)

class EmailSchema(BaseModel):
    email: list[EmailStr]
    subject: str
    body: str

async def send_email(emailDetails: dict):
    email_service = FastMail(config)
    
    message = MessageSchema(
        subject=emailDetails["subject"],
        recipients=emailDetails["email"],
        body=emailDetails["body"],
        subtype=MessageType.plain
    )
    
    await email_service.send_message(message)
    return "Email sent successfully"
