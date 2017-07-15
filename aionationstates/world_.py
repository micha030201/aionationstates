from aionationstates.session import Session, api_query
from aionationstates.types import Dispatch
from aionationstates.shards import Census
from aionationstates.ns_to_human import dispatch_categories

# Needed for type annotations
from typing import List
from aionationstates.session import ApiQuery


class World(Census, Session):
    """Interface to the NationStates World API.  Don't create this
    object yourself, instead use ``aionationstates.world``.
    """
    def regionsbytag(self, *tags: str) -> ApiQuery[List[str]]:
        """All regions belonging to any of the named tags.  Tags can be
        preceded by a ``-`` to select regions without that tag.
        """
        if len(tags) > 10:
            raise ValueError('You can specify up to 10 tags')
        if not tags:
            raise ValueError('No tags specified')
        # We don't check for invalid tags here because the behaviour is
        # fairly intuitive - quering for a non-existent tag returns no
        # regions, excluding it returns all of them.
        @api_query('regionsbytag', tags=','.join(tags))
        async def result(_, root):
            text = root.find('REGIONS').text
            return text.split(',') if text else []
        return result(self)

    def dispatch(self, id: int) -> ApiQuery[Dispatch]:
        """Dispatch by id.  Primarily useful for getting dispatch
        texts, as this is the only way to do so.
        """
        @api_query('dispatch', id=str(id))
        async def result(_, root):
            return Dispatch(root.find('DISPATCH'))
        return result(self)

    def dispatchlist(self, *, author: str = None, category: str = None,
                     subcategory: str = None, sort: str = 'new'
                     ) -> ApiQuery[List[Dispatch]]:
        """Find dispatches by certain criteria.

        Parameters:
            author: Nation authoring the dispatch.
            category: Dispatch's primary category.
            subcategory: Dispatch's secondary category.
            sort: Sort order, 'new' or 'best'.
        """
        params = {'sort': sort}
        if author:
            params['dispatchauthor'] = author
        # Here we do need to ensure that our categories are valid, cause
        # NS just ignores the categories it doesn't recognise and returns
        # whatever it feels like.
        if category and subcategory:
            if (category not in dispatch_categories or
                    subcategory not in dispatch_categories[category]):
                raise ValueError('Invalid category/subcategory')
            params['dispatchcategory'] = f'{category}:{subcategory}'
        elif category:
            if category not in dispatch_categories:
                raise ValueError('Invalid category')
            params['dispatchcategory'] = category

        @api_query('dispatchlist', **params)
        async def result(_, root):
            return [
                Dispatch(elem)
                for elem in root.find('DISPATCHLIST')
            ]
        return result(self)


world = World()

