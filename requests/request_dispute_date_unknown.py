from typing import List
from requests.request_base import RequestBase

# CONST
METHOD_NAME = 'answerInlineQuery'


class RequestDisputeDateUnknown(RequestBase):
    inline_query_id: int
    dispute_id: str

    def __init__(
            self,
            inline_query_id: int,
            dispute_id: str,
    ) -> None:
        super().__init__(METHOD_NAME)
        self.inline_query_id = inline_query_id
        self.dispute_id = dispute_id

    def get_json(self) -> dict:
        return {
            'inline_query_id': self.inline_query_id,
            'is_personal': True,
            'cache_time': 0,
            'results': [
                {
                    'type': 'article',
                    'id': self.dispute_id,
                    'title': 'End dispute with date in future',
                    'input_message_content': {
                        'message_text': 'Couldn''t parse date,\n please add future date as DD.MM.YYYY HH:MM at the end of your dispute'
                    },
                },
            ],
        }
