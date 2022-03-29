from datetime import datetime
from sqlalchemy import or_

from qol3.di import get_db

db = get_db()

class User(db.Model):

    __tablename__ = "users"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    telegram_userid = db.Column("telegram_userid", db.String, nullable=False)
    telegram_username = db.Column("telegram_username", db.String, nullable=False)
    created_at = db.Column("created_at", db.DateTime, nullable=False)
    updated_at = db.Column("updated_at", db.DateTime, nullable=False)



def new_user(telegram_userid:int, telegram_username:str) -> User:
    user = User()
    user.telegram_userid = str(telegram_userid)
    user.telegram_username = telegram_username
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    db.session.add(user)
    db.session.commit()
    return user

def exist_user(user_identity:str) -> bool:
    user = User.query.filter(or_(User.telegram_userid == user_identity, User.telegram_username == user_identity)).first()
    return user != None