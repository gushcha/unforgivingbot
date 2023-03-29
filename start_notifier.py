import asyncio
import sched
import time

from helpers.helper_config import read_config, get_config, Config
from helpers.helper_db import connect_notifier, disconnect
from datetime import datetime, timedelta
from typing import List
from dao.trackers_dao import read as trackers_read
from dao.disputes_dao import read_interval as disputes_read_interval, delete as disputes_delete
from dto.dispute_dto import DisputeDto
from requests.request_dispute_end import RequestDisputeEnd
from helpers.helper_logger import get_logger


async def get_disputes_for_run(config: Config) -> List[DisputeDto]:
    await connect_notifier()
    day_start = datetime.combine(datetime.utcnow().date(), datetime.min.time())
    now = datetime.now()
    day_start_now_timedelta = now - day_start
    seconds_gap = day_start_now_timedelta.seconds % config.notifier_runtime_delta
    ends_on_start = now - \
        timedelta(seconds=seconds_gap) - \
        timedelta(microseconds=now.microsecond)
    ends_on_end = ends_on_start + \
        timedelta(seconds=config.notifier_runtime_delta)
    disputes = await disputes_read_interval(ends_on_end)
    return disputes


async def notify(dispute: DisputeDto) -> None:
    trackers = await trackers_read(dispute.id)
    requestDisputeEndList = map(lambda tracker: RequestDisputeEnd(
        dispute, tracker, trackers), trackers)

    pendingRequestsList = map(
        lambda requestDisputeEnd: requestDisputeEnd.send(),
        requestDisputeEndList
    )

    await asyncio.gather(*pendingRequestsList)
    await disputes_delete(dispute.id)


def blocking_notify(dispute: DisputeDto) -> None:
    asyncio.run(notify(dispute))


if __name__ == '__main__':
    disputes: List[DisputeDto] = []
    read_config()
    get_logger().info('Started notifier')
    config = get_config()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        disputes = asyncio.run(get_disputes_for_run(config))
    except KeyboardInterrupt:
        asyncio.run(disconnect())

    s = sched.scheduler(time.time, time.sleep)
    for dispute in disputes:
        get_logger().debug(
            f'Dispute will be notified in this notifier run {dispute}')
        s.enterabs(float(dispute.ends_on.strftime('%s')),
                   10, blocking_notify, argument=(dispute,))
    s.run()
    asyncio.run(disconnect())
