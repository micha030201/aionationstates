import re
from datetime import datetime


def normalize(identifier):
    identifier = identifier.lower().replace(' ', '_')
    if not re.match('^[a-z0-9_-]+$', identifier):
        raise ValueError(f'provided identifier {identifier} contains invalid'
                         ' characters.')
    return identifier


def banner_url(id):
    return f'https://www.nationstates.net/images/banners/{id}.jpg'


def timestamp(line):
    return datetime.utcfromtimestamp(int(line))


def datetime_to_ns(then: datetime) -> str:
    """Transform a ``datetime`` object into a NationStates-style
    string, for example "6 days ago", "105 minutes ago", etc.
    """
    if then == datetime(1970, 1, 1, 0, 0):
        return 'Antiquity'

    now = datetime.utcnow()
    delta = now - then
    seconds = delta.total_seconds()

    # There's gotta be a better way to do this...
    years,   seconds = divmod(seconds, 60*60*24*365)
    days,    seconds = divmod(seconds, 60*60*24)
    hours,   seconds = divmod(seconds, 60*60)
    minutes, seconds = divmod(seconds, 60)
    years   = int(years)
    days    = int(days)
    hours   = int(hours)
    minutes = int(minutes)
    seconds = round(seconds)

    if years > 1:
        if days > 1:
            return f'{years} years {days} days ago'
        elif days == 1:
            return '{years} years 1 day ago'
        return '{years} years ago'
    if years == 1:
        if days > 1:
            return f'1 year {days} days ago'
        elif days == 1:
            return '1 year 1 day ago'
        return '1 year ago'

    if days > 3:
        return f'{days} days ago'
    if days > 1:
        if hours > 1:
            return f'{days} days {hours} hours ago'
        elif hours == 1:
            return f'{days} days 1 hour ago'
        return f'{days} days ago'
    if days == 1:
        if hours > 1:
            return f'1 day {hours} hours ago'
        elif hours == 1:
            return '1 day 1 hour ago'
        return '1 day ago'

    if hours > 1:
        return f'{hours} hours ago'
    if hours == 1:
        return f'{minutes + 60} minutes ago'

    if minutes > 1:
        return f'{minutes} minutes ago'
    if minutes == 1:
        return '1 minute ago'

    return 'Seconds ago'

