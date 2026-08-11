import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from . import config


def send_to_kindle(epub_path: Path) -> None:
    cfg = config.load()

    msg = MIMEMultipart()
    msg["From"] = cfg["smtp_from"]
    msg["To"] = cfg["kindle_to"]
    msg["Subject"] = epub_path.name

    with open(epub_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="epub+zip")
    attachment.add_header("Content-Disposition", "attachment", filename=epub_path.name)
    msg.attach(attachment)

    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as smtp:
        smtp.starttls()
        smtp.login(cfg["smtp_from"], cfg["smtp_app_password"])
        smtp.send_message(msg)
