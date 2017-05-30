from aionationstates.session import Session
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
        params = {'tags': ','.join(tags)}
        def result(root):
            text = root.find('REGIONS').text
            return text.split(',') if text else ()
        return self._compose_api_request(
            q='regionsbytag', params=params, result=result)

    def dispatch(self, id):
        return self._compose_api_request(
            q='dispatch', params={'dispatchid': id},
            result=lambda root: Dispatch(root.find('DISPATCH'))
        )

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

        def result(root):
            return [
                DispatchThumbnail(elem)
                for elem in root.find('DISPATCHLIST')]
        return self._compose_api_request(
            q='dispatchlist', params=params, result=result)


