from collections import namedtuple
import xml.etree.ElementTree as ET


class ApiRequest:
    def __init__(self, *, session, result, q, params=None):
        self.session = session
        self.results = [result]
        self.q = {q}
        self.params = params or {}

    def __await__(self):
        return self._wrap()

    async def _wrap(self):
        self.params['q'] = '+'.join(self.q)
        resp = await self.session.call_api(self.params)
        root = ET.fromstring(resp.text)
        results = tuple(result(root) for result in self.results)
        return results[0] if len(results) == 1 else results

    def __add__(self, other):
        assert len(self.q & other.q) == 0
        assert len(set(self.params) & set(other.params)) == 0

        self.q |= other.q
        self.params.update(other.params)
        self.results += other.results
        return self
