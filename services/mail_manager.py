import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from helper.email_settings import EmailSettings
from utils.purchase_confirmation import generate_purchase_confirmation_token


class MailManager:
    def __init__(self, settings: EmailSettings):
        self.settings = settings
        self.server: Optional[smtplib.SMTP] = None

    def __enter__(self) -> 'MailManager':
        if (
            self.settings.EMAIL_PORT is not None
            and self.settings.EMAIL_HOST is not None
        ):
            self.server = smtplib.SMTP(
                self.settings.EMAIL_HOST,
                self.settings.EMAIL_PORT
            )
            self.server.starttls()
            self.login()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

    def login(self):
        if (
            self.server is not None
            and self.settings.EMAIL_SERVER_USER is not None
        ):
            try:
                self.server.login(
                    self.settings.EMAIL_SERVER_USER,
                    self.settings.EMAIL_SERVER_PASSWORD
                )
            except smtplib.SMTPAuthenticationError as e:
                logging.error(f"SMTP authentication failed: {e}")
                raise

    def send_email_with_template(self,
                                 to_email: str,
                                 subject: str,
                                 html_template_path: str,
                                 user_id: int):
        if (
            self.server is not None
            and self.settings.EMAIL_SERVER_USER is not None
        ):
            with open(html_template_path, 'r') as file:
                html_template = file.read()

            purchase_confirmation_token = generate_purchase_confirmation_token(
                user_id=user_id)

            html_template = html_template.replace(
                "{purchase_confirmation_token}", purchase_confirmation_token)

            msg = MIMEMultipart()
            msg['From'] = self.settings.EMAIL_SERVER_USER
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(html_template, 'html'))

            try:
                self.server.sendmail(
                    self.settings.EMAIL_SERVER_USER,
                    to_email,
                    msg.as_string()
                )
            except smtplib.SMTPException as e:
                logging.error(f"Failed to send email: {e}")
                raise

    def quit(self):
        if self.server is not None:
            try:
                self.server.quit()
            except smtplib.SMTPException as e:
                logging.warning(f"Error while quitting SMTP server: {e}")
