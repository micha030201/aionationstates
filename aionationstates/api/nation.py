from functools import partial
from collections import namedtuple

from aionationstates.utils import normalize
from aionationstates.session import AuthSession, NS_URL
from aionationstates.api.shards import (CensusShard, DispatchlistShard,
    StandardShardCases)


Freedom = namedtuple('Freedom', 'civilrights economy politicalfreedom')

Govt = namedtuple('Govt',
                  ('administration defence education environment healthcare'
                   ' commerce internationalaid lawandorder publictransport'
                   ' socialequality spirituality welfare'))

Sectors = namedtuple('Sectors', 'blackmarket government industry public')

class Nation(CensusShard, DispatchlistShard, StandardShardCases):
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
            banners = root.find('BANNERS')
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


Issue = namedtuple('Issue', ('id title author editor text options dismiss'))
IssueOption = namedtuple('IssueOption', ('text accept'))

class NationControl(AuthSession, Nation):
    def __init__(self, *args, only_interface=False, **kwargs):
        self.only_interface = only_interface
        super().__init__(*args, **kwargs)
    
    async def accept_issue(self, issue_id, option_id):
        await self.call_web(
            f'page=enact_dilemma/dilemma={issue_id}',
            method='POST', data={'choice-1': str(option_id)}
        )
    
    def dismiss_issue(self, issue_id):
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
                                    self.accept_issue,
                                    issue.get('id'),
                                    option.get('id')
                                )
                            )
                            for option in issue.findall('OPTION')
                        ],
                        dismiss=partial(
                            self.dismiss_issue,
                            issue.get('id')
                        )
                    )
                    for issue in root.find('ISSUES')
                ]
            )

