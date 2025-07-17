import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GMAIL_ADDRESS")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

def fetch_emails(mail):
    mail.select("inbox")
    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()

    fetched = []
    for eid in email_ids:
        res, msg = mail.fetch(eid, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg_obj = email.message_from_bytes(response[1])
                subject, encoding = decode_header(msg_obj["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                from_ = msg_obj.get("From")

                body = ""
                if msg_obj.is_multipart():
                    for part in msg_obj.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg_obj.get_payload(decode=True).decode(errors="ignore")

                fetched.append({
                    "email_id": eid,
                    "mail_obj": mail,
                    "from": from_,
                    "subject": subject,
                    "body": body
                })
    return fetched

def open_mail_connection():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    return mail

