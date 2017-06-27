import logging
from warnings import warn
from collections import namedtuple
from functools import wraps
import xml.etree.ElementTree as ET

import aiohttp

from aionationstates import ratelimit
from aionationstates.types import (
    RateLimitError, SessionConflictError, AuthenticationError, NotFound)


# I too am surprised that this doesn't cause an ImportError
from aionationstates import __version__

NS_URL = 'https://www.nationstates.net/'
API_PATH = 'cgi-bin/api.cgi'
API_URL = NS_URL + API_PATH

USER_AGENT = None  # To be set by the user

logger = logging.getLogger('aionationstates')


class ApiQuery:
    def __init__(self, *, session, result, q, params=None):
        self.session = session
        self.results = [result]
        self.q = set(q)
        self.params = params or {}

    def __await__(self):
        return self._wrap().__await__()

    async def _wrap(self):
        self.params['q'] = '+'.join(self.q)
        resp = await self.session._call_api(self.params)
        root = ET.fromstring(resp.text)
        results = [
            await result(self.session, root)
            for result in self.results
        ]
        return results[0] if len(results) == 1 else tuple(results)

    def __add__(self, other):
        if self.session is not other.session:
            raise ValueError('ApiQueries do not share the same session')
        if not len(self.q & other.q) == 0:
            raise ValueError('ApiQueries contain the same query')
        if not len(set(self.params) & set(other.params)) == 0:
            # XXX is this actually necessary?
            raise ValueError('ApiQueries contain conflicting params')

        self.q |= other.q
        self.params.update(other.params)
        self.results += other.results
        return self


def api_query(*q, **params):
    def decorator(func):
        @wraps(func)
        def wrapper(session):
            return ApiQuery(session=session, q=q,
                            params=params, result=func)
        return wrapper
    return decorator


def api_command(c, **data):
    def decorator(func):
        @wraps(func)
        async def wrapper(session):
            data['c'] = c
            resp = await session._call_api_command(data)
            root = ET.fromstring(resp.text)
            return await func(session, root)
        return wrapper
    return decorator


# Needed because aiohttp's API is weird and every my attempt at making
# a proper use of it has led to sadness and despair.
RawResponse = namedtuple('RawResponse', ('status url text'
                                         ' cookies headers'))


class Session:  # TODO self._useragent
    def __init__(self, *args, **kwargs):
        ...

    async def _request(self, method, url, headers=None, **kwargs):
        headers = headers or {}

        standard_user_agent = f'aionationstates/{aionationstates.__version__}'
        if not aionationstates.USER_AGENT:
            warn('Please supply a useragent by setting the'
                 ' aionationstates.USER_AGENT variable.')
            headers['User-Agent'] = standard_user_agent
        headers['User-Agent'] = \
            f'{aionationstates.USER_AGENT} ({standard_user_agent})'

        async with aiohttp.request(method, url, headers=headers,
                                   allow_redirects=False, **kwargs) as resp:
            return RawResponse(
                status=resp.status,
                url=resp.url,
                cookies=resp.cookies,
                headers=resp.headers,
                text=await resp.text()
            )

    @ratelimit.api
    async def _base_call_api(self, method, **kwargs):
        logger.debug(f'Calling API {method} {kwargs}')
        resp = await self._request(method, API_URL, **kwargs)
        if resp.status == 403:
            raise AuthenticationError
        if resp.status == 429:
            raise RateLimitError(
                f'ratelimited for {resp.headers["X-Retry-After"]} seconds')
        if resp.status == 409:
            raise SessionConflictError('previous login too recent')
        if resp.status == 404:
            raise NotFound
        assert resp.status == 200
        return resp

    async def _call_api(self, params, **kwargs):
        return await self._base_call_api('GET', params=params, **kwargs)

    @ratelimit.web
    async def _call_web(self, path, *, method='GET', **kwargs):
        logger.debug(f'Calling web {method} {path} {kwargs}')
        resp = await self._request(method, NS_URL + path.strip('/'), **kwargs)
        if '<html lang="en" id="page_login">' in resp.text:
            raise AuthenticationError
        assert resp.status == 200
        return resp


