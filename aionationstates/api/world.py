from collections import namedtuple
import xml.etree.ElementTree as ET

from aionationstates.utils import normalize
from aionationstates.session import Session
from aionationstates.api.mixins import (CensusMixin, DispatchlistMixin,
    StandardCasesMixin)

class World(Session, CensusMixin, DispatchlistMixin, StandardCasesMixin):
    async def shards(self, *shards):
        shards = set(shards)
        params = {'q': shards.copy()}
        if 'census' in shards:
            params['scale'] = 'all'
            params['mode'] = 'score+rank+rrank+prank+prrank'
        elif 'censushistory' in shards:
            params['q'].remove('censushistory')
            params['q'].add('census')
            params['scale'] = 'all'
            params['mode'] = 'history'
        params['q'] = '+'.join(params['q'])
        resp = await self.call_api(params=params)
        return dict(self._parse(ET.fromstring(resp.text), shards))

    async def shard(self, shard):
        return (await self.shards(shard))[shard]

    # TODO: dispatchlist parameters, regionsbytag parameters

    STR_CASES = {'featuredregion'}
    INT_CASES = {'numnations'}
    LIST_CASES = {'newnations', 'regions', 'regionsbytag'}

    def _parse(self, root, args):
        yield from super()._parse(root, args)
        
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
        # TODO: 
