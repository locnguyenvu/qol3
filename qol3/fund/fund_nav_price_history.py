from datetime import datetime

from qol3.di import get_db
from qol3.fund.fund import Fund

db = get_db()

class FundNavPriceHistory(db.Model):

    __tablename__ = "fund_nav_price_histories"

    id = db.Column("id", db.Integer, primary_key=True)
    fund_id = db.Column("fund_id", db.Integer, nullable=False)
    fund_code = db.Column("fund_code", db.String, nullable=False)
    update_date = db.Column("update_date", db.Date, nullable=False)
    dealing_date = db.Column("dealing_date", db.Date, nullable=False)
    price = db.Column("price", db.Numeric(10, 2), nullable=False)
    net_change = db.Column("net_change", db.Numeric(10, 2), nullable=False)
    probation_change = db.Column("probation_change", db.Numeric(10, 2), nullable=False)
    is_active = db.Column("is_active", db.Integer, default=0)
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")

    def __init__(self, fund_id:str, fund_code:str):
        self.fund_id = fund_id
        self.fund_code = fund_code

    def __str__(self) -> str:
        change_symbol = "▴"
        if self.net_change < 0:
            change_symbol = "▿"
        
        return "{:<6} {:>7,} ({}{}%)".format(str(self.fund_code).upper(), self.price, change_symbol, abs(self.probation_change))

def save(model:FundNavPriceHistory):
    if not model.created_at:
        model.created_at = datetime.now()
    db.session.add(model)
    db.session.commit()

def existed(model:FundNavPriceHistory) -> bool:
    existed = FundNavPriceHistory.query \
            .where(FundNavPriceHistory.fund_id == model.fund_id) \
            .where(FundNavPriceHistory.fund_code == model.fund_code) \
            .where(FundNavPriceHistory.dealing_date == model.dealing_date) \
            .where(FundNavPriceHistory.price == model.price) \
            .first()
    return existed != None

def mark_active(navPrice:FundNavPriceHistory):
    FundNavPriceHistory.query.filter_by(fund_id=navPrice.fund_id, is_active=1).update({"is_active": 0})
    Fund.query.filter_by(id=navPrice.fund_id).update({"nav_price": navPrice.price, "updated_at": datetime.now()})
    navPrice.is_active = 1
    save(navPrice)

def find_active_by_fund_ids(fund_ids: list) -> list:
    query = FundNavPriceHistory.query.filter_by(is_active=1).filter(FundNavPriceHistory.fund_id.in_(fund_ids))
    return query.all()
