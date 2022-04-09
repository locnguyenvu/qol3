import asyncio
import time
from datetime import datetime

from qol3.bot.subscriber import find_by_topic
from qol3.bot.subscribe_topic import TOPIC_DCVFM_NAV_UPDATE
from qol3.di import get_bot
from qol3.fund.dcvfm.crawler import nav_today as nav_today_
from qol3.fund.fund import list_dcfvm
from qol3.fund.fund_nav_price_history import find_active_by_fund_ids

bot = get_bot()


def nav_today():
    s = time.perf_counter()
    updates = asyncio.run(nav_today_())
    elapsed = time.perf_counter() - s
    print(f"Execute in {elapsed:0.2f} second")
    if len(list(filter(lambda e: e is not None, updates))) == 0:
        return
    dcvfm_funds = list_dcfvm(update_today=True)
    dcvfm_update_today = list(filter(lambda e: e.has_updated_today(), dcvfm_funds))
    if len(dcvfm_funds) == 0 or len(dcvfm_funds) != len(dcvfm_update_today):
        return
    nav_updates = find_active_by_fund_ids(list(map(lambda e: e.id, dcvfm_funds)))

    changes = list(map(lambda e: str(e), nav_updates))
    cur_date = datetime.now()
    message = ["DCVFM nav price {}".format(cur_date.strftime("%Y-%m-%d")), "{:-<26}".format("-")] + changes

    subscribers = find_by_topic(TOPIC_DCVFM_NAV_UPDATE)
    for subscriber in subscribers:
        bot.send_message(chat_id=subscriber.telegram_userid, text="\n".join(message))
