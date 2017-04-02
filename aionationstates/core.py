import xml.etree.ElementTree as ET
from collections import namedtuple
from contextlib import suppress

from aionationstates.session import Session, AuthSession, NS_URL
from aionationstates.utils import normalize


Freedom = namedtuple('Freedom', 'civilrights economy politicalfreedom')
Govt = namedtuple('Govt',
                  ('administration defence education environment healthcare'
                   ' commerce internationalaid lawandorder publictransport'
                   ' socialequality spirituality welfare'))

Dispatch = namedtuple('Dispatch', ('id title author category subcategory'
                                       ' created edited views score text'))
Sectors = namedtuple('Sectors', 'blackmarket government industry public')
CensusScale = namedtuple('CensusScale', 'id score rank prank rrank prrank')
CensusPoint = namedtuple('CensusPoint', 'id timestamp score')

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

def parse_api(args, xml):
    """Parse the NationStates API data.
    
    Inconsistencies:
        * 'factbooklist' is left out as completely unnecessary. Use
          'dispatchlist' instead.
        * 'unstatus' is renamed to 'wa'.
        * 'banner' is removed, use 'banners' and indexing.
    """
    args = set(args)
    root = ET.fromstring(xml)
    
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
    
    if 'census' in args:
        census = root.find('CENSUS')
        if census[0][0].tag == 'POINT':
            yield (
                'censushistory',
                {int(scale.get('id')):
                 [CensusPoint(
                     id=int(scale.get('id')),
                     timestamp=int(point.find('TIMESTAMP')),
                     score=int(point.find('SCORE').text)
                  ) for point in scale]
                 for scale in census}
            )
        else:
            def make_scale(elem):
                id = int(scale.get('id'))
                score = rank = prank = rrank = prrank = None
                with suppress(AttributeError, TypeError):
                    score = int(point.find('SCORE').text)
                with suppress(AttributeError, TypeError):
                    rank = int(point.find('RANK').text)
                with suppress(AttributeError, TypeError):
                    prank = int(point.find('PRANK').text)
                with suppress(AttributeError, TypeError):
                    rrank = int(point.find('RRANK').text)
                with suppress(AttributeError, TypeError):
                    prrank = int(point.find('PRRANK').text)
                return CensusScale(id=id, score=score, rank=rank,
                                   prank=prank, rrank=rrank, prrank=prrank)
            yield (
                'census',
                {int(scale.get('id')): make_scale(scale)
                 for scale in census}
            )
    
    
    if 'endorsements' in args:
        endorsements = root.find('ENDORSEMENTS')
        if endorsements.text:
            yield ('endorsements', endorsements.text.split(','))
        else:
            yield ('endorsements', ())
    
    if 'legislation' in args:
        yield ('legislation', [elem.text for elem in root.find('LEGISLATION')])
    
    if 'sectors' in args:
        sectors = root.find('SECTORS')
        yield ('sectors', Sectors(
            blackmarket=float(sectors.find('BLACKMARKET').text),
            government=float(sectors.find('GOVERNMENT').text),
            industry=float(sectors.find('INDUSTRY').text),
            public=float(sectors.find('PUBLIC').text)
        ))



class Nation(Session):
    """A class to access the public information about an NS nation."""
    def __init__(self, nation):
        self.nation = normalize(nation)

    async def shards(self, *shards):
        """A low-level interface to the Nation Shards API."""
        params = {
            'nation': self.nation,
            'q': '+'.join(shards)
        }
        resp = await self.call_api(params=params)
        return dict(parse_api(shards, ET.fromstring(resp.text)))
    


