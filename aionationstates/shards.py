"""Interfaces to shards shared between APIs."""

# TODO: happenings (region history as well), nations, poll, censusranks, wabadges, zombie


from aionationstates.request import ApiRequest


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


