from typing import Dict

from processors.inline_query import InlineQuery


class ProcessorInlineQuery():
    dispute_queries: Dict[str, InlineQuery]

    def __init__(self, dispute_queries: Dict[str, InlineQuery]) -> None:
        self.dispute_queries = dispute_queries

    def process(self, update: dict) -> None:
        user_id = update['inline_query']['from']['id']
        dispute_query = self.dispute_queries.get(user_id)
        if dispute_query is None:
            self.dispute_queries[user_id] = InlineQuery(
                update['inline_query']
            )
        else:
            dispute_query.update_inline_query(update['inline_query'])
