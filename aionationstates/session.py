import logging
from contextlib import suppress
from collections import namedtuple
import xml.etree.ElementTree as ET

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


class SuddenlyNationstates(Exception):  # TODO: move to another submodule
    pass


class ApiRequest:
    def __init__(self, *, session, result, q, params=None):
        self.session = session
        self.results = [result]
        self.q = {q}
        self.params = params or {}

    def __await__(self):
        return self._wrap().__await__()

    async def _wrap(self):
        self.params['q'] = '+'.join(self.q)
        resp = await self.session._call_api(self.params)
        root = ET.fromstring(resp.text)  # TODO move into _call_api?
        results = tuple(result(root) for result in self.results)
        return results[0] if len(results) == 1 else results

    def __add__(self, other):
        if self.session is not other.session:
            raise ValueError('ApiRequests do not share the same session')
        if not len(self.q & other.q) == 0:
            raise ValueError('ApiRequests contain the same query')
        if not len(set(self.params) & set(other.params)) == 0:
            # XXX is this actually necessary?
            raise ValueError('ApiRequests contain conflicting params')

        self.q |= other.q
        self.params.update(other.params)
        self.results += other.results
        return self


# Needed because aiohttp's API is weird and every my attempt at making
# a proper use of it has led to sadness and despair.
RawResponse = namedtuple('RawResponse', ('status url text'
                                         ' cookies headers'))

class Session:  # TODO self._useragent
    async def _request(self, method, url, headers=None, **kwargs):
        headers = headers or {}
        headers['User-Agent'] = USER_AGENT
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
        resp = await self._request(method, API_URL, **kwargs)
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

    async def _call_api(self, params, **kwargs):
        return await self._base_call_api('GET', params=params, **kwargs)

    @ratelimit.web
    async def _call_web(self, path, *, method='GET', **kwargs):
        resp = await self._request(method, NS_URL + path.strip('/'), **kwargs)
        if '<html lang="en" id="page_login">' in resp.text:
            raise AuthenticationError
        if resp.status != 200:
            raise SuddenlyNationstates(f'unexpected status code: {resp.status}')
        return resp

    def _compose_api_request(self, *, result, q, params=None):
        return ApiRequest(session=self, q=q, params=params, result=result)


class AuthSession(Session):
    """Allows you to make authenticated requests to NationStates' API, as well
    as its web interface, sharing the session between the two.
    
    Important note: does not check credentials upon initialization, you will
    only know if you've made a mistake after you try to make the first request.
    """
    def __init__(self, id, autologin='', password=''):
        self.id = normalize(id)  # TODO unmess
        self.password = password
        self.autologin = autologin
        # Weird things happen if the supplied pin doesn't follow the format
        self.pin = '0000000000'

    async def _base_call_api(self, method, **kwargs):
        logger.debug(f'Making authenticated API request as {self.id} to '
                     f'{str(kwargs)}')
        headers = {
            'X-Password': self.password,
            'X-Autologin': self.autologin,
            'X-Pin': self.pin
        }
        resp = await super()._base_call_api(method, headers=headers, **kwargs)
        with suppress(KeyError):
            self.pin = resp.headers['X-Pin']
            logger.debug('Updating pin from API header')
            self.autologin = resp.headers['X-Autologin']
            logger.debug('Setting autologin from API header')
        return resp

    async def _call_api_command(self, data, **kwargs):
        return await self._base_call_api('POST', data=data, **kwargs)

    async def _call_web(self, path, method='GET', **kwargs):
        if not self.autologin:
            # Obtain autologin in case only password was provided
            await self._call_api({'nation': self.id, 'q': 'nextissue'})
        logger.debug(f'Making authenticated web {method} request as'
                     f' {self.id} to {path} {kwargs.get("data")}')
        cookies = {
            # Will not work with unescaped equals sign
            'autologin': self.id + '%3D' + self.autologin,
            'pin': self.pin
        }
        resp = await super()._call_web(path, method=method,
                                      cookies=cookies, **kwargs)
        with suppress(KeyError):
            self.pin = resp.cookies['pin'].value
            logger.debug('Updating pin from web cookie')
        return resp


