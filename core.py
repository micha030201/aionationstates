import re
from hashlib import sha256
from contextlib import suppress
from collections import namedtuple

import aiohttp

from nkvd import config, logger
from nkvd.nationstates import ratelimit


ns_url = 'https://www.nationstates.net/'
api_path = 'cgi-bin/api.cgi'
api_url = ns_url + api_path


class RawResponse(namedtuple('RawResponse', 'status url text history')):
    """A class to store HTTP responses.
    
    Needed because aiohttp's API is weird and every my attempt at making
    a proper use of it has led to sadness and despair.
    """

class AuthenticationError(Exception):
    """Raised when NationStates doesn't accept provided credentials."""


def normalize(nation):
    nation = nation.lower().replace(' ', '_')
    if not re.match('^[a-z0-9_-]+$', nation):
        raise ValueError('Nation name contains invalid characters.')
    return nation


class NationSession:
    """Allows you to make authenticated requests to NationStates' API, as well
    as its web interface, sharing the session between the two.
    
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
                'GET', api_url, headers=headers,
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
            r = await self.call_api({'nation': self.nation, 'q': 'nextissue'})
        logger.debug('Making authenticated web request')
        print(path)
        headers = {'User-Agent': self.user_agent}
        cookies = {
            # Will not work with unescaped equals sign
            'autologin': self.nation + '%3D' + self.autologin,
            'pin': self.pin
        }
        async with aiohttp.request(
                method, ns_url + path.strip('/'),
                headers=headers, cookies=cookies, **kwargs) as resp:
            with suppress(KeyError):
                self.pin = resp.cookies['pin'].value
                logger.debug('Updating pin from web cookie')
            
            resp =  RawResponse(
                status=resp.status,
                url=resp.url,
                history=resp.history,
                text=await resp.text()
            )
            if '<html lang="en" id="page_login">' in resp.text:
                raise AuthenticationError
            return resp


class Verify:
    """An interface to the NationStates' Verification API."""
    def __init__(self, nation):
        self.nation = normalize(nation)
        self.token = sha256(
            config['NATIONSTATES_SECRET_KEY'].encode() +
            nation.encode()
        ).hexdigest()
        self.url =  ('https://www.nationstates.net/page=verify_login?token=' +
                     self.token)

    async def check(self, checksum):
        if not re.match('^[a-zA-Z0-9_-]{43}$', checksum):
            return False
        params = {
            'a': 'verify',
            'nation': self.nation,
            'checksum': checksum,
            'token': self.token
        }
        async with aiohttp.request('GET', api_url, params=params) as resp:
            text = await resp.text()
        return text == '1\n'

#class Shards:
#    """A class to access NS Nation API public shards.
#    
#    Does NOT support World Census shards. One day I'll write a separate class
#    for those pesky things, but not today.
#    
#    Does NOT check if the shards you're requesting exist. We are not
#    responsible for the damages.
#    """
#    def __init__(self, nation):
#        self.nation = normalize(nation)
    
#    async def _download(self, shards):  # this won't work
#        params = {
#            'nation': self.nation,
#            'q': '+'.join(shards)
#        }
#        async with session.get(api_url, params=params) as resp:
#            text = await resp.text()
        
    
#    async def get(self, *shards):
        
        
        


