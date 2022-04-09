import abc
from qol3.user import exist_user
from qol3.i18n import t
from telegram import Message


class CommandHandler(metaclass=abc.ABCMeta):

    def require_authentication(self) -> bool:
        return True

    def execute(self, message: Message):
        if self.require_authentication() and not exist_user(str(message.from_user.id)):
            message.bot.send_message(chat_id=message.chat.id, text=t("bot.authorization_failed"))
            return
        self._process(message)

    @abc.abstractmethod
    def _process(self, message: Message):
        raise NotImplementedError
