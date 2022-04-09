import importlib
from datetime import datetime
from sqlalchemy import orm
from qol3.bot.telegram import Message
from qol3.bot.workflow.base import WorkFlow
from qol3.di import get_db


db = get_db()


class ChatContext(db.Model):

    __tablename__ = "bot_chat_contexts"

    id = db.Column("id", db.Integer, primary_key=True, nullable=False)
    context = db.Column("context", db.String, nullable=False)
    telegram_userid = db.Column("telegram_userid", db.String, nullable=False)
    telegram_username = db.Column("telegram_username", db.String, nullable=False)
    chat_id = db.Column("chat_id", db.String, nullable=False)
    handler_builder = db.Column("handler_builder", db.JSON, nullable=False)
    is_active = db.Column("is_active", db.SmallInteger, nullable=False, default=0)
    created_at = db.Column("created_at", db.DateTime, nullable=False)
    updated_at = db.Column("updated_at", db.DateTime, nullable=False)

    @orm.reconstructor
    def _init_on_load(self):
        # Load handler
        mod = importlib.import_module(self.handler_builder["module_path"])
        handler = getattr(mod, self.handler_builder["class_name"])
        self._handler = handler(*self.handler_builder["arguments"])

    def __init__(self, ctx: str, handler: WorkFlow, message: Message):
        self.context = ctx
        self.set_handler(handler)
        self.is_active = 1
        self.telegram_userid = str(message.from_user.id)
        self.telegram_username = str(message.from_user.username)
        self.chat_id = str(message.chat.id)

    def handler(self) -> WorkFlow:
        return self._handler

    def set_handler(self, handler: WorkFlow):
        self._handler = handler

    def handle(self, message: Message):
        self._handler.process(message)

        if self._handler.is_finish():
            self.is_active = 0

    def serialize_handler(self):
        if not self._handler:
            return
        self.handler_builder = self._handler.serialize()


def save(model: ChatContext):
    if not model.created_at:
        model.created_at = datetime.now()

    model.serialize_handler()
    model.updated_at = datetime.now()
    db.session.add(model)
    db.session.commit()


def find_active(message: Message) -> ChatContext:
    return ChatContext.query.filter_by(
        telegram_userid=str(message.from_user.id),
        chat_id=str(message.chat.id),
        is_active=1
    ).first()


def terminate_old_context(message: Message):
    db.session.query(ChatContext).filter(
        ChatContext.telegram_userid == str(message.from_user.id),
        ChatContext.chat_id == str(message.chat.id),
        ChatContext.is_active == 1).delete()
