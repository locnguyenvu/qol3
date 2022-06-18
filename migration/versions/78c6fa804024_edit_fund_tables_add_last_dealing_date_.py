"""edit_fund_tables_add_last_dealing_date_column

Revision ID: 78c6fa804024
Revises: c9295328e947
Create Date: 2022-06-18 14:24:53.630607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78c6fa804024'
down_revision = 'c9295328e947'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("funds", sa.Column("last_dealing_date", sa.Date))
    pass


def downgrade():
    op.drop_column("funds", "last_dealing_date")
    pass
