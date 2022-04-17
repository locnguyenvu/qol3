from datetime import datetime
from qol3.di import get_db

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
    created_at = db.Column("created_at", db.DateTime, server_default="NOW()")

    def __init__(self, fund_id: str, fund_code: str, dealing_date: str, update_date: str, price: float, net_change: float, probation_change: float):
        self.fund_id = fund_id
        self.fund_code = fund_code
        self.dealing_date = dealing_date
        self.update_date = update_date
        self.price = price
        self.net_change = net_change
        self.probation_change = probation_change
        self.created_at = datetime.now()

    def to_telegram_markdown_message(self) -> str:
        decorate_symbol = "📈"
        change_symbol = "+"
        if self.net_change < 0:
            decorate_symbol = "📉"
            change_symbol = "-"

        return f"{decorate_symbol}`{self.fund_code:<6}` `{self.price:>12,}` `({change_symbol}{abs(self.probation_change)})`"


def existed(fund_code: str, dealing_date: str, price: float) -> bool:
    record = FundNavPriceHistory.query \
        .where(FundNavPriceHistory.fund_code == fund_code) \
        .where(FundNavPriceHistory.dealing_date == dealing_date) \
        .where(FundNavPriceHistory.price == price) \
        .first()
    return record is not None


def find_changes_today_by_fund_codes(fund_codes: list) -> list:
    today = datetime.now().replace(hour=0, minute=0, second=0)
    query = FundNavPriceHistory.query.filter(
        FundNavPriceHistory.fund_code.in_(fund_codes),
        FundNavPriceHistory.created_at >= today
    )
    return query.all()
