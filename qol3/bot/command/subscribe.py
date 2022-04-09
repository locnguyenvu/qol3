from qol3.bot.chat_context import ChatContext, terminate_old_context, save as ctx_save
from qol3.bot.message import Message
from qol3.bot.subscriber import Subscriber, save, TOPIC_DCVFM_NAV_UPDATE, TOPIC_VNINDEX_DAILY_REPORT
from qol3.bot.workflow.base import WorkFlow
from qol3.i18n import t


prompt_message = """
{title}
0️⃣ {cancel}
1️⃣ {dcvfm_desc}
2️⃣ {vnindex_desc}
"""


class Subscribe(WorkFlow):

    def __init__(self):
        pass

    def process(self, message: Message):
        if message.is_command():
            message.reply(prompt_message.format(
                title=t("bot.subscribe_command.prompt_title"),
                cancel="Cancel",
                dcvfm_desc="Dragon Capital",
                vnindex_desc="VNINDEX")
            )
            return

        try:
            if message.text == '0':
                self.has_finished = True
                return
            if message.text == '1':
                subscriber = Subscriber()
                subscriber.telegram_userid = str(message.sender_id())
                subscriber.topic = TOPIC_DCVFM_NAV_UPDATE
                save(subscriber)
                message.reply(t("bot.subscribe_command.success"))
            if message.text == '2':
                subscriber = Subscriber()
                subscriber.telegram_userid = str(message.sender_id())
                subscriber.topic = TOPIC_VNINDEX_DAILY_REPORT
                save(subscriber)
                message.reply(t("bot.subscribe_command.success"))
        except ValueError:
            pass

    def is_finish(self) -> bool:
        return hasattr(self, "has_finished")
    pass


def handle(message: Message):
    terminate_old_context(str(message.sender_id()), str(message.chat_id()))

    workflow = Subscribe()
    ctx = ChatContext()
    ctx.set_handler(workflow)
    ctx.context = __name__
    ctx.is_active = 1
    ctx.telegram_userid = str(message.sender_id())
    ctx.telegram_username = str(message.sender_username())
    ctx.chat_id = str(message.chat_id())
    ctx.handle(message)
    ctx_save(ctx)
    pass
