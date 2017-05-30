from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    EmbassyPostingRights, AppointedRegionalOfficer, RegionalOfficer,
    Embassies)
from aionationstates.session import Session
from aionationstates.shards import Census, GeneralCases


class Region(Census, GeneralCases, Session):
    def __init__(self, id):
        self.id = normalize(id)

    def call_api(self, params, *args, **kwargs):
        params['region'] = self.id
        return super().call_api(*args, params=params, **kwargs)

    def name(self): return self._str_case('name')
    def flag(self): return self._str_case('flag')
    def factbook(self): return self._str_case('factbook')
    def power(self): return self._str_case('power')

    def delegatevotes(self): return self._int_case('delegatevotes')
    def numnations(self): return self._int_case('numnations')
    population = numnations  # TODO it this necessary?

    def founded(self):
        return self._compose_api_request(
            q='foundedtime',
            result=lambda root: timestamp(root.find('FOUNDEDTIME')))

    def nations(self):
        def result(root):
            text = root.find('NATIONS').text
            return text.split(':') if text else ()
        return self._compose_api_request(q='nations', result=result)

    def embassies(self):
        def result(root):
            Embassies(root.find('EMBASSIES'))
        return self._compose_api_request(q='embassies', result=result)

    def embassyrmb(self):
        def result(root):
            EmbassyPostingRights[root.find('EMBASSYRMB')]
        return self._compose_api_request(q='embassyrmb', result=result)

    def delegate(self):
        def result(root):
            nation = root.find('DELEGATE').text
            if nation == '0':  # No delegate
                return None
            return RegionalOfficer(
                nation=nation,
                authority=root.find('DELEGATEAUTH').text,
                office='WA Delegate'
            )
        return self._compose_api_request(
            q='delegate+delegateauth',  # TODO better API for this sorta things
            result=result
        )

    def founder(self):
        def result(root):
            nation = root.find('FOUNDER').text
            if nation == '0':  # No founder, it's a GCR
                return None
            return RegionalOfficer(
                nation=nation,
                authority=root.find('FOUNDERAUTH').text,
                office='Founder'
            )
        return self._compose_api_request(
            q='founder+founderauth',    # TODO better API for this sorta things
            result=result
        )

    def officers(self):
        def result(root):
            officers = sorted(root.find('OFFICERS'),
                              key=lambda elem: int(elem.find('ORDER').text))
            return [AppointedRegionalOfficer(elem) for elem in officers]
        return self._compose_api_request(q='officers', result=result)

    def tags(self):
        def result(root):
            return [elem.text for elem in root.find('TAGS')]
        return self._compose_api_request(q='tags', result=result)

    # TODO: history, messages


