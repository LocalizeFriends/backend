from datetime import datetime
import time
import pytz

_EPOCH = datetime(1970, 1, 1, tzinfo=pytz.utc)

# based on https://stackoverflow.com/a/30021083
def timestamp_ms(dt):
    if dt.tzinfo is None:
        return int((time.mktime((dt.year, dt.month, dt.day,
                                 dt.hour, dt.minute, dt.second,
                                 -1, -1, -1)) + dt.microsecond / 1e6) * 1000)
    else:
        return int((dt - _EPOCH).total_seconds() * 1000)
