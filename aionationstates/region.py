from collections import namedtuple

from aionationstates.utils import normalize
from aionationstates.shards import CensusShard, StandardShardCases


# TODO: officer authority
Officer = namedtuple('Officer', 'nation office authority time by order')

class Region(CensusShard, StandardShardCases):
    def __init__(self, name):
        self.name = normalize(name)

    def _url_transform(self, params):
        super()._url_transform(params)
        params['region'] = self.name

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


