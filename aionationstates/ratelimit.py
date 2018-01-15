"""Compliance with NationStates' API and web rate limits."""

# This is not the algorithm NationStates uses for ratelimiting; rather
# it's the best compromise between usability and developer sanity.

import asyncio


class DelayedEvent(asyncio.Event):
    def set_after(self, delay):
        self._loop.call_later(delay, self.set)


class EventBuffer:
    def __init__(self, maxlen):
        self.lock = asyncio.Lock()
        self.event_futures = set()
        for _ in range(maxlen):
            event = DelayedEvent()
            event.set()
            event_future = asyncio.ensure_future(event.wait())
            self.event_futures.add(event_future)

    async def wait_oldest_get_new(self):
        async with self.lock:
            done, _ = await asyncio.wait(
                self.event_futures,
                return_when=asyncio.FIRST_COMPLETED
            )
            self.event_futures.remove(done.pop())

        event = DelayedEvent()
        event_future = asyncio.ensure_future(event.wait())
        self.event_futures.add(event_future)
        return event


def _create_ratelimiter(requests, per):
    buffer = EventBuffer(requests)
    portion_duration = per

    def decorator(func):
        async def wrapper(*args, **kwargs):
            event = await buffer.wait_oldest_get_new()
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
