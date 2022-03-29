from qol3.di import get_db

db = get_db()

class FundNavPriceHistory(db.Model):

    __tablename__ = "fund_nav_price_histories"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False),
    fund_id = db.Column("fund_id", db.Integer, nullable=False),
    fund_code = db.Column("fund_code", db.String, nullable=False),
    update_date = db.Column("update_date", db.Date, nullable=False),
    dealing_date = db.Column("dealing_date", db.Date, nullable=False),
    price = db.Column("price", db.Numeric(10, 2), nullable=False),
    net_change = db.Column("net_change", db.Numeric(10, 2), nullable=False),
    probation_change = db.Column("probation_change", db.Numeric(10, 2), nullable=False),
    is_active = db.Column("is_active", db.Integer, default=0),
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")