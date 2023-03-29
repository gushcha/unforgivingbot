
from constants.request_methods import REQUEST_METHOD_SEND_MESSAGE
from requests.request_base import RequestBase


class RequestAbout(RequestBase):
    chat_id: int

    def __init__(self, chat_id: int) -> None:
        super().__init__(REQUEST_METHOD_SEND_MESSAGE)
        self.chat_id = chat_id

    def get_text(self) -> str:
        return f'''Thank you for choosing {self.config.bot_name}!

Currently only notification show up in this chat.

You may use this bot in any chat with your friends,
just type following:

@{self.config.bot_name} The matter of dispute with date formatted DD.MM.YYYY HH:MM

Feel free to contribute at https://github.com/gushcha/unforgivingbot
'''

    def get_json(self) -> dict:
        return {
            'chat_id': self.chat_id,
            'text': self.get_text()
        }
