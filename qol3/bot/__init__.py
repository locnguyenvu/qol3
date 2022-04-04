from .command.help import HelpCommand
from .command.register_user import RegisterUserCommand
from .command.subscribe import SubscribeCommand
from .dispatcher import Dispatcher


dispatcher = Dispatcher()
dispatcher.register_command("help", HelpCommand())
dispatcher.register_command("register", RegisterUserCommand())
dispatcher.register_command("subscribe", SubscribeCommand())
