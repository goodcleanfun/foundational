from datetime import date, datetime

from dateutil.parser import parse as _dateutil_parse
from dateutil.parser import parserinfo


def current_timestamp():
    return datetime.utcnow().timestamp()


def current_year():
    return date.today().year


parse_datetime = _dateutil_parse


def parse_date(dt):
    return _dateutil_parse(dt).date()


def parse_datetime_ignore_tz_microseconds(d):
    return _dateutil_parse(d, ignoretz=True)


def parse_datetime_ignore_tz_seconds(d):
    return _dateutil_parse(d, ignoretz=True).replace(microsecond=0)
