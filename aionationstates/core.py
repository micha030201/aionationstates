import logging

from aionationstates.parser import parse_api
from aionationstates.utils import normalize
from aionationstates.call import call_api, call_web


logger = logging.getLogger('aionationstates')


async def shards(*shards, nation=None, region=None, wa=None):
    params = {'q': '+'.join(shards)}
    if nation:
        params['nation'] = nation
    if region:
        params['region'] = region
    if wa:
        params['wa'] = '1'
    resp = await call_api(params=params)
    return dict(parse_api(shards, resp.text))


class NationControl:
    """Allows you to make authenticated requests to NationStates' API, as well
    as its web interface, sharing the session between the two.
    
    Important note: does not check credentials upon initialization, you will
    only know if you've made a mistake after you try to make the first request.
    """
    def __init__(self, nation, autologin='', password='',
                 only_interface=False):
        self.only_interface = only_interface
        self._current_issues = ()
        
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
        resp = await call_api(headers=headers, params=params)
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
        resp = await call_web(method, cookies=cookies, data=data)
        with suppress(KeyError):
            self.pin = resp.cookies['pin'].value
            logger.debug('Updating pin from web cookie')
        return resp
    
    async def shards(self, *shards):
        params = {
            'nation': self.nation,
            'q': '+'.join(shards)
        }
        resp = await self.call_api(params=params)
        return dict(parse_api(shards, resp.text, call_web=self.call_web))
    
    async def get_issues(self):
        if not (self.only_interface and len(_current_issues) == 5):
            self._current_issues = dict(await self.shards('issues'))['issues']
        return self._current_issues
        


