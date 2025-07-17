import time
import schedule
from email_fetcher import open_mail_connection, fetch_emails
from email_processor import process_email

def job():
    mail = open_mail_connection()
    emails = fetch_emails(mail)

    for email_data in emails:
        try:
            process_email(email_data["body"], email_data["from"], email_data["subject"])
            # Marcar como leído
            mail.store(email_data["email_id"], '+FLAGS', '\\Seen')
        except Exception as e:
            print(f"Error procesando email: {e}")

    mail.logout()

schedule.every(60).seconds.do(job)

print("Iniciando el asistente de emails...")
while True:
    schedule.run_pending()
    time.sleep(1)

