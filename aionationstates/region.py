# Needed for type annotations
from typing import Optional

from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    EmbassyPostingRights, Officer, Authority,
    Embassies, Zombie)
from aionationstates.session import Session, api_query
from aionationstates.shards import Census


class Region(Census, Session):
    def __init__(self, name):
        self.id = normalize(name)

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
        return Embassies(root.find('EMBASSIES'))

    @api_query('embassyrmb')
    async def embassyrmb(self, root) -> EmbassyPostingRights:
        """Posting rights for members the of embassy regions."""
        return EmbassyPostingRights.from_ns(root.find('EMBASSYRMB').text)

    @api_query('delegate')
    async def delegate(self, root) -> Optional[str]:
        """Regional World Assembly Delegate.  ``None`` if the region
        has no delegate.
        """
        nation = root.find('DELEGATE').text  # TODO normalize
        if nation == '0':
            return None
        return nation

    @api_query('delegateauth')
    async def delegateauth(self, root) -> Authority:
        """Regional World Assembly Delegate's authority.  Always set,
        no matter if the region has a delegate or not.
        """

        return Authority.from_ns(root.find('DELEGATEAUTH').text)

    @api_query('founder')
    async def founder(self, root) -> Optional[str]:
        """Regional Founder.  Returned even if the nation has ceased to
        exist.  ``None`` if the region is Game-Created and doesn't have
        a founder.
        """
        nation = root.find('FOUNDER').text  # TODO normalize
        if nation == '0':
            return None
        return nation

    @api_query('founderauth')
    async def founderauth(self, root) -> Authority:
        """Regional Founder's authority.  Always set,
        no matter if the region has a founder or not.
        """
        return Authority.from_ns(root.find('FOUNDERAUTH').text)

    @api_query('officers')
    async def officers(self, root):
        officers = sorted(
            root.find('OFFICERS'),
            # I struggle to say what else this tag would be useful for.
            key=lambda elem: int(elem.find('ORDER').text)
        )
        return [Officer(elem) for elem in officers]

    @api_query('tags')
    async def tags(self, root):
        return [elem.text for elem in root.find('TAGS')]

    @api_query('zombie')
    async def zombie(self, root) -> Zombie:
        return Zombie(root.find('ZOMBIE'))

    # TODO: history, messages


