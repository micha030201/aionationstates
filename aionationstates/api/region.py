from collections import namedtuple

from aionationstates.utils import normalize
from aionationstates.session import Session, AuthSession
from aionationstates.api.mixins import (CensusMixin, StandardCasesMixin,
    ShardMixin)


# TODO: officer authority

Officer = namedtuple('Officer', 'nation office authority time by order')

class Region(Session, CensusMixin, StandardCasesMixin, ShardMixin):
    def __init__(self, region):
        self.region = normalize(region)

    def _url_transform(self, params):
        super()._url_transform(params)
        params['region'] = self.region


    STR_CASES = {
        'name', 'flag', 'founded', 'gavote', 'scvote', 'delegate', 'founder',
        'factbook', 'embassyrmb', 'power', 'founderauth', 'delegateauth'
    }
    INT_CASES = {'foundedtime', 'delegatevotes', 'numnations'}
    LIST_CASES = {'nations'}

    def _parse(self, root, args):
        yield from super()._parse(root, args)
        
        if 'officers' in args:
            yield (
                'officers',
                [Officer(
                     nation=officer.find('NATION').text,
                     office=officer.find('OFFICE').text,
                     authority=officer.find('AUTHORITY').text,
                     time=int(officer.find('TIME').text),
                     by=officer.find('BY').text,
                     order=int(officer.find('ORDER').text)
                 )
                 for officer in root.find('OFFICERS')]
            )
        
        # TODO: embassies, history, messages, tags


