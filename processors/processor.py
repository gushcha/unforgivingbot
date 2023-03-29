from json import dumps
import asyncio
from typing import Dict
from helpers.helper_logger import get_logger
from processors.inline_query import InlineQuery
from processors.processor_callback_query import ProcessorCallbackQuery
from processors.processor_inline_query import ProcessorInlineQuery
from requests.request_about import RequestAbout


class Processor():
    dispute_queries: Dict[str, InlineQuery]

    def __init__(self) -> None:
        self.dispute_queries = {}
        self.processor_inline_query = ProcessorInlineQuery(
            self.dispute_queries)
        self.processor_callback_query = ProcessorCallbackQuery(
            self.dispute_queries)

    def __filterSameInlineQueries(self, updates: list):
        appearedFromIds = []
        filteredUpdates = []
        for update in reversed(updates):
            if ('inline_query' not in update):
                filteredUpdates.append(update)
            if (('inline_query' in update)
                    and (update['inline_query']['from']['id'] not in appearedFromIds)):
                appearedFromIds.append(update['inline_query']['from']['id'])
                filteredUpdates.append(update)
        return filteredUpdates

    def process(self, updates: list, offset: int) -> int:
        last_processed_update_id = offset
        filteredUpdates = self.__filterSameInlineQueries(updates)
        for update in filteredUpdates:
            get_logger().debug(f'Update from tg received: {dumps(update)}')
            if 'inline_query' in update:
                self.processor_inline_query.process(update)
            elif 'callback_query' in update:
                self.processor_callback_query.process(update)
            else:
                if (('message' in update) and ('text' in update['message']) and 'chat' in update['message']):
                    asyncio.create_task(RequestAbout(
                        update['message']['chat']['id']).send())
                else:
                    get_logger().info(
                        f'Update from tg was not processed: {dumps(update)}')
            if last_processed_update_id < update['update_id']:
                last_processed_update_id = update['update_id']
        return last_processed_update_id
