"""add_vnindex_package

Revision ID: f48b00234ae9
Revises: 9456b00cb6bb
Create Date: 2022-04-08 21:05:29.405974

"""
from alembic import op
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = 'f48b00234ae9'
down_revision = '9456b00cb6bb'
branch_labels = None
depends_on = None

config_table = table(
    'configs',
    column('path', sa.String),
    column('value', sa.String),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
)


def upgrade():
    op.bulk_insert(config_table, [
        {
            "path": "vnindex.image_crawler.screenshot_webpage_url",
            "value": "",
            "updated_at": datetime.now(),
            "created_at": datetime.now(),
        }
    ])
    pass


def downgrade():
    op.execute(
        config_table.delete().where(config_table.c.path == "vnindex.image_crawler.screenshot_webpage_url")
    )
    pass
