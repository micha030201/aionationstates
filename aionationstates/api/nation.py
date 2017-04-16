from functools import partial
from collections import namedtuple

from aionationstates.utils import normalize
from aionationstates.session import Session, AuthSession
from aionationstates.api.mixins import (CensusMixin, DispatchlistMixin,
    StandardCasesMixin, ShardMixin)


Freedom = namedtuple('Freedom', 'civilrights economy politicalfreedom')

Govt = namedtuple('Govt',
                  ('administration defence education environment healthcare'
                   ' commerce internationalaid lawandorder publictransport'
                   ' socialequality spirituality welfare'))

Sectors = namedtuple('Sectors', 'blackmarket government industry public')

class Nation(Session, CensusMixin, DispatchlistMixin, StandardCasesMixin,
             ShardMixin):
    def __init__(self, nation):
        self.nation = normalize(nation)

    def _url_transform(self, params):
        super()._url_transform(params)
        params['nation'] = self.nation

    STR_CASES = {
        'name', 'type', 'fullname', 'motto', 'category', 'region', 'animal',
        'currency', 'demonym', 'demonym2', 'demonym2plural', 'flag',
        'majorindustry', 'govtpriority', 'lastactivity', 'influence', 'leader',
        'capital', 'religion', 'admirable', 'animaltrait', 'crime', 'founded',
        'govtdesc', 'industrydesc', 'notable', 'sensibilities', 'gavote',
        'scvote'
    }
    INT_CASES = {
        'population', 'firstlogin', 'lastlogin', 'factbooks', 'dispatches',
        'foundedtime', 'gdp', 'income', 'poorest', 'richest'
    }
    FLOAT_CASES = {'tax', 'publicsector'}
    BOOL_CASES = {'tgcanrecruit', 'tgcancampaign'}

    def _parse(self, root, args):
        """Parse the NationStates API data. Accepts an elementtree and a set,
        returns a generator of (key, value) tuples.
                
        Inconsistencies:
            * banner was removed, use banners and indexing.
        """
        yield from super()._parse(root, args)
        
        if 'wa' in args:
            yield ('wa', root.find('UNSTATUS').text == 'WA Member')
            
        if 'banners' in args:
            yield (
                'banners',
                [f'{NS_URL}images/banners/{elem.text}.jpg' for elem in banners]
            )

        if 'freedom' in args:
            freedom = root.find('FREEDOM')
            yield ('freedom', Freedom(
                civilrights=freedom.find('CIVILRIGHTS').text,
                economy=freedom.find('ECONOMY').text,
                politicalfreedom=freedom.find('POLITICALFREEDOM').text
            ))
        
        if 'freedomscores' in args:
            freedomscores = root.find('FREEDOMSCORES')
            yield ('freedomscores', Freedom(
                civilrights=int(freedomscores.find('CIVILRIGHTS').text),
                economy=int(freedomscores.find('ECONOMY').text),
                politicalfreedom=int(freedomscores.find('POLITICALFREEDOM').text)
            ))
        
        if 'govt' in args:
            govt = root.find('GOVT')
            yield ('govt', Govt(
                administration=float(govt.find('ADMINISTRATION').text),
                defence=float(govt.find('DEFENCE').text),
                education=float(govt.find('EDUCATION').text),
                environment=float(govt.find('ENVIRONMENT').text),
                healthcare=float(govt.find('HEALTHCARE').text),
                commerce=float(govt.find('COMMERCE').text),
                internationalaid=float(govt.find('INTERNATIONALAID').text),
                lawandorder=float(govt.find('LAWANDORDER').text),
                publictransport=float(govt.find('PUBLICTRANSPORT').text),
                socialequality=float(govt.find('SOCIALEQUALITY').text),
                spirituality=float(govt.find('SPIRITUALITY').text),
                welfare=float(govt.find('WELFARE').text)
            ))
        
        if 'deaths' in args:
            yield (
                'deaths',
                {elem.get('type'): float(elem.text)
                 for elem in root.find('DEATHS')}
            )
        
        if 'endorsements' in args:
            endorsements = root.find('ENDORSEMENTS')
            if endorsements.text:
                yield ('endorsements', endorsements.text.split(','))
            else:
                yield ('endorsements', ())
        
        if 'legislation' in args:
            yield (
                'legislation',
                [elem.text for elem in root.find('LEGISLATION')]
            )
        
        if 'sectors' in args:
            sectors = root.find('SECTORS')
            yield ('sectors', Sectors(
                blackmarket=float(sectors.find('BLACKMARKET').text),
                government=float(sectors.find('GOVERNMENT').text),
                industry=float(sectors.find('INDUSTRY').text),
                public=float(sectors.find('PUBLIC').text)
            ))


# The rest of the values are useless as they don't update immediately
CensusDiff = namedtuple('CensusDiff', 'info score')

Issue = namedtuple('Issue', ('id title author editor text options dismiss'))
IssueOption = namedtuple('IssueOption', ('text accept'))

class NationControl(AuthSession, Nation):
    def __init__(self, *args, only_interface=False,
                 return_census=True, **kwargs):
        self.return_census = return_census
        self.only_interface = only_interface
        self._current_issues = ()
        super().__init__(*args, **kwargs)

    async def get_issues(self):  # TODO: finish & fix
        if not (self.only_interface and len(_current_issues) == 5):
            self._current_issues = await self.shard('issues')
        return self._current_issues
    
    async def _accept(self, issue_id, option_id):
        if self.return_census:
            census_before = await self.shard('census')
        await self.call_web(
            f'page=enact_dilemma/dilemma={issue_id}',
            method='POST', data={'choice-1': str(option_id)}
        )
        if self.return_census:
            census_after = await self.shard('census')
            return {
                id: CensusDiff(
                    info=scale.info,
                    score=scale.score - census_before[id].score
                )
                for id, scale in census_after.items()
            }
    
    def _dismiss(issue_id):
        self.call_web(
            f'page=dilemmas/dismiss={issue_id}',
            method='POST', data={'choice--1': '1'}
        )

    def _parse(self, root, args):
        yield from super()._parse(root, args)
        if 'issues' in args:
            yield (
                'issues',
                [
                    Issue(
                        id=int(issue.get('id')),
                        title=issue.find('TITLE').text,
                        text=issue.find('TEXT').text,
                        author=getattr(issue.find('AUTHOR'), 'text', None),
                        editor=getattr(issue.find('EDITOR'), 'text', None),
                        options=[
                            IssueOption(
                                text=option.text,
                                accept=partial(
                                    self._accept,
                                    issue.get('id'),
                                    option.get('id')
                                )
                            )
                            for option in issue.findall('OPTION')
                        ],
                        dismiss=partial(
                            self._dismiss,
                            issue.get('id')
                        )
                    )
                    for issue in root.find('ISSUES')
                ]
            )


