import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(to, subject, body):
    email_address = os.getenv("GMAIL_ADDRESS")
    email_password = os.getenv("GMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg["From"] = email_address
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

