import xml.etree.ElementTree as ET
from contextlib import suppress
from collections import namedtuple

from aionationstates.session import Session, AuthSession, NS_URL
from aionationstates.utils import normalize


Freedom = namedtuple('Freedom', 'civilrights economy politicalfreedom')
Govt = namedtuple('Govt',
                  ('administration defence education environment healthcare'
                   ' commerce internationalaid lawandorder publictransport'
                   ' socialequality spirituality welfare'))

Dispatch = namedtuple('Dispatch', ('title author category subcategory'
                                   ' created edited views score'))
Sectors = namedtuple('Sectors', 'blackmarket government industry public')


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
        deaths = root.find('DEATHS')
        self.deaths = {elem.get('type'): float(elem.text) for elem in deaths}
    
    if 'dispatchlist' in args:
        yield ('dispatchlist', {
            elem.get('id'): Dispatch(
                title=elem.find('TITLE').text,
                author=elem.find('AUTHOR').text,
                category=elem.find('CATEGORY').text,
                subcategory=elem.find('SUBCATEGORY').text,
                created=int(elem.find('CREATED').text),
                edited=int(elem.find('EDITED').text),
                views=int(elem.find('VIEWS').text),
                score=int(elem.find('SCORE').text)
            )
            for elem in root.find('DISPATCHLIST')
        })
    
    if 'endorsements' in args:
        endorsements = root.find('ENDORSEMENTS')
        if endorsements.text:
            yield ('endorsements', endorsements.text.split(','))
        else:
            yield ('endorsements', [])
    
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



class NationShards(Session):
    """A class to access NS Nation API public shards."""
    def __init__(self, nation):
        self.nation = normalize(nation)

    async def get(self, *shards):
        params = {
            'nation': self.nation,
            'q': '+'.join(shards)
        }
        resp = await self.call_api(params=params)
        return dict(self._parse(shards, ET.fromstring(resp.text)))
    
    def _parse(self, shards, xml_root):
        assert xml_root.attrib['id'] == self.nation
        if 'animal' in shards:
            yield ('animal', xml_root.find('ANIMAL').text)
        if 'flag' in shards:
            yield ('flag', xml_root.find('FLAG').text)
        # TODO: finish


