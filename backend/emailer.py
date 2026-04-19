import smtplib
import os
from email.mime.text import MIMEText

def send_email(to, subject, body):
    host = os.getenv("SMTP_HOST", "smtp.office365.com")
    port = int(os.getenv("SMTP_PORT", 587))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")

    msg = MIMEText(body)
    msg["From"] = user
    msg["To"] = to
    msg["Subject"] = subject

    try:
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", e)
