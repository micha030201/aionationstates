"""Interfaces to shards shared between APIs. Designed to be mixed in
with Session, otherwise useless."""

# TODO: happenings (region history as well?), poll, censusranks, wabadges


from aionationstates.types import CensusScaleCurrent, CensusScaleHistory
from aionationstates.session import api_query

class Census:
    def census(self, scale=None):
        params = {'mode': 'score+rank+rrank+prank+prrank'}
        if scale:
            params['scale'] = _scale_to_str(scale)
        @api_query('census', **params)
        def result(root):
            return [
                CensusScaleCurrent(scale_elem)
                for scale_elem in root.find('CENSUS')
            ]
        return result(self)


    def censushistory(self, scale=None):  # TODO to, from?
        params = {'mode': 'history'}
        if scale:
            params['scale'] = _scale_to_str(scale)
        @api_query('census', **params)
        def result(root):
            return [
                CensusScaleHistory(scale_elem)
                for scale_elem in root.find('CENSUS')
            ]


def _scale_to_str(scale):
    if type(scale) is str:
        return scale
    elif type(scale) is int:
        return str(scale)
    else:
        return '+'.join(str(x) for x in scale)


