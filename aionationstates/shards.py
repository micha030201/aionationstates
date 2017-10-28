"""Interfaces to shards shared between APIs. Designed to be mixed in
with Session, otherwise useless."""

# TODO: happenings (region history as well?), censusranks, wabadges

from aionationstates.types import CensusScaleCurrent, CensusScaleHistory
from aionationstates.happenings import UnrecognizedHappening
from aionationstates.session import api_query


class Census:
    def census(self, *scales):
        """Current World Census data.

        By default returns data on today's featured World Census
        scale, use arguments to get results on specific scales.  In
        order to request data on all scales at once you can do
        ``x.census(*range(81))``.

        Parameters
        ----------
        scales : int
            World Census scales, integers between 0 and 80.

        Returns
        -------
        :class:`ApiQuery` of a list of :class:`CensusScaleCurrent` objects
        """
        params = {'mode': 'score+rank+rrank+prank+prrank'}
        if scales:
            params['scale'] = '+'.join(str(x) for x in scales)
        @api_query('census', **params)
        async def result(_, root):
            return [
                CensusScaleCurrent(scale_elem)
                for scale_elem in root.find('CENSUS')
            ]
        return result(self)


    def censushistory(self, *scales):
        """Historical World Census data.

        Was split into its own method for the sake of simplicity and
        intuitiveness when combinind shards.

        By default returns data on today's featured World Census
        scale, use arguments to get results on specific scales.  In
        order to request data on all scales at once you can do
        ``x.censushistory(*range(81))``.

        Returns data for the entire length of history NationStates
        stores.  There is no way to override that.

        Parameters
        ----------
        scales : int
            World Census scales, integers between 0 and 80.

        Returns
        -------
        :class:`ApiQuery` of a list of :class:`CensusScaleHistory` objects
        """
        params = {'mode': 'history'}
        if scales:
            params['scale'] = '+'.join(str(x) for x in scales)
        @api_query('census', **params)
        async def result(_, root):
            return [
                CensusScaleHistory(scale_elem)
                for scale_elem in root.find('CENSUS')
            ]


class Happenings:
    @api_query('happenings')
    async def happenings(self, root):
        """Get the happenings of the nation or region, archived on its
        page.  Newest to oldest.

        Happenings are not parsed because they are different from
        the ones in the normal feed and I see no practical use-cases
        for having these parsed as well.

        Returns
        -------
        an :class:`ApiQuery` of a list of \
        :class:`happenings.UnrecognizedHappening` objects
        """
        return [UnrecognizedHappening(elem) for elem in root.find('HAPPENINGS')]
