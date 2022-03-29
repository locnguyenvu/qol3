import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    DEBUG = False if os.getenv("FLASK_ENV") == "production" else False

    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    TELEGRAM_SECRET = os.getenv("TELEGRAM_SECRET")
    TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET")
