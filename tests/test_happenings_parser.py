import xml.etree.ElementTree as ET

from aionationstates import happenings


def happening_elem(text):
    return ET.fromstring(f"""
        <EVENT id="172176017">
            <TIMESTAMP>1508613622</TIMESTAMP>
            <TEXT><![CDATA[{text}]]></TEXT>
        </EVENT>
    """)


def test_move():
    t = '@@testlandia@@ relocated from %%the_east_pacific%% to %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Move
    assert h.nation.id == 'testlandia'
    assert h.region_from.id == 'the_east_pacific'
    assert h.region_to.id == 'the_north_pacific'


def test_founding():
    t = '@@testlandia@@ was founded in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Founding
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_cte():
    t = '@@testlandia@@ ceased to exist in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.CTE
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_legislation():
    t = 'Following new legislation in @@testlandia@@, euthanasia is legal.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Legislation
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'euthanasia is legal'


def test_legislation_html():
    t = 'Following new legislation in @@testlandia@@, all new &quot;spies&quot; are fifteen-year-old acne-ridden kids on computers.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Legislation
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'all new "spies" are fifteen-year-old acne-ridden kids on computers'


def test_flag():
    t = '@@testlandia@@ altered its national flag.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.FlagChange
    assert h.nation.id == 'testlandia'


def test_wa_category():
    t = '@@testlandia@@ was reclassified from "Left-Leaning College State" to "Inoffensive Centrist Democracy".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.CategoryChange
    assert h.nation.id == 'testlandia'
    assert h.category_before == 'Left-Leaning College State'
    assert h.category_after == 'Inoffensive Centrist Democracy'


def test_settings():
    t = '@@testlandia@@ changed its national motto to "Test arhgHsefv".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': 'Test arhgHsefv'}


def test_settings_multiple():
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


def test_settings_encoding_issues():
    t = '@@testlandia@@ changed its national motto to "&#135;&#135;&#135;&#135;&#135;&#135;".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': '‡‡‡‡‡‡‡‡‡'}


def test_banner_create():
    t = '@@testlandia@@ created a custom banner.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.BannerCreation
    assert h.nation.id == 'testlandia'


def test_dispatch_publish():
    t = '@@testlandia@@ published "<a href="page=dispatch/id=100000">Testington</a>" (Factbook: Military).'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DispatchPublication
    assert h.nation.id == 'testlandia'
    assert h.title == 'Testington'
    assert h.category == 'Factbook'
    assert h.subcategory == 'Military'
    assert h.dispatch_id == 100000
    #assert h.dispatch == TODO should be an ApiQuery


def test_dispatch_publish_unicode():
    t = '@@testlandia@@ published "<a href="page=dispatch/id=100000">&#135;&#135;&#135;&#135;&#135;&#135; &lt;&gt;& &#93;&#93;&gt;"&quot;</a>" (Factbook: Military).'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DispatchPublication
    assert h.nation.id == 'testlandia'
    assert h.title == '‡‡‡‡‡‡‡‡‡ <>& ]]>""'
    assert h.category == 'Factbook'
    assert h.subcategory == 'Military'
    assert h.dispatch_id == 100000


def test_wa_apply():
    t = '@@testlandia@@ applied to join the World Assembly.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.WorldAssemblyApplication
    assert h.nation.id == 'testlandia'


def test_wa_admit():
    t = '@@testlandia@@ was admitted to the World Assembly.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.WorldAssemblyAdmission
    assert h.nation.id == 'testlandia'


def test_wa_resign():
    t = '@@testlandia@@ resigned from the World Assembly.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.WorldAssemblyResignation
    assert h.nation.id == 'testlandia'


def test_delegate_remove():
    t = '@@testlandia@@ lost WA Delegate status in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DelegateChange
    assert h.new_delegate is None
    assert h.old_delegate.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_delegate_install():
    t = '@@testlandia@@ became WA Delegate of %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DelegateChange
    assert h.new_delegate.id == 'testlandia'
    assert h.old_delegate is None
    assert h.region.id == 'the_east_pacific'


def test_delegate_change():
    t = '@@testlandia@@ seized the position of %%the_east_pacific%% WA Delegate from @@aidnaltset@@.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.DelegateChange
    assert h.new_delegate.id == 'testlandia'
    assert h.old_delegate.id == 'aidnaltset'
    assert h.region.id == 'the_east_pacific'


def test_embassy_propose():
    t = '@@testlandia@@ proposed constructing embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyConstructionRequest
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_agree():
    t = '@@testlandia@@ agreed to construct embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyConstructionConfirmation
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_order_closure():
    t = '@@testlandia@@ ordered the closure of embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyClosureOrder
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_request_withdraw():
    t = '@@testlandia@@ withdrew a request for embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyConstructionRequestWithdrawal
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_abort_construction():
    t = '@@testlandia@@ aborted construction of embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyConstructionAbortion
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_established():
    t = 'Embassy established between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyEstablishment
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_cancelled():
    t = 'Embassy cancelled between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EmbassyCancellation
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_endorse():
    t = '@@testlandia@@ endorsed @@aidnaltset@@.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.Endorsement
    assert h.endorser.id == 'testlandia'
    assert h.endorsee.id == 'aidnaltset'


def test_unendorse():
    t = '@@testlandia@@ withdrew its endorsement from @@aidnaltset@@.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.EndorsementWithdrawal
    assert h.endorser.id == 'testlandia'
    assert h.endorsee.id == 'aidnaltset'


def test_poll_create():
    t = '@@testlandia@@ created a new poll in %%the_east_pacific%%: "qwerty".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.PollCreation
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'
    assert h.title == 'qwerty'


def test_poll_create_html():
    t = '@@testlandia@@ created a new poll in %%the_east_pacific%%: "&lt;&gt;&amp; &gt; &quot;. &quot;. &amp;quot;.".'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.PollCreation
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'
    assert h.title == '<>& > ". ". &quot;.'


def test_poll_delete():
    t = '@@testlandia@@ deleted a regional poll in %%the_east_pacific%%.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.PollDeletion
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_zombie_cleanse():
    t = '@@testlandia@@ was cleansed by a Level 5 Invasion Tactical Zombie Elimination Squad from @@landtestia@@, killing 195 million zombies.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.ZombieKillAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 195
    assert h.weapon == 'Level 5 Invasion Tactical Zombie Elimination Squad'


def test_zombie_ravage():
    t = '@@testlandia@@ was ravaged by a Zombie Thing Horde from @@landtestia@@, infecting 70 million survivors.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.ZombieInfectAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 70
    assert h.weapon == 'Zombie Thing Horde'


def test_zombie_cure():
    t = '@@testlandia@@ was struck by a Mk I (Immunizer) Cure Missile from @@landtestia@@, curing 5 million infected.'
    h = happenings.process(happening_elem(t))
    assert type(h) == happenings.ZombieCureAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 5
    assert h.weapon == 'Mk I (Immunizer) Cure Missile'
