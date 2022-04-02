from flask import current_app

from qol3.bot.chat_context import ChatContext, terminate_old_context, save
from qol3.bot.message import Message
from qol3.bot.workflow.base import WorkFlow
from qol3.i18n import t
from qol3.user import exist_user
from qol3.user import new_user


class RegisterUser(WorkFlow):

    def __init__(self):
        pass

    def process(self, message: Message):
        if message.is_command():
            message.reply(t("bot.register_command.prompt_passcode"))
            return

        if message.get_content() != current_app.config.get("bot.register_user.passcode"):
            message.reply(t("bot.register_command.error_wrong_passcode"))
            return
        user = new_user(message.sender_id(), message.sender_username())
        self.user_id = user.id
        message.reply(t("bot.register_command.success"))
        pass

    def is_finish(self) -> bool:
        return hasattr(self, "user_id")


def handle(message: Message):
    terminate_old_context(str(message.sender_id()), str(message.chat_id()))

    if exist_user(str(message.sender_id())):
        message.reply(t("bot.register_command.validation_user_existed"))
        return

    workflow = RegisterUser()
    ctx = ChatContext()
    ctx.set_handler(workflow)
    ctx.context = __name__
    ctx.is_active = 1
    ctx.telegram_userid = str(message.sender_id())
    ctx.telegram_username = str(message.sender_username())
    ctx.chat_id = str(message.chat_id())
    ctx.handle(message)
    save(ctx)
    pass
