from aionationstates.shards import (
    CensusShard, Dispatchlist, StandardShardCases)


class World(Dispatchlist, CensusShard, StandardShardCases):

    # TODO: dispatchlist parameters, regionsbytag parameters

    STR_CASES = {'featuredregion'}
    INT_CASES = {'numnations'}
    LIST_CASES = {'newnations', 'regions', 'regionsbytag'}


