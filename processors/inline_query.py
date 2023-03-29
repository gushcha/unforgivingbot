from string import ascii_letters, digits
from random import choices
import asyncio
from requests.request_base import RequestBase
from requests.request_dispute_date_unknown import RequestDisputeDateUnknown
from requests.request_dispute_proposal import RequestDisputeProposal
from dto.dispute_dto import DisputeDto

from helpers.helper_parse_query_text import parse_date

# CONST
DEBOUNCE_TIMEOUT = 0.5

alphabet = ascii_letters + digits


def getId():
    return ''.join(choices(alphabet, k=4))


class InlineQuery():
    dispute_id: str

    def __init__(self, inline_query) -> None:
        self.dispute_id = getId()
        self._react_to_query(inline_query)
        self.dispute: DisputeDto

    def update_inline_query(self, inline_query,) -> None:
        if self.pendingResponse is not None:
            self.pendingResponse.cancel()
        self._react_to_query(inline_query)

    def _react_to_query(self, inline_query) -> None:
        self.inline_query = inline_query

        ends_on = parse_date(inline_query['query'])

        if ends_on is None:
            self.dispute = None
            return self._respond_date_unknown()

        self.dispute = DisputeDto(
            self.dispute_id,
            self.inline_query['query'],
            ends_on
        )
        self._respond_with_date()

    def _respond_date_unknown(self) -> None:
        request_dispute_date_unknown = RequestDisputeDateUnknown(
            self.inline_query['id'],
            self.dispute_id,
        )
        self.pendingResponse = asyncio.create_task(
            self._respond_debounced(request_dispute_date_unknown))

    def _respond_with_date(self) -> None:
        request_dispute_proposal = RequestDisputeProposal(
            self.inline_query['id'],
            self.dispute_id,
            self.inline_query['query'],
            self.dispute.ends_on,
        )

        self.pendingResponse = asyncio.create_task(
            self._respond_debounced(request_dispute_proposal))

    async def _respond_debounced(self, request: RequestBase) -> None:
        await asyncio.sleep(DEBOUNCE_TIMEOUT)
        self.pendingResponse = None
        await request.send()
