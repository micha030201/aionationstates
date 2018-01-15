"""Compliance with NationStates' API and web rate limits."""

import asyncio
from collections import deque
from operator import methodcaller

from aionationstates.utils import logger


class DelayedEvent(asyncio.Event):
    def set_after(self, delay):
        self._loop.call_later(delay, self.set)



def _create_ratelimiter(requests, per):
    _first_event = asyncio.Event()
    _first_event.set()

    request_events = deque([_first_event], maxlen=requests)
    portion_duration = per * 1.05  # some wiggle room

    def decorator(func):
        async def wrapper(*args, **kwargs):
            while True:
                first_known_event = request_events[0]

                if not first_known_event.is_set():
                    logger.debug(f'waiting {args} {kwargs}')
                    # Ensure we never launch a timer on any but the
                    # oldest request in a given portion.
                    # request_events.clear()
                    # request_events.append(first_known_event)

                    await first_known_event.wait()
                else:
                    logger.debug(f'calling {args} {kwargs}')
                    event = DelayedEvent()
                    request_events.append(event)
                    resp = await func(*args, **kwargs)
                    event.set_after(portion_duration)
                    return resp
        return wrapper
    return decorator


# "API Rate Limit: 50 requests per 30 seconds."
# https://www.nationstates.net/pages/api.html#ratelimits
api = _create_ratelimiter(requests=50, per=30)

# "Scripts must send no more than 10 requests per minute."
# https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966
web = _create_ratelimiter(requests=10, per=60)
