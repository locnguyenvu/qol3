"""add_package_holiday

Revision ID: e6addebfe9d3
Revises: f48b00234ae9
Create Date: 2022-04-16 09:24:09.996255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6addebfe9d3'
down_revision = 'f48b00234ae9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "holidays",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("start_at", sa.Date, nullable=False),
        sa.Column("end_at", sa.Date, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default="NOW()")
    )
    op.create_index("idx_holidays_start_to_end", "holidays", ["start_at", "end_at"])
    pass


def downgrade():
    op.drop_table("holidays")
    pass
