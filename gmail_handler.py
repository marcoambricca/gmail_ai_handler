import imaplib
import email
from email.header import decode_header
import time
import schedule
import os
from dotenv import load_dotenv

load_dotenv()

# Your email credentials
EMAIL = os.getenv("GMAIL_ADDRESS") 
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")  # Use an app-specific password if using Gmail
IMAP_SERVER = "imap.gmail.com"  # Change if you're using a different provider

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def fetch_emails():
    print("Checking for new emails...")

    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select("inbox")

        # Search for unseen emails (you can change the criteria)
        status, messages = mail.search(None, '(UNSEEN)')  # or 'ALL' for all emails
        email_ids = messages[0].split()

        print(f"Found {len(email_ids)} new email(s).")

        for i in email_ids:
            res, msg = mail.fetch(i, "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # Parse email
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    print(f"From: {from_}")
                    print(f"Subject: {subject}")

        mail.logout()

    except Exception as e:
        print(f"Error: {e}")

# Run fetch_emails every 60 seconds
schedule.every(60).seconds.do(fetch_emails)

print("Starting email fetcher...")
while True:
    schedule.run_pending()
    time.sleep(1)

