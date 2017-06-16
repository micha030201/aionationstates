from aionationstates.session import Session, api_query
from aionationstates.types import Dispatch, DispatchThumbnail
from aionationstates.shards import Census
from aionationstates.ns_to_human import dispatch_categories

class World(Census, Session):
    def regionsbytag(self, *tags):
        if len(tags) > 10:
            raise ValueError('You can specify up to 10 tags')
        # We don't check for invalid tags here because the behaviour is
        # fairly intuitive - quering for a non-existent tag returns no
        # regions, excluding it returns all of them.
        @api_query('regionsbytag', tags=','.join(tags))
        def result(root):
            text = root.find('REGIONS').text
            return text.split(',') if text else ()
        return result()

    def dispatch(self, id):
        @api_query('dispatch', id=id)
        def result(root):
            return Dispatch(root.find('DISPATCH'))

    def dispatchlist(self, *, author=None, category=None,
                     subcategory=None, sort='new'):
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
        def result(root):
            return [
                DispatchThumbnail(elem)
                for elem in root.find('DISPATCHLIST')
            ]


