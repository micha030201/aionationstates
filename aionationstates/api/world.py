from aionationstates.session import Session
from aionationstates.api.mixins import (CensusMixin, DispatchlistMixin,
    StandardCasesMixin, ShardMixin)


class World(Session, CensusMixin, DispatchlistMixin, StandardCasesMixin,
        ShardMixin):

    # TODO: dispatchlist parameters, regionsbytag parameters

    STR_CASES = {'featuredregion'}
    INT_CASES = {'numnations'}
    LIST_CASES = {'newnations', 'regions', 'regionsbytag'}

    def _parse(self, root, args):
        yield from super()._parse(root, args)
        
        if 'dispatch' in args:
            dispatch = root.find('DISPATCH')
            yield (
                'dispatch',
                Dispatch(
                    id=int(dispatch.get('id')),
                    title=dispatch.find('TITLE').text,
                    author=dispatch.find('AUTHOR').text,
                    category=dispatch.find('CATEGORY').text,
                    subcategory=dispatch.find('SUBCATEGORY').text,
                    created=int(dispatch.find('CREATED').text),
                    edited=int(dispatch.find('EDITED').text),
                    views=int(dispatch.find('VIEWS').text),
                    score=int(dispatch.find('SCORE').text),
                    text=dispatch.find('TEXT').text
                )
            )


