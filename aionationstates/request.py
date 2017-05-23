from collections import namedtuple
import xml.etree.ElementTree as ET


ApiRequest = namedtuple('ApiRequest', 'results params headers')

class ApiRequestGroup:
    def __init__(self, *, session, result, params, headers=None):
        self.session = session
        self.requests = [
            ApiRequest(
                results=[result],
                params=params,
                headers=headers or {}
            )
        ]

    def __await__(self):
        return self._wrap()

    async def _wrap(self):
        async def gen():
            for results, params, headers in self.requests:
                resp = await self.session.call_api(params, headers=headers)
                root = ET.fromstring(resp.text)
                for result in results:
                    yield result(root)
        results = [result async for result in gen()]
        return results[0] if len(results) == 1 else tuple(results)

    def __add__(self, other):
        # TODO actual request number optimization
        self.requests += other.requests
        return self
