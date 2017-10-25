import xml.etree.ElementTree as ET

import pytest

from aionationstates import happenings


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
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Move
    assert h.nation.id == 'testlandia'
    assert h.region_from.id == 'the_east_pacific'
    assert h.region_to.id == 'the_north_pacific'


def test_founding(happening_elem):
    t = '@@testlandia@@ was founded in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Founding
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_cte(happening_elem):
    t = '@@testlandia@@ ceased to exist in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.CTE
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_legislation(happening_elem):
    t = 'Following new legislation in @@testlandia@@, euthanasia is legal.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Legislation
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'euthanasia is legal'


def test_flag(happening_elem):
    t = '@@testlandia@@ altered its national flag.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.FlagChange
    assert h.nation.id == 'testlandia'


def test_wa_category(happening_elem):
    t = '@@testlandia@@ was reclassified from "Left-Leaning College State" to "Inoffensive Centrist Democracy".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.CategoryChange
    assert h.nation.id == 'testlandia'
    assert h.category_before == 'Left-Leaning College State'
    assert h.category_after == 'Inoffensive Centrist Democracy'


def test_settings(happening_elem):
    t = '@@testlandia@@ changed its national motto to "Test arhgHsefv".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': 'Test arhgHsefv'}


def test_settings_multiple(happening_elem):
    t = ('@@testlandia@@ changed its national currency to "wef erkjf",'
         ' its demonym adjective to "qwdqsIO ni",'
         ' and its demonym plural to "ubuUuu ju".')
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {
        'currency': 'wef erkjf',
        'demonym adjective': 'qwdqsIO ni',
        'demonym plural': 'ubuUuu ju'
    }


def test_settings_encoding_issues(happening_elem):
    t = '@@testlandia@@ changed its national motto to "&#135;&#135;&#135;&#135;&#135;&#135;".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': '‡‡‡‡‡‡‡‡‡'}


def test_banner_create(happening_elem):
    t = '@@testlandia@@ created a custom banner.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.BannerCreation
    assert h.nation.id == 'testlandia'


def test_dispatch_publish(happening_elem):
    t = '@@testlandia@@ published "<a href="page=dispatch/id=100000">Testington</a>" (Factbook: Military).'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DispatchPublication
    assert h.nation.id == 'testlandia'
    assert h.title == 'Testington'
    assert h.category == 'Factbook'
    assert h.subcategory == 'Military'
    assert h.dispatch_id == 100000
    #assert h.dispatch == TODO should be an ApiQuery


def test_dispatch_publish_unicode(happening_elem):
    t = '@@testlandia@@ published "<a href="page=dispatch/id=100000">&#135;&#135;&#135;&#135;&#135;&#135; &lt;&gt;& &#93;&#93;&gt;"&quot;</a>" (Factbook: Military).'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DispatchPublication
    assert h.nation.id == 'testlandia'
    assert h.title == '‡‡‡‡‡‡‡‡‡ <>& ]]>""'
    assert h.category == 'Factbook'
    assert h.subcategory == 'Military'
    assert h.dispatch_id == 100000


def test_wa_apply(happening_elem):
    t = '@@testlandia@@ applied to join the World Assembly.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.WorldAssemblyApplication
    assert h.nation.id == 'testlandia'


def test_wa_admit(happening_elem):
    t = '@@testlandia@@ was admitted to the World Assembly.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.WorldAssemblyAdmission
    assert h.nation.id == 'testlandia'


def test_wa_resign(happening_elem):
    t = '@@testlandia@@ resigned from the World Assembly.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.WorldAssemblyResignation
    assert h.nation.id == 'testlandia'


def test_delegate_remove(happening_elem):
    t = '@@testlandia@@ lost WA Delegate status in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DelegateChange
    assert h.new_delegate is None
    assert h.old_delegate.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_delegate_install(happening_elem):
    t = '@@testlandia@@ became WA Delegate of %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DelegateChange
    assert h.new_delegate.id == 'testlandia'
    assert h.old_delegate is None
    assert h.region.id == 'the_east_pacific'


def test_delegate_change(happening_elem):
    t = '@@testlandia@@ seized the position of %%the_east_pacific%% WA Delegate from @@aidnaltset@@.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DelegateChange
    assert h.new_delegate.id == 'testlandia'
    assert h.old_delegate.id == 'aidnaltset'
    assert h.region.id == 'the_east_pacific'
