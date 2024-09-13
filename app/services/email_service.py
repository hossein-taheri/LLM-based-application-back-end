import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = os.getenv("EMAIL_ADDRESS")
sender_password = os.getenv("EMAIL_PASSWORD")

front_end_url = os.getenv("FRONT_END_URL")


def read_template(template_name, replacements):
    content = open("app/templates/" + template_name, "rb").read().decode("utf-8")
    for replacement_key in replacements:
        content = content.replace(replacement_key, replacements[replacement_key])
    return content


def send_email(receiver_email, email_subject, email_body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = email_subject

    msg.attach(MIMEText(email_body, 'html'))

    # try:
    server = smtplib.SMTP(
        os.getenv("EMAIL_SERVICE_PROVIDER_ADDRESS", 'smtp.gmail.com'),
        int(os.getenv("EMAIL_SERVICE_PROVIDER_PORT", 587))
    )
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print(f"Verification email sent to {receiver_email}")
    # except Exception as e:
    #     print(f"Failed to send email. Error: {e}")


def send_verification_email(user_email, verification_token):
    verification_link = front_end_url + "/#/auth/verify-email/?verification_token=" + verification_token
    email_body = read_template("verify-email.html", {
        "<verification_link>": verification_link
    })

    send_email(
        user_email,
        "Email Verification",
        email_body
    )


def send_forgot_password(user_email, forgot_password_token):
    reset_link = front_end_url + "/#/auth/set-new-password/?forgot_password_token=" + str(forgot_password_token)
    email_body = read_template("forgot-password.html", {
        "<reset_link>": reset_link
    })

    send_email(
        user_email,
        "Forgot Password",
        email_body
    )
