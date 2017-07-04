import re
from html import unescape
# Needed for type annotations
import datetime
from typing import Dict, List
from aionationstates.ns_to_human import Banner
from aionationstates.session import ApiQuery

from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    Freedom, FreedomScores, Govt, Sectors, NationZombie, DispatchThumbnail)
from aionationstates.session import Session, api_query
from aionationstates.shards import Census
from aionationstates.ns_to_human import banner


class Nation(Census, Session):
    """A class to interact with the NationStates Nation public API.

    Parameters:
        name: Name of the nation.

    Attributes:
        id: The defining characteristic of a nation, its
            normalized name.  No two nations share the same id, and no
            one id is shared by multiple nations.
    """
    id: str

    def __init__(self, name: str) -> None:
        self.id = normalize(name)

    def _call_api(self, params, **kwargs):
        params['nation'] = self.id
        return super()._call_api(params, **kwargs)


    @api_query('name')
    async def name(self, root) -> str:
        """Name of the nation, for example 'Testlandia'."""
        return root.find('NAME').text

    @api_query('type')
    async def type(self, root) -> str:
        """Type of the nation, for example 'Hive Mind'."""
        return root.find('TYPE').text

    @api_query('fullname')
    async def fullname(self, root) -> str:
        """Full name of the nation, for example 'The Hive Mind of
        Testlandia'.
        """
        return root.find('FULLNAME').text

    @api_query('motto')
    async def motto(self, root) -> str:
        """Motto of the nation."""
        return root.find('MOTTO').text  # TODO encoding mess

    @api_query('category')
    async def category(self, root) -> str:
        """Nation's World Assembly Category."""
        return root.find('CATEGORY').text

    @api_query('region')
    async def region(self, root) -> str:
        """Region in which the nation resides."""
        return root.find('REGION').text

    @api_query('animal')
    async def animal(self, root) -> str:
        """Nation's national animal."""
        return root.find('ANIMAL').text

    @api_query('currency')
    async def currency(self, root) -> str:
        """Nation's national currency."""
        return root.find('CURRENCY').text

    @api_query('demonym')
    async def demonym(self, root) -> str:
        """Nation's demonym, as an adjective.

        Example: Testlandish, as in 'I'm proud to be Testlandish.'
        """
        return root.find('DEMONYM').text

    @api_query('demonym2')
    async def demonym2(self, root) -> str:
        """Nation's demonym, as a noun.

        Example: Testlandian, as in 'I'm a proud Testlandian.'
        """
        return root.find('DEMONYM2').text

    @api_query('demonym2plural')
    async def demonym2plural(self, root) -> str:
        """Plural of the nation's noun demonym.

        Example: Testlandians, as in 'Here come the Testlandians!'
        """
        return root.find('DEMONYM2PLURAL').text

    @api_query('flag')
    async def flag(self, root) -> str:
        """URL of the nation's flag."""
        return root.find('FLAG').text

    @api_query('majorindustry')
    async def majorindustry(self, root) -> str:
        """The industry prioritized by the nation."""
        return root.find('MAJORINDUSTRY').text

    @api_query('govtpriority')
    async def govtpriority(self, root) -> str:
        """Part of government (Welfare, Administration, Defence, ...)
        prioritized by the nation.
        """
        return root.find('GOVTPRIORITY').text  # TODO we have the govt shard, is this necessary?

    @api_query('lastactivity')
    async def lastactivity(self, root) -> str:
        return root.find('LASTACTIVITY').text  # TODO there's no timestamp; decide

    @api_query('influence')
    async def influence(self, root) -> str:
        return root.find('INFLUENCE').text

    @api_query('leader')
    async def leader(self, root) -> str:
        """Nation's leader.  Either set by the user or the default
        'Leader'.
        """
        return root.find('LEADER').text

    @api_query('capital')
    async def capital(self, root) -> str:
        """Nation's capital. Either set by the user or the default
        '`name` City.'
        """
        return root.find('CAPITAL').text

    @api_query('religion')
    async def religion(self, root) -> str:
        """Nation's main religion.  Either set by the user or the
        default 'a major religion.'
        """
        return root.find('RELIGION').text

    @api_query('admirable')
    async def admirable(self, root) -> str:
        """One of the nation's qualities, at random.

        Example: 'environmentally stunning'
        """
        return root.find('ADMIRABLE').text

    @api_query('animaltrait')
    async def animaltrait(self, root) -> str:
        """Short characteristic of the nation's national animal.

        Example: 'frolics freely in the nation's sparkling oceans'
        """
        return root.find('ANIMALTRAIT').text

    @api_query('crime')
    async def crime(self, root) -> str:
        """A sentence describing the nation's crime levels.

        Example: 'Crime is totally unknown, thanks to a very
        well-funded police force and progressive social policies in
        education and welfare.'
        """
        return root.find('CRIME').text

    @api_query('govtdesc')
    async def govtdesc(self, root) -> str:
        """A couple of sentences describing the nation's government.

        Example: 'It is difficult to tell where the omnipresent
        government stops and the rest of society begins, but it
        juggles the competing demands of Defense, Environment, and
        Healthcare. It meets to discuss matters of state in the
        capital city of Test City.'
        """
        return root.find('GOVTDESC').text

    @api_query('industrydesc')
    async def industrydesc(self, root) -> str:
        """A couple of sentences describing the nation's economy,
        industry, and average income.

        Example: 'The strong Testlandish economy, worth a remarkable
        2,212 trillion denarii a year, is driven almost entirely by
        government activity. The industrial sector, which is extremely
        specialized, is mostly made up of the Arms Manufacturing
        industry, with major contributions from Book Publishing.
        Average income is 73,510 denarii, with the richest citizens
        earning 6.0 times as much as the poorest.'
        """
        return root.find('INDUSTRYDESC').text

    @api_query('notable')
    async def notable(self, root) -> str:
        """A few of nation's peculiarities, at random.

        Example: 'museums and concert halls, multi-spousal wedding
        ceremonies, and devotion to social welfare'
        """
        return root.find('NOTABLE').text

    @api_query('sensibilities')
    async def sensibilities(self, root) -> str:
        """A couple of adjectives describing the nation's citizens.

        Example: 'compassionate, devout'
        """
        return root.find('SENSIBILITIES').text


    @api_query('population')
    async def population(self, root) -> int:
        """Nation's population, in millions."""
        return int(root.find('POPULATION').text)

    @api_query('factbooks')
    async def factbooks(self, root) -> int:
        return int(root.find('FACTBOOKS').text)  # TODO we have the dispatch shard, is this necessary?

    @api_query('dispatches')
    async def dispatches(self, root) -> int:
        return int(root.find('DISPATCHES').text)  # TODO we have the dispatch shard, is this necessary?

    @api_query('gdp')
    async def gdp(self, root) -> int:
        """Nation's gross domestic product."""
        return int(root.find('GDP').text)

    @api_query('income')
    async def income(self, root) -> int:
        """Average income in the nation."""
        return int(root.find('INCOME').text)  # TODO we have census, is this necessary?

    @api_query('poorest')
    async def poorest(self, root) -> int:
        """Average income of poor in the nation."""
        return int(root.find('POOREST').text)  # TODO we have census, is this necessary?

    @api_query('richest')
    async def richest(self, root) -> int:
        """Average income of rich in the nation."""
        return int(root.find('RICHEST').text)    # TODO we have census, is this necessary?

    @api_query('foundedtime')
    async def founded(self, root) -> datetime.datetime:
        """When the nation was founded.

        ``1970-01-01 00:00`` for nations founded in Antiquity.
        """
        return timestamp(root.find('FOUNDEDTIME').text)

    @api_query('firstlogin')
    async def firstlogin(self, root) -> datetime.datetime:
        """When the nation was first logged into.

        ``1970-01-01 00:00`` for nations first logged into during
        Antiquity.
        """
        return timestamp(root.find('FIRSTLOGIN').text)

    @api_query('lastlogin')
    async def lastlogin(self, root) -> datetime.datetime:
        """When the nation was last logged into."""
        return timestamp(root.find('LASTLOGIN').text)

    @api_query('wa')
    async def wa(self, root) -> bool:
        """Whether the nation is a member of the World Assembly or not."""
        return root.find('UNSTATUS').text == 'WA Member'

    @api_query('freedom')
    async def freedom(self, root) -> Freedom:
        """Nation's `Freedoms`: three basic indicators of the nation's
        Civil Rights, Economy, and Political Freedom, as expressive
        adjectives.
        """
        return Freedom(root.find('FREEDOM'))

    @api_query('freedomscores')
    async def freedomscores(self, root) -> FreedomScores:
        """Nation's `Freedoms`: three basic indicators of the nation's
        Civil Rights, Economy, and Political Freedom, as percentages.
        """
        return FreedomScores(root.find('FREEDOMSCORES'))

    @api_query('govt')
    async def govt(self, root) -> Govt:
        """Nation's government expenditure, as percentages."""
        return Govt(root.find('GOVT'))

    @api_query('deaths')
    async def deaths(self, root) -> Dict[str, float]:
        """Causes of death in the nation, as percentages."""
        return {
            elem.get('type'): float(elem.text)
            for elem in root.find('DEATHS')
        }

    @api_query('endorsements')
    async def endorsements(self, root) -> List[str]:
        """Endorsements the nation has received."""
        text = root.find('ENDORSEMENTS').text
        return text.split(',') if text else []

    @api_query('legislation')
    async def legislation(self, root) -> List[str]:
        """Effects of the most recently passed legislation.

        May contain HTML elements and character references.
        """
        return [elem.text for elem in root.find('LEGISLATION')]

    @api_query('sectors')
    async def sectors(self, root) -> Sectors:
        """Components of the nation's economy, as percentages."""
        return Sectors(root.find('SECTORS'))

    @api_query('dispatchlist')
    async def dispatchlist(self, root) -> List[DispatchThumbnail]:
        """Nation's published dispatches."""
        return [
            DispatchThumbnail(elem)
            for elem in root.find('DISPATCHLIST')
        ]

    @api_query('zombie')
    async def zombie(self, root) -> NationZombie:
        """Nation's condition during the annual Z-Day event."""
        return NationZombie(root.find('ZOMBIE'))

    def verify(self, checksum: str, *, token: str = None) -> ApiQuery[bool]:
        """Interface to the `NationStates Verification API
        <https://www.nationstates.net/pages/api.html#verification>`_.

        Parameters:
            checksum: The user-supplied verification code.  Expires if
                the nation logs out, if it performs a significant
                in-game action such as moving regions or endorsing
                another nation, and after it is successfully verified.
            token: A token specific to your service and the nation
                being verified.
        """
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

    def verification_url(self, *, token: str = None) -> str:
        """URL the user needs to follow in order to get the
        verification code for the nation.

        Parameters:
            token: A token specific to your service and the nation
                being verified.
        """
        if token:
            return ('https://www.nationstates.net/'
                    f'page=verify_login?token={token}')
        return f'https://www.nationstates.net/page=verify_login'

    @api_query('banners')
    async def banners(self, root) -> List[Banner]:
        """Nation's visible banners.  If the user has set a primary
        banner, it will be the first element in the list.
        """
        expand_macros = self._get_macros_expander()
        return [
            await banner(elem.text)._expand_macros(expand_macros)
            for elem in root.find('BANNERS')
        ]

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

    async def description(self) -> str:
        """Nation's full description, as seen on its in-game page."""
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

