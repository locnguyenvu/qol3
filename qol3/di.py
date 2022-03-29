from flask import g
from flask_sqlalchemy import SQLAlchemy
from telegram import Bot

def bootstrap(app):
    g.bot = Bot(app.config["TELEGRAM_SECRET"]) 
    g.db = SQLAlchemy(app)

def get_bot():
    return g.bot

def get_db():
    return g.db

