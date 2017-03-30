import re
from contextlib import suppress
from collections import namedtuple

import aiohttp

from nkvd import logger
from nkvd.nationstates import ratelimit
from nkvd.nationstates.utils import normalize


NS_URL = 'https://www.nationstates.net/'
API_PATH = 'cgi-bin/api.cgi'
API_URL = NS_URL + API_PATH

USER_AGENT = 'https://github.com/balag12/NKVD-discordbot'


class AuthenticationError(Exception):
    """Raised when NationStates doesn't accept provided credentials."""


class RawResponse(namedtuple('RawResponse',
                             'status url text cookies headers history')):
    """A class to store HTTP responses.
    
    Needed because aiohttp's API is weird and every my attempt at making
    a proper use of it has led to sadness and despair.
    """


class _Session:
    async def _request(self, method, url, headers=None, **kwargs):
        headers = headers or {}
        headers['User-Agent'] = USER_AGENT
        async with aiohttp.request(method, url,
                                   headers=headers, **kwargs) as resp:
            return RawResponse(
                status=resp.status,
                url=resp.url,
                cookies=resp.cookies,
                headers=resp.headers,
                history=resp.history,
                text=await resp.text()
            )


class ApiSession(_Session):
    @ratelimit.api
    async def call_api(self, **kwargs):
        resp = await self._request('GET', API_URL,
                                   allow_redirects=False, **kwargs)
        if resp.status == 403:
            raise AuthenticationError
        return resp


class WebSession(_Session):  
    @ratelimit.web
    async def call_web(self, path, method='GET', **kwargs):
        resp = await self._request(method, NS_URL + path.strip('/'), **kwargs)
        if '<html lang="en" id="page_login">' in resp.text:
            raise AuthenticationError
        return resp


class NationSession(WebSession, ApiSession):
    """Allows you to make authenticated requests to NationStates' API, as well
    as its web interface, sharing the session between the two.
    
    You generally shouldn't need to use this class directly, instead picking
    a higher-level abstraction, like PrivateShards or NationControl.
    
    Important note: does not check credentials upon initialization, you will
    only know if you've made a mistake after you try to make the first request.
    """
    def __init__(self, nation, autologin='', password=''):
        self.nation = normalize(nation)
        self.password = password
        self.autologin = autologin
        # Weird things happen if the supplied pin doesn't follow the format
        self.pin = '0000000000'

    async def call_api(self, params):
        logger.debug(f'Making authenticated API request as {self.nation}')
        headers = {
            'X-Password': self.password,
            'X-Autologin': self.autologin,
            'X-Pin': self.pin
        }
        resp = await super().call_api(headers=headers, params=params)
        with suppress(KeyError):
            self.pin = resp.headers['X-Pin']
            logger.debug('Updating pin from API header')
            self.autologin = resp.headers['X-Autologin']
            logger.debug('Setting autologin from API header')
        return resp

    async def call_web(self, path, method='GET', data=None):
        if not self.autologin:
            # Obtain autologin in case only password was provided
            await self.call_api({'nation': self.nation, 'q': 'nextissue'})
        logger.debug(f'Making authenticated web request as {self.nation}')
        cookies = {
            # Will not work with unescaped equals sign
            'autologin': self.nation + '%3D' + self.autologin,
            'pin': self.pin
        }
        resp = await super().call_web(method, cookies=cookies, data=data)
        with suppress(KeyError):
            self.pin = resp.cookies['pin'].value
            logger.debug('Updating pin from web cookie')
        return resp


