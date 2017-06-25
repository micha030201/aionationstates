from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    EmbassyPostingRights, AppointedRegionalOfficer, RegionalOfficer,
    Embassies, RegionZombie)
from aionationstates.session import Session, api_query
from aionationstates.shards import Census


class Region(Census, Session):
    def __init__(self, id, *args, **kwargs):
        self.id = normalize(id)
        super().__init__(*args, **kwargs)

    def _call_api(self, params, *args, **kwargs):
        params['region'] = self.id
        return super()._call_api(*args, params=params, **kwargs)


    @api_query('name')
    async def name(self, root):
        return root.find('NAME').text

    @api_query('flag')
    async def flag(self, root):
        return root.find('FLAG').text

    @api_query('factbook')
    async def factbook(self, root):
        return root.find('FACTBOOK').text  # TODO encoding mess

    @api_query('power')
    async def power(self, root):
        return root.find('POWER').text

    @api_query('delegatevotes')
    async def delegatevotes(self, root):
        return int(root.find('DELEGATEVOTES').text)

    @api_query('numnations')
    async def numnations(self, root):
        return int(root.find('NUMNATIONS').text)

    @api_query('foundedtime')
    async def founded(self, root):
        return timestamp(root.find('FOUNDEDTIME'))

    @api_query('nations')
    async def nations(self, root):
        text = root.find('NATIONS').text
        return text.split(':') if text else ()

    @api_query('embassies')
    async def embassies(self, root):
        Embassies(root.find('EMBASSIES'))

    @api_query('embassyrmb')
    async def embassyrmb(self, root):
        EmbassyPostingRights[root.find('EMBASSYRMB').text]

    @api_query('delegate', 'delegateauth')
    async def delegate(self, root):
        nation = root.find('DELEGATE').text
        if nation == '0':  # No delegate
            return None
        return RegionalOfficer(
            nation=nation,
            authority=root.find('DELEGATEAUTH').text,
            office='WA Delegate'
        )

    @api_query('founder', 'founderauth')
    async def founder(self, root):
        nation = root.find('FOUNDER').text
        if nation == '0':  # No founder, it's a GCR
            return None
        return RegionalOfficer(
            nation=nation,
            authority=root.find('FOUNDERAUTH').text,
            office='Founder'
        )

    @api_query('officers')
    async def officers(self, root):
        officers = sorted(
            root.find('OFFICERS'),
            # I struggle to say what else this tag would be useful for.
            key=lambda elem: int(elem.find('ORDER').text)
        )
        return [AppointedRegionalOfficer(elem) for elem in officers]

    @api_query('tags')
    async def tags(self, root):
        return [elem.text for elem in root.find('TAGS')]

    @api_query('zombie')
    async def zombie(self, root):
        return RegionZombie(root.find('ZOMBIE'))

    # TODO: history, messages


