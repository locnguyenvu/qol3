from .dispatcher import Dispatcher
from .command import help as help_, register_user

dispatcher = Dispatcher()

dispatcher.register_command("help", help_.handle, require_auth=False)
dispatcher.register_command("register", register_user.handle, require_auth=False)