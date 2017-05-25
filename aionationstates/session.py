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

class ExternalCallersError(Exception):
    """Indicates that an external entity on the system is interfering with
    our requests.
    """

class RateLimitError(ExternalCallersError):
    pass

class SessionConflictError(ExternalCallersError):
    pass


class AuthenticationError(Exception):
    pass


class SuddenlyNationstates(Exception):  # TODO: move to another submodule?
    pass


# Needed because aiohttp's API is weird and every my attempt at making
# a proper use of it has led to sadness and despair.
RawResponse = namedtuple('RawResponse', ('status url text'
                                         ' cookies headers'))

#from aionationstates.nation import Nation, NationControl
#from aionationstates.region import Region
#from aionationstates.world import World

#class Api:
#    def __init__(self, useragent)
#        self.useragent = useragent + '/aionationstates0.0.0'
#
#    async def get_nation(self, nationname):
#        return Nation(nationname)
#
#    async def get_region(self, regionname):
#        return Region(regionname)
#    
#    ...


class Session:
    async def _request(self, method, url, headers=None, **kwargs):
        headers = headers or {}
        headers['User-Agent'] = USER_AGENT
        print(kwargs)
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
    async def call_api(self, params, *, method='GET', **kwargs):
        resp = await self._request(method, API_URL, params=params, **kwargs)
        if resp.status == 403:
            raise AuthenticationError
        if resp.status == 429:
            raise RateLimitError(
                f'ratelimited for {resp.headers["X-Retry-After"]} seconds')
        if resp.status == 409:
            raise SessionConflictError('previous login too recent')
        if resp.status != 200:
            raise SuddenlyNationstates(f'unexpected status code: {resp.status}')  # TODO 404 handling
        return resp

    @ratelimit.web
    async def call_web(self, path, *, method='GET', **kwargs):
        resp = await self._request(method, NS_URL + path.strip('/'), **kwargs)
        if '<html lang="en" id="page_login">' in resp.text:
            raise AuthenticationError
        if resp.status != 200:
            raise SuddenlyNationstates(f'unexpected status code: {resp.status}')
        return resp


class AuthSession(Session):
    """Allows you to make authenticated requests to NationStates' API, as well
    as its web interface, sharing the session between the two.
    
    Important note: does not check credentials upon initialization, you will
    only know if you've made a mistake after you try to make the first request.
    """
    def __init__(self, name, autologin='', password=''):
        self.name = normalize(name)
        self.password = password
        self.autologin = autologin
        # Weird things happen if the supplied pin doesn't follow the format
        self.pin = '0000000000'

    async def call_api(self, params, **kwargs):
        logger.debug(f'Making authenticated API request as {self.name} to '
                     f'{str(params)}')
        headers = {
            'X-Password': self.password,
            'X-Autologin': self.autologin,
            'X-Pin': self.pin
        }
        resp = await super().call_api(params, headers=headers, **kwargs)
        with suppress(KeyError):
            self.pin = resp.headers['X-Pin']
            logger.debug('Updating pin from API header')
            self.autologin = resp.headers['X-Autologin']
            logger.debug('Setting autologin from API header')
        return resp

    async def call_web(self, path, method='GET', **kwargs):
        if not self.autologin:
            # Obtain autologin in case only password was provided
            await self.call_api({'nation': self.name, 'q': 'nextissue'})
        logger.debug(f'Making authenticated web {method} request as'
                     f' {self.name} to {path} {kwargs.get("data")}')
        cookies = {
            # Will not work with unescaped equals sign
            'autologin': self.name + '%3D' + self.autologin,
            'pin': self.pin
        }
        resp = await super().call_web(path, method=method,
                                      cookies=cookies, **kwargs)
        with suppress(KeyError):
            self.pin = resp.cookies['pin'].value
            logger.debug('Updating pin from web cookie')
        return resp


