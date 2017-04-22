from aionationstates.api.Shards import (
    CensusShard, DispatchlistShard, StandardShardCases)


class World(CensusShard, DispatchlistShard, StandardShardCases):

    # TODO: dispatchlist parameters, regionsbytag parameters

    STR_CASES = {'featuredregion'}
    INT_CASES = {'numnations'}
    LIST_CASES = {'newnations', 'regions', 'regionsbytag'}


