import xml.etree.ElementTree as ET

import pytest

from aionationstates import happening_types


@pytest.fixture
def happening_elem(request):
    def create_elem(text):
        return ET.fromstring(f"""
            <EVENT id="172176017">
                <TIMESTAMP>1508613622</TIMESTAMP>
                <TEXT><![CDATA[{text}]]></TEXT>
            </EVENT>
        """)
    return create_elem


def test_move(happening_elem):
    t = '@@testlandia@@ relocated from %%the_east_pacific%% to %%the_north_pacific%%.'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.MoveHappening
    assert h.nation.id == 'testlandia'
    assert h.region_from.id == 'the_east_pacific'
    assert h.region_to.id == 'the_north_pacific'


def test_founding(happening_elem):
    t = '@@testlandia@@ was founded in %%the_east_pacific%%.'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.FoundingHappening
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_cte(happening_elem):
    t = '@@testlandia@@ ceased to exist in %%the_east_pacific%%.'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.CTEHappening
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_legislation(happening_elem):
    t = 'Following new legislation in @@testlandia@@, euthanasia is legal.'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.LegislationHappening
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'euthanasia is legal'


def test_flag(happening_elem):
    t = '@@testlandia@@ altered its national flag.'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.FlagChangeHappening
    assert h.nation.id == 'testlandia'


def test_legislation(happening_elem):
    t = '@@testlandia@@ was reclassified from "Left-Leaning College State" to "Inoffensive Centrist Democracy".'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.Wa
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'euthanasia is legal'


def test_settings(happening_elem):
    t = '@@testlandia@@ changed its national motto to "Test arhgHsefv".'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.SettingsChangeHappening
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': 'Test arhgHsefv'}


def test_settings_multiple(happening_elem):
    t = ('@@testlandia@@ changed its national currency to "wef erkjf",'
         ' its demonym adjective to "qwdqsIO ni",'
         ' and its demonym plural to "ubuUuu ju".')
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.SettingsChangeHappening
    assert h.nation.id == 'testlandia'
    assert h.changes == {
        'currency': 'wef erkjf',
        'demonym adjective': 'qwdqsIO ni',
        'demonym plural': 'ubuUuu ju'
    }


def test_settings_encoding_issues(happening_elem):
    t = '@@testlandia@@ changed its national motto to "&#135;&#135;&#135;&#135;&#135;&#135;".'
    h = happening_types.process(happening_elem(t))
    assert type(h) == happening_types.SettingsChangeHappening
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': '‡‡‡‡‡‡‡‡‡'}
