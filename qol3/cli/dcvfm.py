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

    funds = list_dcfvm(update_today=True)
    funds_update_today = list(filter(lambda e: e.has_updated_today(), funds))
    if len(funds) == 0 or len(funds) != len(funds_update_today):
        return

    message_builder = ["DCVFM nav price {}".format(datetime.now().strftime("%Y-%m-%d")), "{:-<26}".format("-")]
    nav_updates_hashmap = dict()
    nav_updates = find_active_by_fund_ids(list(map(lambda f: f.id, funds)))
    for update in nav_updates:
        nav_updates_hashmap[update.fund_code] = str(update)
    for display_order in ["DCBC", "DCDS", "DCIP", "DCBF"]:
        if display_order not in nav_updates_hashmap:
            continue
        message_builder.append(nav_updates_hashmap[display_order])

    subscribers = find_by_topic(TOPIC_DCVFM_NAV_UPDATE)
    for subscriber in subscribers:
        bot.send_message(chat_id=subscriber.telegram_userid, text="\n".join(message_builder))
