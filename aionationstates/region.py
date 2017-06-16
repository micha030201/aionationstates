from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    EmbassyPostingRights, AppointedRegionalOfficer, RegionalOfficer,
    Embassies, RegionZombie)
from aionationstates.session import Session, api_query
from aionationstates.shards import Census


class Region(Census, Session):
    def __init__(self, id):
        self.id = normalize(id)

    def _call_api(self, params, *args, **kwargs):
        params['region'] = self.id
        return super()._call_api(*args, params=params, **kwargs)


    @api_query('name')
    def name(root):
        return root.find('NAME').text

    @api_query('flag')
    def flag(root):
        return root.find('FLAG').text

    @api_query('factbook')
    def factbook(root):
        return root.find('FACTBOOK').text  # TODO encoding mess

    @api_query('power')
    def power(root):
        return root.find('POWER').text

    @api_query('delegatevotes')
    def delegatevotes(root):
        return int(root.find('DELEGATEVOTES').text)

    @api_query('numnations')
    def numnations(root):
        return int(root.find('NUMNATIONS').text)

    @api_query('foundedtime')
    def founded(root):
        return timestamp(root.find('FOUNDEDTIME'))

    @api_query('nations')
    def nations(root):
        text = root.find('NATIONS').text
        return text.split(':') if text else ()

    @api_query('embassies')
    def embassies(root):
        Embassies(root.find('EMBASSIES'))

    @api_query('embassyrmb')
    def embassyrmb(root):
        EmbassyPostingRights[root.find('EMBASSYRMB')]

    @api_query('delegate', 'delegateauth')
    def delegate(root):
        nation = root.find('DELEGATE').text
        if nation == '0':  # No delegate
            return None
        return RegionalOfficer(
            nation=nation,
            authority=root.find('DELEGATEAUTH').text,
            office='WA Delegate'
        )

    @api_query('founder', 'founderauth')
    def founder(root):
        nation = root.find('FOUNDER').text
        if nation == '0':  # No founder, it's a GCR
            return None
        return RegionalOfficer(
            nation=nation,
            authority=root.find('FOUNDERAUTH').text,
            office='Founder'
        )

    @api_query('officers')
    def officers(root):
        officers = sorted(
            root.find('OFFICERS'),
            # I struggle to say what else this tag would be useful for.
            key=lambda elem: int(elem.find('ORDER').text)
        )
        return [AppointedRegionalOfficer(elem) for elem in officers]

    @api_query('tags')
    def tags(root):
        return [elem.text for elem in root.find('TAGS')]

    @api_query('zombie')
    def zombie(root):
        return RegionZombie(root.find('ZOMBIE'))

    # TODO: history, messages


