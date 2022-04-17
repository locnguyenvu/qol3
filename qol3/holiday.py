from datetime import datetime
from qol3.di import get_db

db = get_db()


class Holiday(db.Model):

    __tablename__ = "holidays"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    name = db.Column("name", db.String(255), nullable=False)
    start_at = db.Column("start_at", db.Date, nullable=False)
    end_at = db.Column("end_at", db.Date, nullable=False)
    created_at = db.Column("created_at", db.DateTime, nullable=False, server_default="NOW()")

    def __init__(self, name: str, start_at: str, end_at: str):
        self.name = name
        self.start_at = start_at
        self.end_at = end_at


def is_today_holiday() -> bool:
    today = datetime.now().strftime("%Y-%m-%d")

    holiday = Holiday.query.filter(Holiday.start_at <= today, Holiday.end_at >= today).first()
    return holiday is not None


def save(model: Holiday):
    model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()
