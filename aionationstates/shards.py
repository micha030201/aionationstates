"""Interfaces to shards shared between APIs."""

# TODO: happenings (region history as well), nations, poll, censusranks, wabadges, zombie

from contextlib import suppress
import xml.etree.ElementTree as ET
from collections import namedtuple

from aionationstates.ns_to_human import census_info
from aionationstates.session import Session
from aionationstates.request import ApiRequest


class CensusScale:
    def __init__(self, elem):
        self.info = census_info[int(scale.get('id'))]
        self.score = self.rank = self.prank = self.rrank = self.prrank = None
        with suppress(AttributeError, TypeError):
            self.score = float(scale.find('SCORE').text)
        with suppress(AttributeError, TypeError):
            self.rank = int(scale.find('RANK').text)
        with suppress(AttributeError, TypeError):
            self.prank = float(scale.find('PRANK').text)
        with suppress(AttributeError, TypeError):
            self.rrank = int(scale.find('RRANK').text)
        with suppress(AttributeError, TypeError):
            self.prrank = float(scale.find('PRRANK').text)


class CensusPoint:
    def __init__(self, elem):
        self.info = census_info[int(scale.get('id'))]
        self.timestamp = int(point.find('TIMESTAMP').text)
        self.score = float(point.find('SCORE').text)


class Census:
    """
    Inconsistencies:
        census with mode=history was renamed to censushistory.
    """
    def census(self):
        return ApiRequest(
            session=self,
            q='census',
            params={'scale': 'all', 'mode': 'score+rank+rrank+prank+prrank'},
            result=(lambda root: [CensusScale(scale_elem)
                                  for scale_elem in root.find('CENSUS')])
        )

    def censushistory(self):
        return ApiRequest(
            session=self,
            q='census',
            params={'scale': 'all', 'mode': 'history'},
            result=(lambda root: [[CensusHistory(point_elem)
                                   for point_elem in scale_elem]
                                  for scale_elem in root.find('CENSUS')])
        )


class Dispatch(Session):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_elem(cls, elem):
        r = cls()
        r._parse(elem)
        return r

    def _parse(self, elem):
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text
        self.author = elem.find('AUTHOR').text
        self.category = elem.find('CATEGORY').text
        self.subcategory = elem.find('SUBCATEGORY').text
        self.created = int(elem.find('CREATED').text)
        self.edited = int(elem.find('EDITED').text)
        self.views = int(elem.find('VIEWS').text)
        self.score = int(elem.find('SCORE').text)
        with suppress(AttributeError):
            self.text = elem.find('TEXT').text

    async def update(self):
        params = {
            'q': 'dispatch',
            'dispatchid': str(self.id)
        }
        resp = await self.call_api(params=params)
        root = ET.fromstring(resp.text)
        self._parse(root.find('DISPATCH'))


class Dispatchlist(Session):
    """
    Inconsistencies:
        factbooklist was left out as unnecessary. Use dispatchlist.
    """
    async def dispatchlist(self, *, author=None, category=None,
                           subcategory=None, sort='new'):
        params = {'q': 'dispatchlist', 'sort': sort}
        if author:
            params['dispatchauthor'] = author
        if category and subcategory:
            params['dispatchcategory'] = f'{category}:{subcategory}'
        elif category:
            params['dispatchcategory'] = category
        resp = await self.call_api(params=params)
        root = ET.fromstring(resp.text)
        return (Dispatch.from_elem(elem) for elem in root.find('DISPATCHLIST'))


