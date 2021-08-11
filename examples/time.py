from datetime import datetime, timedelta
from typing import Optional, Union

import dateutil.parser
import dateutil.tz


def isoformat(date: datetime, timespec: str = "auto") -> Optional[str]:
    """Format date as ISO8601.

    Replace default "+00:00" UTC timezone format with "Z"
    """
    if date is None:
        return None
    return date.isoformat(timespec=timespec).replace("+00:00", "Z")


def isoparse(date_str: Union[bytes, str]) -> datetime:
    """Parse ISO8601 date.

    If no timezone is specified, UTC is assumed."""
    parsed = dateutil.parser.isoparse(date_str)
    if parsed.tzinfo is None:
        # default to UTC if not specified
        parsed = parsed.replace(tzinfo=dateutil.tz.UTC)
    return parsed


def parse_milliseconds(ms: int) -> datetime:
    """Convert a millisecond epoch timestamp to datetime.

    Arguments
    ---------
    ms:
        millisecond epoch timestamp

    Returns
    -------
    datetime object in UTC timezone
    """
    # datetime.fromtimestamp doesn't handle negative values
    return datetime.fromtimestamp(0, dateutil.tz.UTC) + timedelta(milliseconds=ms)
