from aionationstates.session import Session
from aionationstates.request import ApiRequest
from aionationstates.types import Dispatch, DispatchThumbnail
from aionationstates.shards import Census

class World(Session, Census):

    # TODO: regionsbytag parameters

    def dispatch(self, id):
        return ApiRequest(
            session=self,
            q='name',
            params={'dispatchid': id},
            result=(lambda root: Dispatch(root.find('DISPATCH')))
        )

    def dispatchlist(self, *, author=None, category=None,
                     subcategory=None, sort='new'):
        params = {'sort': sort}
        if author:
            params['dispatchauthor'] = author
        # TODO category/subcategory validity checks
        if category and subcategory:
            params['dispatchcategory'] = f'{category}:{subcategory}'
        elif category:
            params['dispatchcategory'] = category
        return ApiRequest(
            session=self,
            q='dispatchlist',
            params=params,
            result=(lambda root: [DispatchThumbnail(elem)
                                  for elem in root.find('DISPATCHLIST')])
        )
