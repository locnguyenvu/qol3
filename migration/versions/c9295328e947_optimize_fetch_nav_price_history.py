"""optimize_fetch_nav_price_history

Revision ID: c9295328e947
Revises: e6addebfe9d3
Create Date: 2022-04-16 14:05:32.104123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9295328e947'
down_revision = 'e6addebfe9d3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("idx_fund_nav_price_history_created_at", "fund_nav_price_histories", ["created_at"])
    op.drop_column("fund_nav_price_histories", "is_active")
    pass


def downgrade():
    op.drop_index("idx_fund_nav_price_history_created_at", "fund_nav_price_histories")
    op.add_column("fund_nav_price_histories", sa.Column("is_active", sa.Integer, default=0))
    pass
