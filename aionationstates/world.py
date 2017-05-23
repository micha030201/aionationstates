from aionationstates.shards import (
    CensusShard, Dispatch, Dispatchlist, StandardShardCases)


class World(Dispatchlist, CensusShard, StandardShardCases):

    # TODO: regionsbytag parameters

    STR_CASES = {'featuredregion'}
    INT_CASES = {'numnations'}
    LIST_CASES = {'newnations', 'regions', 'regionsbytag'}

    async def dispatch(self, id):
        d = Dispatch(id=id)
        await d.update()
        return d


