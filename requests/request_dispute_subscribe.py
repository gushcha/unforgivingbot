from typing import List

from constants.request_methods import REQUEST_METHOD_EDIT_MESSAGE_TEXT
from dto.dispute_dto import DisputeDto
from requests.keyboards.keyboard_subscribe import keyboard_subscribe
from requests.request_base import RequestBase


class RequestDisputeSubscribe(RequestBase):
    inline_message_id: int
    dispute: DisputeDto
    usernames: List[str]

    def __init__(
            self,
            inline_message_id: int,
            dispute: DisputeDto,
            usernames: List[str],
    ) -> None:
        super().__init__(REQUEST_METHOD_EDIT_MESSAGE_TEXT)
        self.inline_message_id = inline_message_id
        self.dispute = dispute
        self.usernames = usernames

    def get_message_text(self) -> str:
        usernames_printed = '\n'.join(self.usernames)

        return f'''Dispute {self.dispute.id}

{self.dispute.text}

Reminder set on {self.dispute.ends_on.strftime("%d %b %Y %H:%M")}

{usernames_printed}'''

    def get_reply_markup(self) -> dict:
        return {
            'inline_keyboard': keyboard_subscribe(self.dispute.id)
        }

    def get_json(self) -> dict:
        return {
            'inline_message_id': self.inline_message_id,
            'text': self.get_message_text(),
            'reply_markup': self.get_reply_markup(),
        }
