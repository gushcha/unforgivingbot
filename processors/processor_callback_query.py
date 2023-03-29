import asyncio
from typing import Dict, Tuple

from helpers.helper_logger import get_logger
from dao.disputes_dao import read as dispute_read, create as dispute_create
from dao.trackers_dao import create as tracker_create, read as trackers_read
from dto.dispute_dto import DisputeDto
from dto.tracker_dto import TrackerDto
from processors.inline_query import InlineQuery
from constants.callback_actions import CALLBACK_ACTION_SUBSCRIBE
from requests.request_dispute_not_found import RequestDisputeNotFound
from requests.request_dispute_subscribe import RequestDisputeSubscribe


class ProcessorCallbackQuery():
    dispute_queries: Dict[str, InlineQuery]

    def __init__(self, dispute_queries: Dict[str, InlineQuery]) -> None:
        self.dispute_queries = dispute_queries

    def _get_dispute_query_user_id(self, dispute_id: str) -> str | None:
        for user_id in self.dispute_queries:
            dispute_query = self.dispute_queries[user_id]
            if dispute_query.dispute is not None and dispute_query.dispute_id == dispute_id:
                return user_id

    def _construct_username(self, from_user: dict) -> str:
        if from_user['username']:
            return f'@{from_user["username"]}'
        elif from_user['first_name'] or from_user['last_name']:
            return f'{from_user["first_name"]} {from_user["last_name"]}'
        else:
            return '+1'

    async def _submit_and_subscribe(
        self,
        inline_message_id: str,
        dispute_query_user_id: str,
        from_user: dict
    ) -> None:
        dispute = self.dispute_queries[dispute_query_user_id].dispute
        user_id = from_user['id']
        username = self._construct_username(from_user)
        tracker = TrackerDto(dispute.id, user_id, username)

        await dispute_create(dispute)
        del self.dispute_queries[dispute_query_user_id]
        await tracker_create(tracker)

        await RequestDisputeSubscribe(
            inline_message_id,
            dispute,
            [username]
        ).send()

    async def _subscribe(
        self,
        inline_message_id: str,
        dispute: DisputeDto,
        from_user: dict
    ) -> None:
        user_id = from_user['id']
        added_username = self._construct_username(from_user)
        usernames = []
        added_tracker = TrackerDto(dispute.id, user_id, added_username)
        trackers = await trackers_read(dispute.id)

        is_already_subscribed = False
        for tracker in trackers:
            if (tracker.chat_id == user_id):
                usernames.append(f'{tracker.username} (already subscribed)')
                is_already_subscribed = True
            else:
                usernames.append(tracker.username)
        if not is_already_subscribed:
            await tracker_create(added_tracker)
            usernames.append(added_username)

        await RequestDisputeSubscribe(
            inline_message_id,
            dispute,
            usernames
        ).send()

    async def _process_task(self, update: dict) -> None:
        callback_action = update['callback_query']['data'][0:1]
        if callback_action != CALLBACK_ACTION_SUBSCRIBE:
            get_logger().error(
                f'Unexpected callback action: {callback_action}')
            return

        dispute_id = update['callback_query']['data'][2:6]
        from_user = update['callback_query']['from']
        inline_message_id = update['callback_query']['inline_message_id']
        dispute_query_user_id = self._get_dispute_query_user_id(dispute_id)
        try:
            if (dispute_query_user_id):
                await self._submit_and_subscribe(inline_message_id, dispute_query_user_id, from_user)
            else:
                dispute = await dispute_read(dispute_id)
                if dispute is None:
                    get_logger().warn(
                        f'Dispute not found in memory or database: {dispute_id}')
                    await RequestDisputeNotFound(update['callback_query']['id']).send()
                    return

                await self._subscribe(inline_message_id, dispute, from_user)
        except Exception as e:
            get_logger().exception(e)


    def process(self, update: dict) -> None:
        asyncio.create_task(self._process_task(update))
