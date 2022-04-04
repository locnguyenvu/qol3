import re
from telegram import Message as BaseMessage


class Message(BaseMessage):

    def command(self) -> str:
        chunks = self.text.split(" ")
        return chunks[0].lstrip("/")

    def is_command(self) -> bool:
        return re.match(r"^\/[a-zA-Z0-9]+", self.text) is not None

    pass
