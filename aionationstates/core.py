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

def _banner_url(code):
    return f'{NS_URL}images/banners/{code}.jpg'

class NationData:
    """A class to parse and represent Nation API data.
    Intended to be as close to the raw API data as possible, while remaining
    usable.
    
    Inconsistencies:
        * factbooklist was left out as completely unnecessary. Use
          dispatchlist instead.
    """
    str_cases = (
        'NAME', 'TYPE', 'FULLNAME', 'MOTTO', 'CATEGORY', 'REGION', 'ANIMAL',
        'CURRENCY', 'DEMONYM', 'DEMONYM2', 'DEMONYM2PLURAL', 'FLAG',
        'MAJORINDUSTRY', 'GOVTPRIORITY', 'LASTACTIVITY', 'INFLUENCE', 'LEADER',
        'CAPITAL', 'RELIGION', 'ADMIRABLE', 'ANIMALTRAIT', 'CRIME', 'FOUNDED',
        'GOVTDESC', 'INDUSTRYDESC', 'NOTABLE', 'SENSIBILITIES', 
    )
    int_cases = (
        'POPULATION', 'FIRSTLOGIN', 'LASTLOGIN', 'FACTBOOKS', 'DISPATCHES',
        'FOUNDEDTIME', 'GDP', 'INCOME', 'POOREST', 'RICHEST', 
    )
    float_cases = ('TAX', 'PUBLICSECTOR')
    bool_cases = ('TGCANRECRUIT', 'TGCANCAMPAIGN')
    def __init__(self, xml):
        root = ET.fromstring(xml)
        assert root.tag == 'NATION'
        
        for tag in self.str_cases:
            with suppress(AttributeError):
                setattr(self, tag.lower(), root.find(tag).text)
        for tag in self.int_cases:
            with suppress(AttributeError):
                setattr(self, tag.lower(), int(root.find(tag).text))
        for tag in self.float_cases:
            with suppress(AttributeError):
                setattr(self, tag.lower(), float(root.find(tag).text))
        for tag in self.bool_cases:
            with suppress(AttributeError):
                setattr(self, tag.lower(), bool(int(root.find(tag).text)))
        
        with suppress(AttributeError):
            self.unstatus = self.wa = root.find('UNSTATUS').text == 'WA Member'

        banner = root.find('BANNER')
        banners = root.find('BANNERS')
        if banner:
            self.banners = (_banner_url(banner.text),)
        elif banners:
            self.banners = [_banner_url(elem.text) for elem in banners]

        freedom = root.find('FREEDOM')
        if freedom:
            self.freedom = Freedom(
                civilrights=freedom.find('CIVILRIGHTS').text,
                economy=freedom.find('ECONOMY').text,
                politicalfreedom=freedom.find('POLITICALFREEDOM').text
            )
        
        freedomscores = root.find('FREEDOMSCORES')
        if freedomscores:
            self.freedomscores = Freedom(
                civilrights=int(freedomscores.find('CIVILRIGHTS').text),
                economy=int(freedomscores.find('ECONOMY').text),
                politicalfreedom=int(freedomscores.find('POLITICALFREEDOM').text)
            )
        
        govt = root.find('GOVT')
        if govt:
            self.govt = Govt(
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
            )
        
        deaths = root.find('DEATHS')
        if deaths:
            self.deaths = {elem.get('type'): float(elem.text)
                           for elem in deaths.findall('DEATH')}
        
        dispatchlist = root.find('DISPATCHLIST') or []
        self.dispatchlist = {
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
            for elem in dispatchlist
        }
        
        endorsements = root.find('ENDORSEMENTS')
        if endorsements:
            if endorsements.text:
                self.endorsements = endorsements.text.split(',')
            else:
                self.endorsements = []
        
        legislation = root.find('LEGISLATION')
        if legislation:
            self.legislation = [elem.text for elem in legislation]
        
        sectors = root.find('SECTORS')
        if sectors:
            self.sectors = Sectors(
                blackmarket=float(sectors.find('BLACKMARKET').text),
                government=float(sectors.find('GOVERNMENT').text),
                industry=float(sectors.find('INDUSTRY').text),
                public=float(sectors.find('PUBLIC').text)
            )



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


