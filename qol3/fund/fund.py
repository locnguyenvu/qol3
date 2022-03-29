from qol3.di import get_db

db = get_db()

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