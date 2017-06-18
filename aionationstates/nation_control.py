from aionationstates.types import Issue, IssueResult
from aionationstates.nation import Nation
from aionationstates.session import Session, api_query, api_command


class NationControl(Nation, Session):
    """Allows you to make authenticated requests to NationStates' API,
    as well as its web interface, sharing the session between the two.

    Does not check credentials upon initialization, you will only know
    if you've made a mistake after you try to make the first request.
    """
    def __init__(self, *args, autologin='', password='', **kwargs):
        self.password = password
        self.autologin = autologin
        # Weird things happen if the supplied pin doesn't follow the format
        self.pin = '0000000000'
        super().__init__(*args, **kwargs)

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

    async def _call_api_command(self, data, **kwargs):
        data['nation'] = self.id
        return await self._base_call_api('POST', data=data, **kwargs)


    def issues(self):
        @api_query('issues')
        def result(root):
            return [Issue(elem, self) for elem in root.find('ISSUES')]
        return result()

    def _accept_issue(self, issue_id, option_id):
        @api_command('issue', issue=str(issue_id), option=str(option_id))
        def result(root):
            return IssueResult(root.find('ISSUE'))
        return result(self)


