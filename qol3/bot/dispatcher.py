from typing import Callable

from qol3.i18n import t
from qol3.di import get_bot
from qol3.user import exist_user
from qol3.bot.message import Message
from qol3.bot.chat_context import find_active as find_active_context, save as save_context

bot = get_bot()

class Dispatcher(object):

    def __init__(self):
        self.commands = dict()
        pass

    def register_command(self, name:str, handler:Callable, require_auth=True):
        self.commands[name] = dict(handler=handler, require_auth=require_auth)

    def dispatch(self, payload:dict):

        if "message" in payload:
            message = Message(payload)

            if message.is_command() and message.get_command() in self.commands:
                cmd = self.commands[message.get_command()]
                if cmd["require_auth"] and not exist_user(str(message.sender_id())):
                    bot.send_message(chat_id=message.chat_id(), text=t("bot.authorization_failed"))
                    return
                handler = cmd["handler"]
                handler(message)
                return
            
        ctx = find_active_context(str(message.sender_id()), str(message.chat_id()))
        if ctx:
            ctx.handle(message)
            save_context(ctx)
            return 

        pass