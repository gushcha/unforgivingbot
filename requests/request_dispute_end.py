from typing import List
from constants.request_methods import REQUEST_METHOD_SEND_MESSAGE
from dto.dispute_dto import DisputeDto
from dto.tracker_dto import TrackerDto
from requests.request_base import RequestBase


class RequestDisputeEnd(RequestBase):
    dispute: DisputeDto
    tracker: TrackerDto
    trackers: List[TrackerDto]

    def __init__(
        self,
        dispute: DisputeDto,
        tracker: TrackerDto,
        trackers: List[TrackerDto]
    ) -> None:
        super().__init__(REQUEST_METHOD_SEND_MESSAGE)
        self.dispute = dispute
        self.tracker = tracker
        self.trackers = trackers

    def get_text(self) -> str:
        usernames = map(lambda tracker: tracker.username, self.trackers)
        usernames_printed = '\n'.join(usernames)

        return f'''Dispute {self.dispute.id} finished!

{self.dispute.text}

{usernames_printed}'''

    def get_json(self) -> dict:
        return {
            'chat_id': self.tracker.chat_id,
            'text': self.get_text()
        }
