# Copy this file to config.py and fill in real values.
# config.py is gitignored and must never be committed.

# Gmail's SMTP host; rarely needs to change.
SMTP_HOST = "smtp.gmail.com"

# STARTTLS port for Gmail SMTP; rarely needs to change.
SMTP_PORT = 587

# The Gmail address doc2kindle sends from. Must also be added to your
# Kindle's approved sender list: Amazon -> Manage Your Content and Devices
# -> Preferences -> Personal Document Settings -> Approved Personal
# Document E-mail List.
SMTP_FROM = "you@gmail.com"

# Gmail App Password for SMTP_FROM (not your regular Gmail password).
# Requires 2FA enabled on the account. Generate one at:
# https://myaccount.google.com/apppasswords
SMTP_APP_PASSWORD = ""

# Your Kindle's "Send to Kindle" email address. Find it at:
# Amazon -> Manage Your Content and Devices -> Preferences ->
# Personal Document Settings -> Send-to-Kindle E-Mail Settings.
KINDLE_TO = "your-kindle-address@kindle.com"
