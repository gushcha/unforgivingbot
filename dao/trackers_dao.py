from typing import List

from helpers.helper_db import get_cursor, commit
from dto.tracker_dto import TrackerDto

# CONST
MAX_NUMBER_OF_TRACKERS = 1000


async def create(tracker: TrackerDto) -> None:
    cursor = get_cursor()
    await cursor.execute('''insert into trackers \
        (dispute_id, chat_id, username) \
        values (%s, %s, %s);''', (
        tracker.dispute_id,
        tracker.chat_id,
        tracker.username)
    )
    await commit()
    await cursor.close()


async def read(dispute_id: str) -> List[TrackerDto]:
    cursor = get_cursor()
    await cursor.execute('''select dispute_id, chat_id, username \
        from trackers where dispute_id=%s''', (dispute_id,))
    query_result = await cursor.fetchmany(MAX_NUMBER_OF_TRACKERS)
    if not query_result:
        return []
    trackers: List[TrackerDto] = []
    for row in query_result:
        (dispute_id, chat_id, username,) = row
        trackers.append(TrackerDto(dispute_id, chat_id, username))
    await cursor.close()

    return trackers
