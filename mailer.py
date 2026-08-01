import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from pathlib import Path

import config


def send_to_kindle(epub_path: Path) -> None:
    missing = [
        name
        for name in ("SMTP_HOST", "SMTP_PORT", "SMTP_FROM", "SMTP_APP_PASSWORD", "KINDLE_TO")
        if not getattr(config, name, None)
    ]
    if missing:
        raise RuntimeError(
            f"config.py is missing values: {', '.join(missing)} — "
            "see config.example.py for where to get them."
        )

    msg = MIMEMultipart()
    msg["From"] = config.SMTP_FROM
    msg["To"] = config.KINDLE_TO
    msg["Subject"] = epub_path.name

    with open(epub_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="epub+zip")
    attachment.add_header("Content-Disposition", "attachment", filename=epub_path.name)
    msg.attach(attachment)

    with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(config.SMTP_FROM, config.SMTP_APP_PASSWORD)
        smtp.send_message(msg)
