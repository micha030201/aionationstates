import pytest

import utils
import aionationstates


class Nation(utils.SessionTestMixin, aionationstates.Nation):
    pass


@pytest.mark.asyncio
async def test_name():
    nation = Nation('testLandia')
    nation._responses = {
        utils.request({'nation': 'testlandia', 'q': 'name'}):
        utils.response('''
        <NATION id="testlandia">
            <NAME>Testlandia</NAME>
        </NATION>
        ''')
    }
    name = await nation.name()
    assert name == 'Testlandia'
