# TODO slots?

from contextlib import suppress
from collections import namedtuple

from aionationstates.ns_to_human import census_info


class CensusScale:
    def __init__(self, elem):
        self.info = census_info[int(elem.get('id'))]


class CensusScaleCurrent(CensusScale):
    def __init__(self, elem):
        super().__init__(elem)
        # For recently-founded nations (and maybe in other cases as well, who
        # knows) the ranks & percentages may not show up even if requested.
        self.score = self.rank = self.prank = self.rrank = self.prrank = None
        with suppress(AttributeError, TypeError):
            self.score = float(elem.find('SCORE').text)
        with suppress(AttributeError, TypeError):
            self.rank = int(elem.find('RANK').text)
        with suppress(AttributeError, TypeError):
            self.prank = float(elem.find('PRANK').text)
        with suppress(AttributeError, TypeError):
            self.rrank = int(elem.find('RRANK').text)
        with suppress(AttributeError, TypeError):
            self.prrank = float(elem.find('PRRANK').text)


class CensusPoint:
    def __init__(self, elem):
        super().__init__(elem)
        self.timestamp = int(elem.find('TIMESTAMP').text)
        self.score = float(elem.find('SCORE').text)


class CensusScaleHistory(CensusScale):
    def __init__(self, elem):
        super().__init__(elem)
        self.history = [CensusPoint(sub_elem) for sub_elem in elem]


class DispatchThumbnail:
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


class Dispatch(DispatchThumbnail):
    def __init__(self, elem):
        super().__init__(elem)
        self.text = elem.find('TEXT').text


class PollOption:
    def __init__(self, elem):
        self.text = point.find('TIMESTAMP').text
        self.timestamp = int()
        self.score = float(point.find('SCORE').text)


