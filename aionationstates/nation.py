from functools import partial
from contextlib import suppress
from functools import partial
import xml.etree.ElementTree as ET

from aionationstates.utils import normalize, timestamp, banner_url
from aionationstates.types import Freedom, FreedomScores, Govt, Sectors, NationZombie, Issue, IssueResult
from aionationstates.session import Session, AuthSession, NS_URL, SuddenlyNationstates
from aionationstates.shards import Census, GeneralCases


class Nation(Census, GeneralCases, Session):
    def __init__(self, id):
        self.id = normalize(id)

    def _call_api(self, params, **kwargs):
        params['nation'] = self.id
        return super()._call_api(params, **kwargs)

    def name(self): return self._str_case('name')
    def type(self): return self._str_case('type')
    def fullname(self): return self._str_case('fullname')
    def motto(self): return self._str_case('motto')  # TODO encoding mess
    def category(self): return self._str_case('category')
    def region(self): return self._str_case('region')
    def animal(self): return self._str_case('animal')
    def currency(self): return self._str_case('currency')
    def demonym(self): return self._str_case('demonym')
    def demonym2(self): return self._str_case('demonym2')
    def demonym2plural(self): return self._str_case('demonym2plural')
    def flag(self): return self._str_case('flag')
    def majorindustry(self): return self._str_case('majorindustry')
    def govtpriority(self): return self._str_case('govtpriority')
    def lastactivity(self): return self._str_case('lastactivity')  # TODO there's no timestamp; decide
    def influence(self): return self._str_case('influence')
    def leader(self): return self._str_case('leader')
    def capital(self): return self._str_case('capital')
    def religion(self): return self._str_case('religion')
    def admirable(self): return self._str_case('admirable')
    def animaltrait(self): return self._str_case('animaltrait')
    def crime(self): return self._str_case('crime')
    def govtdesc(self): return self._str_case('govtdesc')
    def industrydesc(self): return self._str_case('industrydesc')
    def notable(self): return self._str_case('notable')
    def sensibilities(self): return self._str_case('sensibilities')

    def population(self): return self._int_case('population')
    def factbooks(self): return self._int_case('factbooks')
    def dispatches(self): return self._int_case('dispatches')
    def gdp(self): return self._int_case('gdp')
    def income(self): return self._int_case('income')
    def poorest(self): return self._int_case('poorest')
    def richest(self): return self._int_case('richest')

    def founded(self):
        return self._compose_api_request(
            q='foundedtime',
            result=lambda root: timestamp(root.find('FOUNDEDTIME').text))

    def firstlogin(self):
        return self._compose_api_request(
            q='firstlogin',
            result=lambda root: timestamp(root.find('FIRSTLOGIN').text))

    def lastlogin(self):
        return self._compose_api_request(
            q='lastlogin',
            result=lambda root: timestamp(root.find('LASTLOGIN').text))

    def wa(self):
        def result(root):
            return root.find('UNSTATUS').text == 'WA Member'
        return self._compose_api_request(q='wa', result=result)

    def banners(self):
        def result(root):
            return [
                banner_url(elem.text)
                for elem in root.find('BANNERS')
            ]
        return self._compose_api_request(q='banners', result=result)

    def freedom(self):
        return self._compose_api_request(
            q='freedom',
            result=lambda root: Freedom(root.find('FREEDOM')))

    def freedomscores(self):
        return self._compose_api_request(
            q='freedomscores',
            result=lambda root: FreedomScores(root.find('FREEDOMSCORES')))

    def govt(self):
        return self._compose_api_request(
            q='govt',
            result=lambda root: Govt(root.find('GOVT')))

    def deaths(self):
        def result(root):
            return {
                elem.get('type'): float(elem.text)
                for elem in root.find('DEATHS')
            }
        return self._compose_api_request(q='deaths', result=result)

    def endorsements(self):
        def result(root):
            text = root.find('ENDORSEMENTS').text
            return text.split(',') if text else ()
        return self._compose_api_request(q='endorsements', result=result)

    def legislation(self):
        def result(root):
            return [elem.text for elem in root.find('LEGISLATION')]
        return self._compose_api_request(q='legislation', result=result)

    def sectors(self):
        return self._compose_api_request(
            q='sectors',
            result=lambda root: Sectors(root.find('SECTORS')))

    def dispatchlist(self):
        def result(root):
            return [
                DispatchThumbnail(elem)
                for elem in root.find('DISPATCHLIST')
            ]
        return self._compose_api_request(q='dispatchlist', result=result)

    def zombie(self):
        return self._compose_api_request(
            q='zombie',
            result=lambda root: NationZombie(root.find('ZOMBIE')))

    def verify(self, checksum, *, token=None):
        params = {'a': 'verify', 'checksum': checksum}
        if token:
            params['token'] = token
        return self._compose_api_request(
            # Needed so that we get output in xml, as opposed to
            # plain text. It doesn't actually matter what the
            # q param is, it's just important that it's not empty.
            q='i_need_the_output_in_xml',
            params=params,
            result=lambda root: bool(int(root.find('VERIFY').text)))

    def verification_url(self, *, token=None):
        if token:
            return f'{NS_URL}page=verify_login?token={token}'
        return f'{NS_URL}page=verify_login'


class NationControl(AuthSession, Nation):
    def _call_api_command(self, data, **kwargs):
        data['nation'] = self.id
        return super()._call_api(data, **kwargs)

    def issues(self):
        def result(root):
            return [Issue(elem, self) for elem in root.find('ISSUES')]
        return self._compose_api_request(q='issues', result=result)

    async def _accept_issue(self, issue_id, option_id):
        data = {
            'c': 'issue',
            'issue': str(issue_id),
            'option': str(option_id)
        }
        resp = await self._call_api_command(data)
        root = ET.fromstring(resp.text)
        return IssueResult(root.find('ISSUE'))


