import xml.etree.ElementTree as ET

from nkvd.nationstates.session import ApiSession, NationSession
from nkvd.nationstates.utils import normalize


class NationShards(ApiSession):
    """A class to access NS Nation API public shards."""
    def __init__(self, nation):
        self.nation = normalize(nation)

    async def get(self, *shards):
        params = {
            'nation': self.nation,
            'q': '+'.join(shards)
        }
        resp = await self.call_api(params=params)
        return dict(self._parse(shards, ET.fromstring(resp.text)))
    
    def _parse(self, shards, xml_root):
        assert xml_root.attrib['id'] == self.nation
        if 'animal' in shards:
            yield ('animal', xml_root.find('ANIMAL').text)
        if 'flag' in shards:
            yield ('flag', xml_root.find('FLAG').text)
        # TODO: finish


