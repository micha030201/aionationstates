# TODO slots?

from contextlib import suppress
from collections import namedtuple

from aionationstates.ns_to_human import census_info


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


