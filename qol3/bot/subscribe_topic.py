from qol3.bot.subscriber import find_by_telegram_userid

TOPIC_DCVFM_NAV_UPDATE = "fund.dcvfm-nav-price-update"
TOPIC_VNINDEX_DAILY_REPORT = "vnindex.daily-report"

AVAILABLE_TOPICS = {
    TOPIC_DCVFM_NAV_UPDATE: {'desc': 'Dragron Captital', 'unicode_logo': '1️⃣', 'selected_value': '1'},
    TOPIC_VNINDEX_DAILY_REPORT: {'desc': 'VNINDEX', 'unicode_logo': '2️⃣', 'selected_value': '2'},
}


def subscribe_instruction(telegram_userid: int) -> str:
    topics = find_by_telegram_userid(telegram_userid)
    message_chunks = [
        "0️⃣ Cancel",
    ]

    for key in AVAILABLE_TOPICS:
        mess = [AVAILABLE_TOPICS[key]['unicode_logo'], AVAILABLE_TOPICS[key]['desc']]
        existed = filter(lambda e: e.topic == key, topics)
        if len(list(existed)) > 0:
            mess.append(' ✅')

        message_chunks.append(" ".join(mess))

    return "\n".join(message_chunks)
