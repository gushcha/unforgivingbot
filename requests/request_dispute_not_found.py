from requests.request_base import RequestBase
from constants.request_methods import REQUEST_METHOD_ANSWER_CALLBACK_QUERY


class RequestDisputeNotFound(RequestBase):
    callback_query_id: str
    dispute_id: str

    def __init__(self, callback_query_id) -> None:
        self.callback_query_id = callback_query_id
        super().__init__(REQUEST_METHOD_ANSWER_CALLBACK_QUERY)

    def get_json(self) -> dict:
        return {
            'callback_query_id': self.callback_query_id,
            'text': 'Could not subscribe!\n Dispute lost or outdated.\n Please create new one'
        }
