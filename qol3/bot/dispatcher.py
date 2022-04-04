from qol3.di import get_bot
from qol3.bot.telegram import Message
from qol3.bot.chat_context import find_active as find_active_context, save as save_context
from .command.base import CommandHandler

bot = get_bot()


class Dispatcher(object):

    def __init__(self):
        self.commands = dict()
        pass

    def register_command(self, name: str, handler: CommandHandler):
        self.commands[name] = handler

    def dispatch(self, payload: dict):

        if "message" in payload:
            message = Message.de_json(payload["message"], bot)

            if message.is_command() and message.command() in self.commands:
                handler = self.commands[message.command()]
                handler.execute(message)
                return

            ctx = find_active_context(message)
            if ctx:
                ctx.handle(message)
                save_context(ctx)
                return

        pass
