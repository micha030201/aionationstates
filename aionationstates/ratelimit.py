"""Compliance with NationStates' API and web rate limits."""

import asyncio
import logging
from functools import partial
from contextlib import suppress


logger = logging.getLogger('aionationstates')


async def _ratelimit_queue_consumer(queue, clean_every):
    while True:
        await queue.get()
        # A bit of wiggle room for network delays and such.
        await asyncio.sleep(clean_every + clean_every / 20)
        if queue.qsize() == queue.maxsize:
            logger.info(
                'clearing saturated request buffer'
                f' of length {queue.maxsize + 1}')
        else:
            logger.debug(
                f'clearing request buffer of length {queue.maxsize + 1}'
                f' containing {queue.qsize() + 1} items')
        with suppress(asyncio.QueueEmpty):
            while True:
                queue.get_nowait()


def _create_ratelimiter(requests_allowed, per):
    # We have to make queues one item shorter than the number of allowed
    # requests because the consumers consume an extra item while
    # waiting for it to be added to the queue.
    queue = asyncio.Queue(maxsize=requests_allowed - 1)
    asyncio.get_event_loop().create_task(_ratelimit_queue_consumer(queue, per))
    return partial(queue.put, None)


# "API Rate Limit: 50 requests per 30 seconds."
# https://www.nationstates.net/pages/api.html#ratelimits
api = _create_ratelimiter(requests_allowed=50, per=30)

# "Scripts must send no more than 10 requests per minute."
# https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966
web = _create_ratelimiter(requests_allowed=10, per=60)
