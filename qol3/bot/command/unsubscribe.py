from qol3.bot.chat_context import ChatContext, terminate_old_context, save as ctx_save
from qol3.bot.subscriber import unsubscribe
from qol3.bot.subscribe_topic import AVAILABLE_TOPICS, subscribe_instruction
from qol3.bot.workflow.base import WorkFlow
from qol3.i18n import t
from telegram import Message
from .base import CommandHandler


class UnSubscribe(WorkFlow):

    def __init__(self):
        pass

    def process(self, message: Message):
        
        if message.is_command():
            prompt_message = subscribe_instruction(message.from_user.id)
            message.reply_text(prompt_message)
            return

        try:
            if message.text == '0':
                self.has_finished = True
                return

            for topic in AVAILABLE_TOPICS:
                topic_info = AVAILABLE_TOPICS[topic]
                if topic_info['selected_value'] == message.text:
                    unsubscribe(message.from_user.id, topic)
                    prompt_message = subscribe_instruction(message.from_user.id)
                    message.bot.send_message(chat_id=message.from_user.id, text=prompt_message)
                    return
            
        except ValueError:
            pass

    def is_finish(self) -> bool:
        return hasattr(self, "has_finished")
    pass


class UnSubscribeCommand(CommandHandler):
    def require_authentication(self) -> bool:
        return False

    def _process(self, message: Message):
        terminate_old_context(message)
        workflow = UnSubscribe()
        ctx = ChatContext(__name__, workflow, message)
        ctx.handle(message)
        ctx_save(ctx)
        pass