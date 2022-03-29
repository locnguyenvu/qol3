import qol3.bot.chat_context
from qol3.i18n import t
from qol3.bot.message import Message
from qol3.bot.workflow.register_user import RegisterUser as RegisterUserWorkFlow
from qol3.user import exist_user

def handle(message: Message):
    qol3.bot.chat_context.terminate_old_context(str(message.sender_id()), str(message.chat_id()))

    if exist_user(str(message.sender_id())):
        message.reply(t("bot.register_command.validation_user_existed"))
        return

    workflow = RegisterUserWorkFlow()
    ctx = qol3.bot.chat_context.ChatContext()
    ctx.set_handler(workflow)
    ctx.context = __name__
    ctx.is_active = 1
    ctx.telegram_userid = str(message.sender_id())
    ctx.telegram_username = str(message.sender_username())
    ctx.chat_id = str(message.chat_id())
    ctx.handle(message)
    qol3.bot.chat_context.save(ctx)
    pass