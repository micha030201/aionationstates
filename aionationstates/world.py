import xml.etree.ElementTree as ET

from aionationstates.session import Session
from aionationstates.shards import (
    CensusShard, DispatchlistShard, StandardShardCases)


class Dispatch(Session):
    def __init__(self, elem):
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text
        self.author = elem.find('AUTHOR').text
        self.category = elem.find('CATEGORY').text
        self.subcategory = elem.find('SUBCATEGORY').text
        self.created = int(elem.find('CREATED').text)
        self.edited = int(elem.find('EDITED').text)
        self.views = int(elem.find('VIEWS').text)
        self.score = int(elem.find('SCORE').text)
        text_elem = elem.find('TEXT')
        self.text = text_elem.text if text_elem else None

    async def update(self):
        params = {
            'q': 'dispatch',
            'dispatchid': self.id
        }
        resp = await self.call_api(params=params)
        root = ET.fromstring(resp.text)
        self.__init__(root.find('WORLD').find('DISPATCH'))


class World(CensusShard, DispatchlistShard, StandardShardCases):

    # TODO: dispatchlist parameters, regionsbytag parameters

    STR_CASES = {'featuredregion'}
    INT_CASES = {'numnations'}
    LIST_CASES = {'newnations', 'regions', 'regionsbytag'}


