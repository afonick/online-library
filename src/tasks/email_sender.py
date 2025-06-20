import smtplib
from pathlib import Path

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from fastapi import HTTPException

from src.core.config import settings


def send_email(subject: str, body: str, recipient: str, attachment_path: str | None = None):
    if settings.EMAIL_BACKEND == "smtp":
        sender_email = settings.SENDER_EMAIL
        sender_password = settings.SENDER_PASSWORD
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT_SSL if settings.USE_SSL else settings.SMTP_PORT_TLS

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Добавление вложения, если указано
        if attachment_path:
            try:
                with open(attachment_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=Path(attachment_path).name)
                    part["Content-Disposition"] = f'attachment; filename="{Path(attachment_path).name}"'
                    message.attach(part)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Ошибка при добавлении вложения: {e}")

        try:
            if settings.USE_SSL:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, message.as_string())
            else:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, message.as_string())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка отправки письма: {e}")

    elif settings.EMAIL_BACKEND == "console":
        print(f"=== Email to {recipient} ===")
        print(f"Subject: {subject}")
        print(f"Message: {body}")
        if attachment_path:
            print(f"Attachment: {attachment_path}")
        print("=============================")
