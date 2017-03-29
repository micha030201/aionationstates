import re

from contextlib import suppress
from hashlib import sha256
from secrets import token_hex

import aiohttp

from nkvd.nationstates.core import API_URL, NS_URL, USER_AGENT, normalize
from nkvd.nationstates import ratelimit


class Verify:
    """An interface to the NationStates' Verification API.
    Does not use a token.
    """
    def __init__(self, nation):
        self.nation = normalize(nation)
        self.url = (NS_URL + 'page=verify_login')
    
    async def check(self, checksum):
        if not re.match('^[a-zA-Z0-9_-]{43}$', checksum):
            return False
        return await self._call(checksum)
        
    @ratelimit.api
    async def _call(self, checksum):
        """Get regex out of ratelimit."""
        headers = {'User-Agent': USER_AGENT}
        params = {
            'a': 'verify',
            'nation': self.nation,
            'checksum': checksum
        }
        with suppress(AttributeError):
            params['token'] = self.token
        async with aiohttp.request('GET', API_URL, headers=headers,
                                   params=params) as resp:
            return await resp.text() == '1\n'


class TokenVerify(Verify):
    """Generates a token based on a secret key you provide."""
    def __init__(self, nation, secret_key):
        self.nation = normalize(nation)
        self.token = sha256(
            secret_key.encode() +
            nation.encode()
        ).hexdigest()
        self.url = (NS_URL + 'page=verify_login?token=' + self.token)


class RandomTokenVerify(Verify):
    """Generates a random token per class instance."""
    def __init__(self, nation):
        self.nation = normalize(nation)
        self.token = token_hex(32)
        self.url = (NS_URL + 'page=verify_login?token=' + self.token)


