from qol3.bot.telegram import Message
from .base import CommandHandler


class HelpCommand(CommandHandler):

    def require_authentication(self) -> bool:
        return False

    def _process(self, message: Message):
        message.bot.send_message(chat_id=message.from_user.id, text="Test")
