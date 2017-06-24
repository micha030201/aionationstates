import logging
from operator import add
from functools import reduce
from contextlib import suppress

from aionationstates.types import Issue, IssueResult
from aionationstates.nation import Nation
from aionationstates.session import Session, api_query, api_command
from aionationstates.world import World


logger = logging.getLogger('discord-plays-nationstates')
world = World()


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
        headers = {
            'X-Password': self.password,
            'X-Autologin': self.autologin,
            'X-Pin': self.pin
        }
        resp = await super()._base_call_api(method, headers=headers, **kwargs)
        with suppress(KeyError):
            self.pin = resp.headers['X-Pin']
            logger.info(f'Updating pin for {self.id} from API header')
            self.autologin = resp.headers['X-Autologin']
            logger.debug(f'Setting autologin for {self.id} from API header')
        return resp

    async def _call_web(self, path, method='GET', **kwargs):
        if not self.autologin:
            # Obtain autologin in case only password was provided
            await self._call_api({'nation': self.id, 'q': 'nextissue'})
        cookies = {
            # Will not work with unescaped equals sign
            'autologin': self.id + '%3D' + self.autologin,
            'pin': self.pin
        }
        resp = await super()._call_web(path, method=method,
                                      cookies=cookies, **kwargs)
        with suppress(KeyError):
            self.pin = resp.cookies['pin'].value
            logger.info(f'Updating pin for {self.id} from web cookie')
        return resp

    async def _call_api_command(self, data, **kwargs):
        data['nation'] = self.id
        return await self._base_call_api('POST', data=data, **kwargs)

    # Away from the boring Session nonsense, onto the new and
    # exciting API private shards and commands!

    @api_query('issues')
    async def issues(self, root):
        issues = [Issue(elem, self) for elem in root.find('ISSUES')]

        # The idea is to call make_banners only once, as it makes
        # a request to the API
        banners = await world._make_banners(
            reduce(add, (issue.banners for issue in issues)),
            expand_macros=self._get_macros_expander()
        )
        for issue in issues:
            # If there even is a better way of doing this, I'm
            # sure not seeing it
            issue.banners = banners[:len(issue.banners)]
            del banners[:len(issue.banners)]

        return issues

    def _accept_issue(self, issue_id, option_id):
        @api_command('issue', issue=str(issue_id), option=str(option_id))
        async def result(self, root):
            issue_result = IssueResult(root.find('ISSUE'))
            expand_macros = self._get_macros_expander()
            issue_result.banners = await world._make_banners(
                issue_result.banners,
                expand_macros=expand_macros
            )
            issue_result.headlines = [
                await expand_macros(headline)
                for headline in issue_result.headlines
            ]
            return issue_result
        return result(self)

