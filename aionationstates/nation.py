import re
from html import unescape

from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    Freedom, FreedomScores, Govt, Sectors, NationZombie, DispatchThumbnail)
from aionationstates.session import Session, api_query
from aionationstates.shards import Census
from aionationstates.world import World


world = World()


class Nation(Census, Session):
    def __init__(self, id, *args, **kwargs):
        self.id = normalize(id)
        super().__init__(*args, **kwargs)

    def _call_api(self, params, **kwargs):
        params['nation'] = self.id
        return super()._call_api(params, **kwargs)


    @api_query('name')
    async def name(self, root):
        return root.find('NAME').text

    @api_query('type')
    async def type(self, root):
        return root.find('TYPE').text

    @api_query('fullname')
    async def fullname(self, root):
        return root.find('FULLNAME').text

    @api_query('motto')
    async def motto(self, root):
        return root.find('MOTTO').text  # TODO encoding mess

    @api_query('category')
    async def category(self, root):
        return root.find('CATEGORY').text

    @api_query('region')
    async def region(self, root):
        return root.find('REGION').text

    @api_query('animal')
    async def animal(self, root):
        return root.find('ANIMAL').text

    @api_query('currency')
    async def currency(self, root):
        return root.find('CURRENCY').text

    @api_query('demonym')
    async def demonym(self, root):
        return root.find('DEMONYM').text

    @api_query('demonym2')
    async def demonym2(self, root):
        return root.find('DEMONYM2').text

    @api_query('demonym2plural')
    async def demonym2plural(self, root):
        return root.find('DEMONYM2PLURAL').text

    @api_query('flag')
    async def flag(self, root):
        return root.find('FLAG').text

    @api_query('majorindustry')
    async def majorindustry(self, root):
        return root.find('MAJORINDUSTRY').text

    @api_query('govtpriority')
    async def govtpriority(self, root):
        return root.find('GOVTPRIORITY').text

    @api_query('lastactivity')
    async def lastactivity(self, root):
        return root.find('LASTACTIVITY').text  # TODO there's no timestamp; decide

    @api_query('influence')
    async def influence(self, root):
        return root.find('INFLUENCE').text

    @api_query('leader')
    async def leader(self, root):
        return root.find('LEADER').text

    @api_query('capital')
    async def capital(self, root):
        return root.find('CAPITAL').text

    @api_query('religion')
    async def religion(self, root):
        return root.find('RELIGION').text

    @api_query('admirable')
    async def admirable(self, root):
        return root.find('ADMIRABLE').text

    @api_query('animaltrait')
    async def animaltrait(self, root):
        return root.find('ANIMALTRAIT').text

    @api_query('crime')
    async def crime(self, root):
        return root.find('CRIME').text

    @api_query('govtdesc')
    async def govtdesc(self, root):
        return root.find('GOVTDESC').text

    @api_query('industrydesc')
    async def industrydesc(self, root):
        return root.find('INDUSTRYDESC').text

    @api_query('notable')
    async def notable(self, root):
        return root.find('NOTABLE').text

    @api_query('sensibilities')
    async def sensibilities(self, root):
        return root.find('SENSIBILITIES').text


    @api_query('population')
    async def population(self, root):
        return int(root.find('POPULATION').text)

    @api_query('factbooks')
    async def factbooks(self, root):
        return int(root.find('FACTBOOKS').text)

    @api_query('dispatches')
    async def dispatches(self, root):
        return int(root.find('DISPATCHES').text)

    @api_query('gdp')
    async def gdp(self, root):
        return int(root.find('GDP').text)

    @api_query('income')
    async def income(self, root):
        return int(root.find('INCOME').text)

    @api_query('poorest')
    async def poorest(self, root):
        return int(root.find('POOREST').text)

    @api_query('richest')
    async def richest(self, root):
        return int(root.find('RICHEST').text)

    @api_query('foundedtime')
    async def founded(self, root):
        return timestamp(root.find('FOUNDEDTIME').text)

    @api_query('firstlogin')
    async def firstlogin(self, root):
        return timestamp(root.find('FIRSTLOGIN').text)

    @api_query('lastlogin')
    async def lastlogin(self, root):
        return timestamp(root.find('LASTLOGIN').text)

    @api_query('wa')
    async def wa(self, root):
        return root.find('UNSTATUS').text == 'WA Member'

    @api_query('freedom')
    async def freedom(self, root):
        return Freedom(root.find('FREEDOM'))

    @api_query('freedomscores')
    async def freedomscores(self, root):
        return FreedomScores(root.find('FREEDOMSCORES'))

    @api_query('govt')
    async def govt(self, root):
        return Govt(root.find('GOVT'))

    @api_query('deaths')
    async def deaths(self, root):
        return {
            elem.get('type'): float(elem.text)
            for elem in root.find('DEATHS')
        }

    @api_query('endorsements')
    async def endorsements(self, root):
        text = root.find('ENDORSEMENTS').text
        return text.split(',') if text else ()

    @api_query('legislation')
    async def legislation(self, root):
        return [elem.text for elem in root.find('LEGISLATION')]

    @api_query('sectors')
    async def sectors(self, root):
        return Sectors(root.find('SECTORS'))

    @api_query('dispatchlist')
    async def dispatchlist(self, root):
        return [
            DispatchThumbnail(elem)
            for elem in root.find('DISPATCHLIST')
        ]

    @api_query('zombie')
    async def zombie(self, root):
        return NationZombie(root.find('ZOMBIE'))

    def verify(self, checksum, *, token=None):
        params = {'a': 'verify', 'checksum': checksum}
        if token:
            params['token'] = token
        # Needed so that we get output in xml, as opposed to
        # plain text. It doesn't actually matter what the
        # q param is, it's just important that it's not empty.
        @api_query('i_need_the_output_in_xml', **params)
        async def result(self, root):
            return bool(int(root.find('VERIFY').text))
        return result(self)

    def verification_url(self, *, token=None):
        if token:
            return 'https://www.nationstates.net/'
                   f'page=verify_login?token={token}'
        return f'https://www.nationstates.net/page=verify_login'

    @api_query('banners')
    async def banners(self, root):
        ids = [elem.text for elem in root.find('BANNERS')]
        return await world._make_banners(
            ids, expand_macros=self._get_macros_expander())

    def _get_macros_expander(self):
        # TODO rewrite to join this request with the one that returns banner ids?

        # The only macros present in the banner names are name,
        # demonym, and faith.  If the NS admins ever choose to answer
        # my request and fix the unexpanded macros in issue effect
        # headlines, the rest should probably be removed as unnecessary.
        query = (
            self.demonym() + self.demonym2() + self.demonym2plural()
            + self.name() + self.religion() + self.animal() + self.capital()
            + self.leader()
        )
        query_result = None

        async def expand_macros(line):
            nonlocal query_result
            if '@@' in line:
                if query_result is None:
                    # Only request macros data if we need it
                    query_result = await query
                return (
                    line
                    .replace('@@DEMONYM@@', query_result[0])
                    .replace('@@DEMONYM2@@', query_result[1])
                    # Not documented, or even mentioned anywhere.
                    # Discovered through experimentation.  No idea if
                    # that's a pattern or not.
                    # More experimentation will tell, I guess?
                    .replace('@@PL(DEMONYM2)@@', query_result[2])
                    .replace('@@NAME@@', query_result[3])
                    .replace('@@FAITH@@', query_result[4])
                    .replace('@@ANIMAL@@', query_result[5])
                    # I feel filthy just looking at this.  Surely, NS
                    # wouldn't put bits of Perl code to be executed into
                    # macros?  Surely, their systems can't be that bad?
                    # Yeah right.  Ha ha.  Ha.
                    .replace('@@$nation->query_capital()@@', query_result[6])
                    # I wasn't that nihilistic before starting to write
                    # this library, was I?
                    .replace('@@LEADER@@', query_result[7])
                )
            return line

        return expand_macros

    async def description(self):
        resp = await self._call_web(f'nation={self.id}')
        return unescape(
            re.search(
                '<div class="nationsummary">(.+?)<p class="nationranktext">',
                resp.text,
                flags=re.DOTALL
            )
            .group(1)
            .replace('\n', '')
            .replace('</p>', '')
            .replace('<p>', '\n\n')
            .strip()
        )

