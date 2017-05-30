from aionationstates.session import Session
from aionationstates.types import Dispatch, DispatchThumbnail
from aionationstates.shards import Census
from aionationstates.ns_to_human import dispatch_categories

class World(Census, Session):

    # TODO: regionsbytag parameters

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


