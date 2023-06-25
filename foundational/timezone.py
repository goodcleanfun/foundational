from datetime import datetime

import pendulum
from pytz import timezone

US_EASTERN = timezone("US/Eastern").zone
US_CENTRAL = timezone("US/Central").zone
US_MOUNTAIN = timezone("US/Mountain").zone
US_PACIFIC = timezone("US/Pacific").zone
UTC = timezone("UTC").zone


def local_datetime_utc(*args, **kwargs):
    dt = pendulum(*args, **kwargs)
    return datetime.utcfromtimestamp(dt.timestamp())
