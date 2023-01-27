import asyncio
import telegram
from os.path import basename, splitext
from qol3.holiday import is_today_holiday
from qol3.bot.subscriber import find_by_topic
from qol3.bot.subscribe_topic import TOPIC_VNINDEX_DAILY_REPORT
from qol3.di import get_bot
from qol3.vnindex import msn_crawler

bot = get_bot()


def end_session_chart():
    if is_today_holiday():
        return
    result = asyncio.run(msn_crawler.screenshot_chart())
    file_binary = open(result, 'rb')
    file_name_without_extension = splitext(result)[0]
    subscribers = find_by_topic(TOPIC_VNINDEX_DAILY_REPORT)
    for subscriber in subscribers:
        bot.send_photo(chat_id=subscriber.telegram_userid, photo=file_binary, filename=basename(file_name_without_extension))


def end_session_summary():
    if is_today_holiday():
        return
    summary = asyncio.run(msn_crawler.summary_on_end_session())
    if summary.changes_fix < 0:
        message = f"""
VNINDEX: _{summary.post_str()}_
[{summary.change_sign()}]({summary.reference_link}) {summary.changes_fix_str()} \\(_{summary.changes_percent_str()}%_\\)
            """
    else:
        message = f"""
VNINDEX: *{summary.post_str()}*
[{summary.change_sign()}]({summary.reference_link}) {summary.changes_fix_str()} \\(_{summary.changes_percent_str()}%_\\)
            """
    subscribers = find_by_topic(TOPIC_VNINDEX_DAILY_REPORT)
    for subscriber in subscribers:
        asyncio.run(bot.send_message(chat_id=subscriber.telegram_userid,
                         text=message,
                         parse_mode=telegram.constants.ParseMode.MARKDOWN_V2,
                         disable_web_page_preview=True))
