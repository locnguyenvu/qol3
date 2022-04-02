from .command import help as help_
from .command import register_user
from .command import subscribe
from .dispatcher import Dispatcher


dispatcher = Dispatcher()
dispatcher.register_command("help", help_.handle, require_auth=False)
dispatcher.register_command("register", register_user.handle, require_auth=False)
dispatcher.register_command("subscribe", subscribe.handle, require_auth=True)
