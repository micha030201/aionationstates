import re
from contextlib import suppress
from collections import namedtuple

import aiohttp

from nkvd import logger
from nkvd.nationstates import ratelimit


NS_URL = 'https://www.nationstates.net/'
API_PATH = 'cgi-bin/api.cgi'
API_URL = NS_URL + API_PATH

USER_AGENT = 'https://github.com/balag12/NKVD-discordbot'


class AuthenticationError(Exception):
    """Raised when NationStates doesn't accept provided credentials."""


class RawResponse(namedtuple('RawResponse', 'status url text history')):
    """A class to store HTTP responses.
    
    Needed because aiohttp's API is weird and every my attempt at making
    a proper use of it has led to sadness and despair.
    """


class NationSession:
    """Allows you to make authenticated requests to NationStates' API, as well
    as its web interface, sharing the session between the two.
    
    You generally shouldn't need to use this class directly, instead picking
    a higher-level abstraction, like PrivateShards or NationControl.
    
    Important note: does not check credentials upon initialization, you will
    only know if you've made a mistake after you try to make the first request.
    """
    def __init__(self, nation, autologin='', password='',
                 user_agent='https://github.com/balag12/NKVD-discordbot'):
        self.user_agent = user_agent
        self.nation = normalize(nation)
        self.password = password
        self.autologin = autologin
        # Weird things happen if the supplied pin doesn't follow the format
        self.pin = '0000000000'

    @ratelimit.api
    async def call_api(self, params):
        logger.debug('Making authenticated API request')
        headers = {
            'User-Agent': self.user_agent,
            'X-Password': self.password,
            'X-Autologin': self.autologin,
            'X-Pin': self.pin
        }
        async with aiohttp.request(
                'GET', API_URL, headers=headers,
                allow_redirects=False, params=params) as resp:
            if resp.status == 403:
                raise AuthenticationError
            with suppress(KeyError):
                self.pin = resp.headers['X-Pin']
                logger.debug('Updating pin from API header')
                self.autologin = resp.headers['X-Autologin']
                logger.debug('Setting autologin from API header')
            return RawResponse(
                status=resp.status,
                url=resp.url,
                history=resp.history,
                text=await resp.text()
            )

    @ratelimit.web
    async def call_web(self, path, method='GET', **kwargs):
        if not self.autologin:
            # Obtain autologin in case only password was provided
            await self.call_api({'nation': self.nation, 'q': 'nextissue'})
        logger.debug('Making authenticated web request')
        headers = {'User-Agent': self.user_agent}
        cookies = {
            # Will not work with unescaped equals sign
            'autologin': self.nation + '%3D' + self.autologin,
            'pin': self.pin
        }
        async with aiohttp.request(
                method, NS_URL + path.strip('/'),
                headers=headers, cookies=cookies, **kwargs) as resp:
            with suppress(KeyError):
                self.pin = resp.cookies['pin'].value
                logger.debug('Updating pin from web cookie')
            
            resp = RawResponse(
                status=resp.status,
                url=resp.url,
                history=resp.history,
                text=await resp.text()
            )
            if '<html lang="en" id="page_login">' in resp.text:
                raise AuthenticationError
            return resp
