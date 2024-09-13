import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = os.getenv("EMAIL_ADDRESS")
sender_password = os.getenv("EMAIL_PASSWORD")
front_end_url = os.getenv("FRONT_END_URL")


def send_email(receiver_email, email_subject, email_body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_body, 'html'))

    server = smtplib.SMTP(
        os.getenv("EMAIL_SERVICE_PROVIDER_ADDRESS", 'smtp.gmail.com'),
        int(os.getenv("EMAIL_SERVICE_PROVIDER_PORT", 587))
    )
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print(f"Verification email sent to {receiver_email}")


send_email("htaheri550@gmail.com", "Email Subject", "Email Body")