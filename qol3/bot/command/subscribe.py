from qol3.bot.chat_context import ChatContext, terminate_old_context, save as ctx_save
from qol3.bot.telegram import Message
from qol3.bot.subscriber import Subscriber, save, TOPIC_DCVFM_NAV_UPDATE
from qol3.bot.workflow.base import WorkFlow
from qol3.i18n import t
from .base import CommandHandler


prompt_message = """
{title}
1️⃣ {dcvfm_desc}
"""


class Subscribe(WorkFlow):

    def __init__(self):
        pass

    def process(self, message: Message):
        if message.is_command():
            message.bot.send_message(chat_id=message.chat.id, text=prompt_message.format(
                title=t("bot.subscribe_command.prompt_title"),
                dcvfm_desc="Dragon Capital")
            )
            return

        try:
            if message.text == '1':
                subscriber = Subscriber()
                subscriber.telegram_userid = str(message.from_user.id)
                subscriber.topic = TOPIC_DCVFM_NAV_UPDATE
                save(subscriber)
                self.has_finished = True
                message.bot.send_message(chat_id=message.chat.id, text=t("bot.subscribe_command.success"))
        except ValueError:
            pass

    def is_finish(self) -> bool:
        return hasattr(self, "has_finished")
    pass


class SubscribeCommand(CommandHandler):

    def _process(self, message: Message):
        terminate_old_context(message)
        workflow = Subscribe()
        ctx = ChatContext(__name__, workflow, message)
        ctx.handle(message)
        ctx_save(ctx)
        pass
