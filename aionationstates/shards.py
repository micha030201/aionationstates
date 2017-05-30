"""Interfaces to shards shared between APIs. Designed to be mixed in
with Session, otherwise useless."""

# TODO: happenings (region history as well?), poll, censusranks, wabadges, zombie


from aionationstates.types import CensusScaleCurrent, CensusScaleHistory


class GeneralCases:
    """When the xml tag name is just the capitalised shard name and
    little to no additional processing is required.
    """
    def _str_case(self, q):
        def result(root): return root.find(q.upper()).text
        return self._compose_api_request(q=q, result=result)

    def _int_case(self, q):
        def result(root): return int(root.find(q.upper()).text)
        return self._compose_api_request(q=q, result=result)

    # The rest are uncommon enough to be left out


class Census:
    def census(self, scale=None):
        def result(root):
            return [
                CensusScaleCurrent(scale_elem)
                for scale_elem in root.find('CENSUS')
            ]
        params = {'mode': 'score+rank+rrank+prank+prrank'}
        if scale:
            params['scale'] = _scale_to_str(scale)
        return self._compose_api_request(
            q='census', params=params, result=result)

    def censushistory(self, scale=None):
        def result(root):
            return [
                CensusScaleHistory(scale_elem)
                for scale_elem in root.find('CENSUS')
            ]
        params = {'mode': 'history'}
        if scale:
            params['scale'] = _scale_to_str(scale)
        return self._compose_api_request(
            q='census', params=params, result=result)


def _scale_to_str(self, scale):
    if type(scale) is str:
        return scale
    elif type(scale) is int:
        return str(scale)
    else:
        return '+'.join(str(x) for x in scale)


