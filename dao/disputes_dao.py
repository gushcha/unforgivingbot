from typing import List

from helpers.helper_db import commit, get_cursor
from dto.dispute_dto import DisputeDto
from datetime import datetime, timezone, timedelta

# CONST
MAX_NUMBER_OF_DISPUTES = 1000


async def create(dispute: DisputeDto) -> None:
    cursor = get_cursor()
    await cursor.execute('''insert into disputes \
        (id, text, created_on, ends_on) \
        values (%s, %s, %s, %s);''', (
        dispute.id,
        dispute.text,
        dispute.created_on,
        dispute.ends_on,)
    )
    await commit()
    await cursor.close()


async def read(dispute_id: int) -> DisputeDto | None:
    cursor = get_cursor()
    await cursor.execute('''select id, text, created_on, ends_on \
        from disputes where id=%s''', (dispute_id,))
    query_result = await cursor.fetchone()
    await cursor.close()

    if query_result is None:
        return None
    (id, text, created_on, ends_on) = query_result
    return DisputeDto(id, text, ends_on, created_on)


async def read_interval(ends_on_end: datetime) -> List[DisputeDto]:
    cursor = get_cursor()
    await cursor.execute('''select id, text, created_on, ends_on \
        from disputes where ends_on < %s''', (ends_on_end,))
    query_result = await cursor.fetchmany(MAX_NUMBER_OF_DISPUTES)

    disputes: List[disputes] = []

    for row in query_result or []:
        (id, text, created_on, ends_on) = row
        disputes.append(DisputeDto(id, text, ends_on, created_on))

    await cursor.close()

    return disputes


async def delete(dispute_id: str) -> None:
    cursor = get_cursor()
    await cursor.execute('''DELETE FROM disputes WHERE id=%s''', (dispute_id,))
    await commit()
    await cursor.close()
