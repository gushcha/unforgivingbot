from re import search
from datetime import datetime, timezone

# CONST
REMIND_HOUR = 10
REMIND_MINUTE = 0
date_time_reg = '([0-3]?\d)[\.\- ]((?:[0]\d)|10|11|12)[\.\-]?(?:(?:20)?([2-9]\d))?(?:(?:\s+|\s+[^\d\W]{0,5}\s+)(0?\d|1\d|2[0-4])[\.:\- ]([0-5]\d))?\s*'


def parse_date(text: str, timezone: timezone = timezone.utc) -> None | datetime:
    dateStringsMatch = search(date_time_reg, text)
    date_now = datetime.now().astimezone(timezone)

    if dateStringsMatch is None:
        return None

    day = int(dateStringsMatch.group(1))
    month = int(dateStringsMatch.group(2))
    if dateStringsMatch.group(3) is None:
        year = date_now.year
    else:
        year = int(f'20{dateStringsMatch.group(3)}')
    hour = int(dateStringsMatch.group(4) or REMIND_HOUR)
    minute = int(dateStringsMatch.group(5) or REMIND_MINUTE)

    try:
        specified_date = datetime(
            year,
            month,
            day,
            hour,
            minute,
            tzinfo=timezone
        )
    except:
        return None

    if specified_date <= date_now:
        return None

    return specified_date
