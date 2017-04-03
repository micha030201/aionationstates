import logging
from contextlib import suppress
from functools import partial
import xml.etree.ElementTree as ET

from aionationstates.data_types import *
from aionationstates.utils import normalize
from aionationstates.session import Session, AuthSession


logger = logging.getLogger('aionationstates')


class Nation(Session):
    async def shards(self, *shards):
        params = {
            'nation': self.nation,
            'q': '+'.join(shards)
        }
        resp = await self.call_api(params=params)
        return dict(self._parse(ET.fromstring(resp.text), set(shards)))

    async def shard(self, shard):
        return (await self.shards(shard))[shard]

    STR_CASES = {
        'name', 'type', 'fullname', 'motto', 'category', 'region', 'animal',
        'currency', 'demonym', 'demonym2', 'demonym2plural', 'flag',
        'majorindustry', 'govtpriority', 'lastactivity', 'influence', 'leader',
        'capital', 'religion', 'admirable', 'animaltrait', 'crime', 'founded',
        'govtdesc', 'industrydesc', 'notable', 'sensibilities'
    }
    INT_CASES = {
        'population', 'firstlogin', 'lastlogin', 'factbooks', 'dispatches',
        'foundedtime', 'gdp', 'income', 'poorest', 'richest'
    }
    FLOAT_CASES = {'tax', 'publicsector'}
    BOOL_CASES = {'tgcanrecruit', 'tgcancampaign'}

    def _parse(self, xml, args):
        """Parse the NationStates API data. Accepts an elementtree and a set,
        returns a generator of (key, value) tuples.
                
        Inconsistencies:
            * factbooklist was left out as unnecessary. Use dispatchlist.
            * unstatus was renamed to wa.
            * banner was removed, use banners and indexing.
            * census with mode=history was renamed to censushistory.
            * partial census, like with rank but not rrank, won't work.
        """
        
        for arg in args & STR_CASES:
            yield (arg, root.find(arg.upper()).text)
        for arg in args & INT_CASES:
            yield (arg, int(root.find(arg.upper()).text))
        for arg in args & FLOAT_CASES:
            yield (arg, float(root.find(arg.upper()).text))
        for arg in args & BOOL_CASES:
            yield (arg, bool(int(root.find(arg.upper()).text)))
        
        if 'unstatus' in args:
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
        
        if 'dispatchlist' in args:
            yield ('dispatchlist', [
                Dispatch(
                    id=int(elem.get('id')),
                    title=elem.find('TITLE').text,
                    author=elem.find('AUTHOR').text,
                    category=elem.find('CATEGORY').text,
                    subcategory=elem.find('SUBCATEGORY').text,
                    created=int(elem.find('CREATED').text),
                    edited=int(elem.find('EDITED').text),
                    views=int(elem.find('VIEWS').text),
                    score=int(elem.find('SCORE').text),
                    text=None
                )
                for elem in root.find('DISPATCHLIST')
            ])
        
        if 'dispatch' in args:
            dispatch = root.find('DISPATCH')
            yield (
                'dispatch',
                Dispatch(
                    id=int(dispatch.get('id')),
                    title=dispatch.find('TITLE').text,
                    author=dispatch.find('AUTHOR').text,
                    category=dispatch.find('CATEGORY').text,
                    subcategory=dispatch.find('SUBCATEGORY').text,
                    created=int(dispatch.find('CREATED').text),
                    edited=int(dispatch.find('EDITED').text),
                    views=int(dispatch.find('VIEWS').text),
                    score=int(dispatch.find('SCORE').text),
                    text=dispatch.find('TEXT').text
                )
            )
        
        if 'censushistory' in args:
            yield (
                'censushistory',
                {int(scale.get('id')):
                 [CensusPoint(
                     id=int(scale.get('id')),
                     timestamp=int(point.find('TIMESTAMP').text),
                     score=float(point.find('SCORE').text)
                  ) for point in scale]
                 for scale in root.find('CENSUS')}
            )
        if 'census' in args:
            yield (
                'census',
                {
                    int(scale.get('id')): CensusScale(
                        id=int(scale.get('id')),
                        score = float(scale.find('SCORE').text),
                        rank = int(scale.find('RANK').text),
                        prank = int(scale.find('PRANK').text),
                        rrank = int(scale.find('RRANK').text),
                        prrank = int(scale.find('PRRANK').text)
                    )
                    for scale in root.find('CENSUS')
                }
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


class NationControl(Nation, AuthSession):
    def __init__(self, *args, only_interface=False,
                 return_census=True, **kwargs):
        self.return_census = return_census
        self.only_interface = only_interface
        self._current_issues = ()
        super().__init__(*args, **kwargs)

    async def get_issues(self):
        if not (self.only_interface and len(_current_issues) == 5):
            self._current_issues = dict(await self.shards('issues'))['issues']
        return self._current_issues
    
    async def _accept(self, issue_id, option_id):
        if self.return_census:
            census_before = await self.shard('census')  # TODO: finish
        self.call_web(
            f'page=enact_dilemma/dilemma={issue_id}',
            method='POST', data={'choice-1': str(option_id)}
        )
    
    def _dismiss(issue_id):
        return self.call_web(
            f'page=dilemmas/dismiss={issue_id}',
            method='POST', data={'choice--1': '1'}
        )

    def _parse(self, xml, args):
        super()._parse(xml, args)
        
        if 'issues' in args:
            yield (
                'issues',
                [
                    Issue(
                        id=int(issue.get('id')),
                        title=issue.find('TITLE').text,
                        text=issue.find('TEXT').text,
                        author=issue.find('AUTHOR').text,
                        editor=getattr(issue.find('EDITOR'), 'text', None),
                        options=[
                            IssueOption(
                                text=option.text,
                                accept=partial(
                                    accept,
                                    issue.get('id'),
                                    option.get('id')
                                )
                            )
                            for option in issue.findall('OPTION')
                        ],
                        dismiss=partial(
                            dismiss,
                            issue.get('id')
                        )
                    )
                    for issue in root.find('ISSUES')
                ]
            )


