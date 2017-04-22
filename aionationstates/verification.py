import re
from contextlib import suppress
from hashlib import sha256
from secrets import token_hex

from aionationstates.utils import normalize
from aionationstates.session import Session, NS_URL


class Verify(Session):
    """An interface to the NationStates' Verification API.
    Does not use a token.
    """
    def __init__(self, nation):
        self.nation = normalize(nation)
        self.url = (NS_URL + 'page=verify_login')

    async def check(self, checksum):
        if not re.match('^[a-zA-Z0-9_-]{43}$', checksum):
            return False
        params = {
            'a': 'verify',
            'nation': self.nation,
            'checksum': checksum
        }
        with suppress(AttributeError):
            params['token'] = self.token
        return await self.call_api(params=params).text == '1\n'


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


