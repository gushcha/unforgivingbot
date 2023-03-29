from datetime import datetime
from typing import List
from constants.request_methods import REQUEST_METHOD_ANSWER_INLINE_QUERY
from requests.keyboards.keyboard_subscribe import keyboard_subscribe
from requests.request_base import RequestBase


class RequestDisputeProposal(RequestBase):
    inline_query_id: int
    dispute_id: str
    dispute_text: str
    dispute_ends_on: datetime

    def __init__(
            self,
            inline_query_id: int,
            dispute_id: str,
            dispute_text: str,
            dispute_ends_on: datetime
    ) -> None:
        super().__init__(REQUEST_METHOD_ANSWER_INLINE_QUERY)
        self.inline_query_id = inline_query_id
        self.dispute_id = dispute_id
        self.dispute_text = dispute_text
        self.dispute_ends_on = dispute_ends_on

    def get_title(self) -> str:
        return f'Submit dispute ending on {self.dispute_ends_on.strftime("%d %b %Y %H:%M")}'

    def get_message_text(self) -> str:
        return f'''Dispute {self.dispute_id}
        
{self.dispute_text}

Reminder set on {self.dispute_ends_on.strftime("%d %b %Y %H:%M")}'''

    def get_reply_markup(self) -> dict:
        return {
            'inline_keyboard': keyboard_subscribe(self.dispute_id)
        }

    def get_json(self) -> dict:
        return {
            'inline_query_id': self.inline_query_id,
            'is_personal': True,
            'cache_time': 0,
            'results': [
                {
                    'type': 'article',
                    'id': self.dispute_id,
                    'title': self.get_title(),
                    'reply_markup': self.get_reply_markup(),
                    'input_message_content': {
                        'message_text': self.get_message_text(),
                    },
                },
            ],
        }
