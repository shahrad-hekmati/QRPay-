import os

from dotenv import load_dotenv

load_dotenv()


class EmailSettings:
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_SERVER_USER = os.getenv('EMAIL_SERVER_USER')
    EMAIL_SERVER_PASSWORD = os.getenv('EMAIL_SERVER_PASSWORD')
    EMAIL_FROM = os.getenv('EMAIL_FROM')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL') == 'True'
