import asyncio
from os.path import basename, splitext
from qol3.bot.subscriber import find_by_topic
from qol3.bot.subscribe_topic import TOPIC_VNINDEX_DAILY_REPORT
from qol3.di import get_bot
from qol3.vnindex import chromium_crawler

bot = get_bot()


def daily_report():
    result = asyncio.run(chromium_crawler.screenshot_chart())
    file_binary = open(result, 'rb')
    file_name_without_extension = splitext(result)[0]
    subscribers = find_by_topic(TOPIC_VNINDEX_DAILY_REPORT)
    for subscriber in subscribers:
        bot.send_photo(chat_id=subscriber.telegram_userid, photo=file_binary, filename=basename(file_name_without_extension))
