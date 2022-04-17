from datetime import datetime
from qol3.di import get_db

db = get_db()

DCVFM = 'dcvfm'


class Fund(db.Model):

    __tablename__ = 'funds'

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    code = db.Column("code", db.String(100), unique=True, nullable=False)
    code_alias = db.Column("code_alias", db.String(255), unique=True, nullable=False)
    name = db.Column("name", db.String(255), unique=True, nullable=False)
    nav_price = db.Column("nav_price", db.Numeric(10, 2), nullable=False)
    group = db.Column("group", db.String(100), nullable=False)
    update_weekday = db.Column("update_weekday", db.String(7), default="0000000")
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")
    updated_at = db.Column("updated_at", db.DateTime)

    def has_updated_today(self) -> bool:
        if not self.updated_at:
            return False
        today = datetime.today()
        return today.year == self.updated_at.year \
            and today.month == self.updated_at.month \
            and today.day == self.updated_at.day

    def is_nav_update_today(self) -> bool:
        today = datetime.today()
        week_day = today.weekday()
        return self.update_weekday[week_day] == "1"


def list_dcfvm(update_today=True):
    query = Fund.query.filter_by(group=DCVFM)
    if update_today:
        today = datetime.today()
        weekday_index = ['_'] * 7
        weekday_index[today.weekday()] = "1"
        query = query.filter(Fund.update_weekday.like("".join(weekday_index)))

    return query.all()


def get_dcvfm_by_code(code: str) -> Fund:
    query = Fund.query \
        .where(Fund.group == DCVFM) \
        .where(Fund.code == code)
    return query.first()
