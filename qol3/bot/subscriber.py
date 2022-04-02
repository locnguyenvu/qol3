from datetime import datetime
from qol3.di import get_db

db = get_db()


TOPIC_DCVFM_NAV_UPDATE = "investment.dcvfm-nav-price-update"


class Subscriber(db.Model):

    __tablename__ = "bot_subscribers"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    topic = db.Column(db.String, nullable=False)
    telegram_userid = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime)


def save(model: Subscriber):
    if Subscriber.query.filter_by(topic=model.topic, telegram_userid=model.telegram_userid).first():
        raise ValueError("Duplicate on register")

    if not model.created_at:
        model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()


def delete(model: Subscriber):
    db.session.delete(model)
    db.session.commit()


def find_by_topic(topic: str) -> list:
    return Subscriber.query.filter_by(topic=topic).all()
