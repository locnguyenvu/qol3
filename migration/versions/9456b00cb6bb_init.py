"""init

Revision ID: 9456b00cb6bb
Revises:
Create Date: 2022-03-29 09:19:46.905464

"""
from alembic import op
from datetime import datetime
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9456b00cb6bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    tbl_config = op.create_table(
        "configs",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("value", sa.Text, nullable=False, default=''),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )
    op.create_index('idx_config_path', 'configs', ['path'])
    op.create_unique_constraint('unique_configs_path', 'configs', ['path'])
    op.bulk_insert(tbl_config, [
        {
            "path": "fund.dcvfm.crawler.base_url_ajax",
            "value": "",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "path": "bot.register_user.passcode",
            "value": "",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

    ])

    tbl_fund = op.create_table(
        "funds",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("code", sa.String(100), unique=True, nullable=False),
        sa.Column("code_alias", sa.String(255), unique=True, nullable=False),
        sa.Column("name", sa.String(255), unique=True, nullable=False),
        sa.Column("nav_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("group", sa.String(100), nullable=False),
        sa.Column("update_weekday", sa.String(7), default="0000000"),
        sa.Column("created_at", sa.DateTime, server_default="NOW()"),
        sa.Column("updated_at", sa.DateTime),
    )
    op.create_index('idx_fund_code', 'funds', ['code'])
    op.bulk_insert(tbl_fund, [
        {"code": "VFMVF1", "code_alias": "DCDS", "name": "QUỸ ĐẦU TƯ CHỨNG KHOÁN VIỆT NAM (VFMVF1) | VIETNAM SECURITIES INVESTMENT FUND", "nav_price": 0.00, "group": "dcvfm", "update_weekday": "1111100", "created_at": datetime.now()},
        {"code": "VFMVF4", "code_alias": "DCBC", "name": "QUỸ ĐẦU TƯ DOANH NGHIỆP HÀNG ĐẦU VIỆT NAM (VFMVF4) | VIETNAM BLUE-CHIP FUND", "nav_price": 0.00, "group": "dcvfm", "update_weekday": "1111100", "created_at": datetime.now()},
        {"code": "VFMVFB", "code_alias": "DCBF", "name": "QUỸ ĐẦU TƯ TRÁI PHIẾU VIỆT NAM (VFMVFB) | VIETNAM BOND FUND", "nav_price": 0.00, "group": "dcvfm", "update_weekday": "0000100", "created_at": datetime.now()},
        {"code": "DCIP", "code_alias": "DCIP", "name": "QUỸ ĐẦU TƯ ĐỊNH HƯỚNG BẢO TOÀN VỐN VIỆT NAM | VIETNAM CAPITAL PROTECTION ORIENTED FUND", "nav_price": 0.00, "group": "dcvfm", "update_weekday": "1111100", "created_at": datetime.now()},
    ])

    op.create_table(
        "fund_nav_price_histories",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("fund_id", sa.Integer, nullable=False),
        sa.Column("fund_code", sa.String, nullable=False),
        sa.Column("update_date", sa.Date, nullable=False),
        sa.Column("dealing_date", sa.Date, nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("net_change", sa.Numeric(10, 2), nullable=False),
        sa.Column("probation_change", sa.Numeric(10, 2), nullable=False),
        sa.Column("is_active", sa.Integer, default=0),
        sa.Column("created_at", sa.DateTime, server_default="NOW()")
    )
    op.create_index("idx_fund_nav_price_history_dealing_date", "fund_nav_price_histories", ["dealing_date"])

    op.create_table(
        "bot_subscribers",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("topic", sa.String, nullable=False),
        sa.Column("telegram_userid", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "bot_chat_contexts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("context", sa.String, nullable=False),
        sa.Column("telegram_userid", sa.String, nullable=False),
        sa.Column("telegram_username", sa.String, nullable=False),
        sa.Column("chat_id", sa.String, nullable=False),
        sa.Column("handler_builder", sa.JSON, nullable=False),
        sa.Column("is_active", sa.SmallInteger, nullable=False, default="0"),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("telegram_userid", sa.String, nullable=False),
        sa.Column("telegram_username", sa.String, nullable=False),
        sa.Column("created_at", sa.DateTime, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=False),
    )
    pass


def downgrade():
    op.drop_table("configs")
    op.drop_table("funds")
    op.drop_table("fund_nav_price_histories")
    op.drop_table("bot_subscribers")
    op.drop_table("bot_chat_contexts")
    op.drop_table("users")
    pass
