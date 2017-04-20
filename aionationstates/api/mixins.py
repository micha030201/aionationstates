# TODO: happenings (region history as well), nations, poll, censusranks, wabadges, zombie

from contextlib import suppress
import xml.etree.ElementTree as ET

from collections import namedtuple
from aionationstates.ns_to_human import census_info


class ShardMixin:
    async def shards(self, *shards):
        shards = set(shards)
        params = {'q': shards.copy()}
        self._url_transform(params)
        params['q'] = '+'.join(params['q'])
        resp = await self.call_api(params=params)
        return dict(self._parse(ET.fromstring(resp.text), shards))

    async def shard(self, shard):
        return (await self.shards(shard))[shard]
    
    def _url_transform(self, params):
        pass
    
    def _parse(self, root, args):
        return ()


class StandardCasesMixin(ShardMixin):
    STR_CASES = INT_CASES = FLOAT_CASES = BOOL_CASES = LIST_CASES = set()
    def _parse(self, root, args):
        yield from super()._parse(root, args)
        for arg in args & self.STR_CASES:
            yield (arg, root.find(arg.upper()).text)
        for arg in args & self.INT_CASES:
            yield (arg, int(root.find(arg.upper()).text))
        for arg in args & self.FLOAT_CASES:
            yield (arg, float(root.find(arg.upper()).text))
        for arg in args & self.BOOL_CASES:
            yield (arg, bool(int(root.find(arg.upper()).text)))
        for arg in args & self.LIST_CASES:
            yield (arg, (root.find(arg.upper()).text
                         .replace(':', ',')  # what is consistency even
                         .split(',')))


CensusScale = namedtuple('CensusScale', 'info score rank prank rrank prrank')
CensusPoint = namedtuple('CensusPoint', 'info timestamp score')

class CensusMixin(ShardMixin):
    """     
    Inconsistencies:
        * census with mode=history was renamed to censushistory.
    """
    def _url_transform(self, params):
        super()._url_transform(params)
        if 'census' in params['q']:
            params['scale'] = 'all'
            params['mode'] = 'score+rank+rrank+prank+prrank'
        elif 'censushistory' in params['q']:
            params['q'].remove('censushistory')
            params['q'].add('census')
            params['scale'] = 'all'
            params['mode'] = 'history'
    
    def _parse(self, root, args):
        yield from super()._parse(root, args)
        if 'censushistory' in args:
            yield (
                'censushistory',
                {int(scale.get('id')):
                 [CensusPoint(
                      info=census_info[int(scale.get('id'))],
                      timestamp=int(point.find('TIMESTAMP').text),
                      score=float(point.find('SCORE').text)
                  ) for point in scale]
                 for scale in root.find('CENSUS')}
            )
        if 'census' in args:
            def make_scale(scale):
                info = census_info[int(scale.get('id'))]
                score = rank = prank = rrank = prrank = None
                with suppress(AttributeError, TypeError):
                    score = float(scale.find('SCORE').text)
                with suppress(AttributeError, TypeError):
                    rank = int(scale.find('RANK').text)
                with suppress(AttributeError, TypeError):
                    prank = float(scale.find('PRANK').text)
                with suppress(AttributeError, TypeError):
                    rrank = int(scale.find('RRANK').text)
                with suppress(AttributeError, TypeError):
                    prrank = float(scale.find('PRRANK').text)
                return CensusScale(info=info, score=score, rank=rank,
                                   prank=prank, rrank=rrank, prrank=prrank)
            yield (
                'census',
                {int(scale.get('id')): make_scale(scale)
                 for scale in root.find('CENSUS')}
            )


Dispatch = namedtuple('Dispatch', ('id title author category subcategory'
                                   ' created edited views score text'))

class DispatchlistMixin(ShardMixin):
    """     
    Inconsistencies:
        * factbooklist was left out as unnecessary. Use dispatchlist.
    """
    def _parse(self, root, args):
        yield from super()._parse(root, args)
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
                    text=None  # TODO: get text coroutine
                )
                for elem in root.find('DISPATCHLIST')
            ])


