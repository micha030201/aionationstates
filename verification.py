
class Verify:
    """An interface to the NationStates' Verification API."""
    def __init__(self, nation):
        self.nation = normalize(nation)
        self.token = sha256(
            config['NATIONSTATES_SECRET_KEY'].encode() +
            nation.encode()
        ).hexdigest()
        self.url = (NS_URL + 'page=verify_login?token=' + self.token)

    async def check(self, checksum):
        if not re.match('^[a-zA-Z0-9_-]{43}$', checksum):
            return False
        params = {
            'a': 'verify',
            'nation': self.nation,
            'checksum': checksum,
            'token': self.token
        }
        async with aiohttp.request('GET', API_URL, params=params) as resp:
            text = await resp.text()
        return text == '1\n'
