import aionationstates.session


class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self.items()))


def request(method, **kwargs):
    kwargs = HashableDict(
        (key, HashableDict(value))
        for key, value in kwargs.items()
    )
    return (method, kwargs)


def get(params):
    return request('GET', params=params)


def post(data):
    return request('POST', data=data)


def response(text, *, status=None, url=None,
             headers=None, cookies=None):
    return aionationstates.session.RawResponse(
        text=text, status=status, url=url,
        headers=headers, cookies=cookies
    )


class SessionTestMixin:
    def __init__(self, *args, **kwargs):
        self._responses = {}
        super().__init__(*args, **kwargs)

    async def _base_call_api(self, method, **kwargs):
        r = request(method=method, **kwargs)
        return self._responses[r]
