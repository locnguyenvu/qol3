from flask import current_app
from qol3.bot.chat_context import ChatContext, terminate_old_context, save
from qol3.bot.telegram import Message
from qol3.bot.workflow.base import WorkFlow
from qol3.i18n import t
from qol3.user import exist_user
from qol3.user import new_user
from .base import CommandHandler


class RegisterUser(WorkFlow):

    def __init__(self):
        pass

    def process(self, message: Message):
        if message.is_command():
            message.bot.send_message(chat_id=message.from_user.id, text=t("bot.register_command.prompt_passcode"))
            return

        if message.text != current_app.config.get("bot.register_user.passcode"):
            message.bot.send_message(chat_id=message.from_user.id, text=t("bot.register_command.error_wrong_passcode"))
            return
        user = new_user(message.from_user.id, message.from_user.username)
        self.user_id = user.id
        message.bot.send_message(chat_id=message.from_user.id, text=t("bot.register_command.success"))
        pass

    def is_finish(self) -> bool:
        return hasattr(self, "user_id")


class RegisterCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return False

    def _process(self, message: Message):
        terminate_old_context(message)

        if exist_user(str(message.from_user.id)):
            message.bot.send_message(chat_id=message.chat.id, text=t("bot.register_command.validation_user_existed"))
            return

        workflow = RegisterUser()
        ctx = ChatContext(__name__, workflow, message)
        ctx.handle(message)
        save(ctx)
        pass
