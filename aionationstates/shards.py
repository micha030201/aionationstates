"""Interfaces to shards shared between APIs."""

# TODO: happenings (region history as well?), nations, poll, censusranks, wabadges, zombie


from aionationstates.request import ApiRequest
from aionationstates.types import CensusScaleCurrent, CensusScaleHistory


class Census:
    """
    Inconsistencies:
        census with mode=history was renamed to censushistory.
    """

    def _scale_to_str(self, scale):
        if type(scale) is str:
            return scale
        elif type(scale) is int:
            return str(scale)
        else:
            return '+'.join(str(x) for x in scale)

    def census(self, scale=None):
        params = {'mode': 'score+rank+rrank+prank+prrank'}
        if scale:
            params['scale'] = _scale_to_str(scale)
        return ApiRequest(
            session=self,
            q='census',
            params=params,
            result=(lambda root: [CensusScaleCurrent(scale_elem)
                                  for scale_elem in root.find('CENSUS')])
        )

    def censushistory(self):
        params = {'mode': 'history'}
        if scale:
            params['scale'] = _scale_to_str(scale)
        return ApiRequest(
            session=self,
            q='census',
            params=params,
            result=(lambda root: [CensusScaleHistory(point_elem)
                                  for scale_elem in root.find('CENSUS')])
        )


