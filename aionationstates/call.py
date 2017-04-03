import re
import logging
from contextlib import suppress
from collections import namedtuple

import aiohttp

from aionationstates import ratelimit
from aionationstates.utils import normalize


logger = logging.getLogger('aionationstates')

NS_URL = 'https://www.nationstates.net/'
API_PATH = 'cgi-bin/api.cgi'
API_URL = NS_URL + API_PATH

USER_AGENT = 'https://github.com/micha030201/aionationstates'


class AuthenticationError(Exception):
    """Raised when NationStates doesn't accept provided credentials."""

# A namedtuple to store HTTP responses.

# Needed because aiohttp's API is weird and every my attempt at making
# a proper use of it has led to sadness and despair.
RawResponse = namedtuple('RawResponse', ('status url text'
                                         ' cookies headers history'))


async def _request(self, method, url, headers=None, **kwargs):
    headers = headers or {}
    headers['User-Agent'] = USER_AGENT
    async with aiohttp.request(method, url, headers=headers, **kwargs) as resp:
        return RawResponse(
            status=resp.status,
            url=resp.url,
            cookies=resp.cookies,
            headers=resp.headers,
            history=resp.history,
            text=await resp.text()
        )

@ratelimit.api
async def call_api(self, **kwargs):
    resp = await self._request('GET', API_URL,
                               allow_redirects=False, **kwargs)
    if resp.status == 403:
        raise AuthenticationError
    return resp

@ratelimit.web
async def call_web(self, path, method='GET', **kwargs):
    resp = await self._request(method, NS_URL + path.strip('/'), **kwargs)
    if '<html lang="en" id="page_login">' in resp.text:
        raise AuthenticationError
    return resp



