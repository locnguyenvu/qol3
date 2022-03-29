from flask import current_app

from qol3.bot.message import Message
from qol3.i18n import t
from qol3.user import new_user
from .base import WorkFlow


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