from .command.help import HelpCommand
from .command.register import RegisterCommand
from .command.subscribe import SubscribeCommand
from .command.unsubscribe import UnSubscribeCommand
from .dispatcher import Dispatcher


dispatcher = Dispatcher()
dispatcher.register_command("help", HelpCommand())
dispatcher.register_command("register", RegisterCommand())
dispatcher.register_command("subscribe", SubscribeCommand())
dispatcher.register_command("unsubscribe", UnSubscribeCommand())
