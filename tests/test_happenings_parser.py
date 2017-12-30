import xml.etree.ElementTree as ET

from aionationstates import happenings
from aionationstates import Nation, Region, Authority


def happening_elem(text):
    return ET.fromstring(f"""
        <EVENT id="172176017">
            <TIMESTAMP>1508613622</TIMESTAMP>
            <TEXT><![CDATA[{text}]]></TEXT>
        </EVENT>
    """)


def test_move():
    t = '@@testlandia@@ relocated from %%the_east_pacific%% to %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.Move
    assert h.nation.id == 'testlandia'
    assert h.region_from.id == 'the_east_pacific'
    assert h.region_to.id == 'the_north_pacific'


def test_founding():
    t = '@@testlandia@@ was founded in %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.Founding
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_cte():
    t = '@@testlandia@@ ceased to exist in %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.CTE
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_legislation():
    t = 'Following new legislation in @@testlandia@@, euthanasia is legal.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.Legislation
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'euthanasia is legal'


def test_legislation_html():
    t = 'Following new legislation in @@testlandia@@, all new &quot;spies&quot; are fifteen-year-old acne-ridden kids on <i>computers</i>.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.Legislation
    assert h.nation.id == 'testlandia'
    assert h.effect_line == 'all new &quot;spies&quot; are fifteen-year-old acne-ridden kids on <i>computers</i>'


def test_flag():
    t = '@@testlandia@@ altered its national flag.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.FlagChange
    assert h.nation.id == 'testlandia'


def test_wa_category():
    t = '@@testlandia@@ was reclassified from "Left-Leaning College State" to "Inoffensive Centrist Democracy".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.CategoryChange
    assert h.nation.id == 'testlandia'
    assert h.category_before == 'Left-Leaning College State'
    assert h.category_after == 'Inoffensive Centrist Democracy'


def test_settings():
    t = '@@testlandia@@ changed its national motto to "Test arhgHsefv".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': 'Test arhgHsefv'}


def test_settings_comma():
    t = '@@testlandia@@ changed its national motto to "Test, arhgHsefv".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': 'Test, arhgHsefv'}


def test_settings_multiple():
    t = ('@@testlandia@@ changed its national currency to "wef erkjf",'
         ' its demonym adjective to "qwdqsIO ni",'
         ' and its demonym plural to "ubuUuu ju".')
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {
        'currency': 'wef erkjf',
        'demonym adjective': 'qwdqsIO ni',
        'demonym plural': 'ubuUuu ju'
    }


def test_settings_multiple_comma():
    t = ('@@testlandia@@ changed its national currency to "wef erkjf",'
         ' its demonym adjective to "qwdqsIO ni",'
         ' and its demonym plural to "ubuUuu, ju".')
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {
        'currency': 'wef erkjf',
        'demonym adjective': 'qwdqsIO ni',
        'demonym plural': 'ubuUuu, ju'
    }


def test_settings_multiple2():
    t = '@@testlandia@@ changed its national leader to "the First Grand Consul" and its nation type to "Imperial States".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {
        'leader': 'the First Grand Consul',
        'nation type': 'Imperial States',
    }


def test_settings_encoding_issues():
    t = '@@testlandia@@ changed its national motto to "&#135;&#135;&#135;&#135;&#135;&#135;".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.SettingsChange
    assert h.nation.id == 'testlandia'
    assert h.changes == {'motto': '‡‡‡‡‡‡‡‡‡'}


def test_banner_create():
    t = '@@testlandia@@ created a custom banner.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.BannerCreation
    assert h.nation.id == 'testlandia'


def test_dispatch_publish():
    t = '@@testlandia@@ published "<a href="page=dispatch/id=100000">Testington</a>" (Factbook: Military).'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DispatchPublication
    assert h.nation.id == 'testlandia'
    assert h.title == 'Testington'
    assert h.category == 'Factbook'
    assert h.subcategory == 'Military'
    assert h.dispatch_id == 100000
    #assert h.dispatch == TODO should be an ApiQuery


def test_dispatch_publish_unicode():
    t = '@@testlandia@@ published "<a href="page=dispatch/id=100000">&#135;&#135;&#135;&#135;&#135;&#135; &lt;&gt;& &#93;&#93;&gt;"&quot;</a>" (Factbook: Military).'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DispatchPublication
    assert h.nation.id == 'testlandia'
    assert h.title == '‡‡‡‡‡‡‡‡‡ <>& ]]>""'
    assert h.category == 'Factbook'
    assert h.subcategory == 'Military'
    assert h.dispatch_id == 100000


def test_wa_apply():
    t = '@@testlandia@@ applied to join the World Assembly.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.WorldAssemblyApplication
    assert h.nation.id == 'testlandia'


def test_wa_admit():
    t = '@@testlandia@@ was admitted to the World Assembly.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.WorldAssemblyAdmission
    assert h.nation.id == 'testlandia'


def test_wa_resign():
    t = '@@testlandia@@ resigned from the World Assembly.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.WorldAssemblyResignation
    assert h.nation.id == 'testlandia'


def test_delegate_remove():
    t = '@@testlandia@@ lost WA Delegate status in %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DelegateChange
    assert h.new_delegate is None
    assert h.old_delegate.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_delegate_install():
    t = '@@testlandia@@ became WA Delegate of %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DelegateChange
    assert h.new_delegate.id == 'testlandia'
    assert h.old_delegate is None
    assert h.region.id == 'the_east_pacific'


def test_delegate_change():
    t = '@@testlandia@@ seized the position of %%the_east_pacific%% WA Delegate from @@aidnaltset@@.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DelegateChange
    assert h.new_delegate.id == 'testlandia'
    assert h.old_delegate.id == 'aidnaltset'
    assert h.region.id == 'the_east_pacific'


def test_embassy_propose():
    t = '@@testlandia@@ proposed constructing embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyConstructionRequest
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_agree():
    t = '@@testlandia@@ agreed to construct embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyConstructionConfirmation
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_order_closure():
    t = '@@testlandia@@ ordered the closure of embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyClosureOrder
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_request_withdraw():
    t = '@@testlandia@@ withdrew a request for embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyConstructionRequestWithdrawal
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_abort_construction():
    t = '@@testlandia@@ aborted construction of embassies between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyConstructionAbortion
    assert h.nation.id == 'testlandia'
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_established():
    t = 'Embassy established between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyEstablishment
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_embassy_cancelled():
    t = 'Embassy cancelled between %%the_east_pacific%% and %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EmbassyCancellation
    assert h.regions[0].id == 'the_east_pacific'
    assert h.regions[1].id == 'the_north_pacific'


def test_endorse():
    t = '@@testlandia@@ endorsed @@aidnaltset@@.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.Endorsement
    assert h.endorser.id == 'testlandia'
    assert h.endorsee.id == 'aidnaltset'


def test_unendorse():
    t = '@@testlandia@@ withdrew its endorsement from @@aidnaltset@@.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.EndorsementWithdrawal
    assert h.endorser.id == 'testlandia'
    assert h.endorsee.id == 'aidnaltset'


def test_poll_create():
    t = '@@testlandia@@ created a new poll in %%the_east_pacific%%: "qwerty".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.PollCreation
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'
    assert h.title == 'qwerty'


def test_poll_create_html():
    t = '@@testlandia@@ created a new poll in %%the_east_pacific%%: "&lt;&gt;&amp; &gt; &quot;. &quot;. &amp;quot;.".'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.PollCreation
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'
    assert h.title == '<>& > ". ". &quot;.'


def test_poll_delete():
    t = '@@testlandia@@ deleted a regional poll in %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.PollDeletion
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'


def test_zombie_cleanse():
    t = '@@testlandia@@ was cleansed by a Level 5 Invasion Tactical Zombie Elimination Squad from @@landtestia@@, killing 195 million zombies.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.ZombieKillAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 195
    assert h.weapon == 'Level 5 Invasion Tactical Zombie Elimination Squad'


def test_zombie_ravage():
    t = '@@testlandia@@ was ravaged by a Zombie Thing Horde from @@landtestia@@, infecting 70 million survivors.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.ZombieInfectAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 70
    assert not h.convert
    assert h.weapon == 'Zombie Thing Horde'


def test_zombie_ravage_convert():
    t = '@@testlandia@@ was ravaged by a Zombie Thing Horde from @@landtestia@@, infecting 182 million survivors and converting to a zombie exporter! Oh no!'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.ZombieInfectAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 182
    assert h.convert
    assert h.weapon == 'Zombie Thing Horde'


def test_zombie_cure():
    t = '@@testlandia@@ was struck by a Mk I (Immunizer) Cure Missile from @@landtestia@@, curing 5 million infected.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.ZombieCureAction
    assert h.recepient.id == 'testlandia'
    assert h.sender.id == 'landtestia'
    assert h.impact == 5
    assert h.weapon == 'Mk I (Immunizer) Cure Missile'


def test_zombie_lockdown():
    t = '@@testlandia@@ instituted Lockdown Zombie Border Control in %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.ZombieBorderControlActivation
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'
    assert h.type == 'Lockdown'


def test_zombie_keycode():
    t = '@@testlandia@@ instituted Keycode Zombie Border Control in %%the_east_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.ZombieBorderControlActivation
    assert h.nation.id == 'testlandia'
    assert h.region.id == 'the_east_pacific'
    assert h.type == 'Keycode'


def test_refound():
    t = '@@testlandia@@ was refounded in %%lazarus%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.Refounding
    assert h.nation == Nation('testlandia')
    assert h.region == Region('lazarus')


def test_appoint_oficer_one_auth():
    t = '@@testlandia@@ appointed @@asdfg@@ as qwerty with authority over <i class="icon-mic"></i>Communications in %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerAppointment
    assert h.appointer == Nation('testlandia')
    assert h.appointee == Nation('asdfg')
    assert h.title == 'qwerty'
    assert h.authority == Authority.COMMUNICATIONS
    assert h.region == Region('the_north_pacific')


def test_appoint_oficer_two_auth():
    t = '@@testlandia@@ appointed @@asdfg@@ as qwerty with authority over <i class="icon-mic"></i>Communications and <i class="icon-building"></i>Embassies in %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerAppointment
    assert h.appointer == Nation('testlandia')
    assert h.appointee == Nation('asdfg')
    assert h.title == 'qwerty'
    assert h.authority == Authority.COMMUNICATIONS | Authority.EMBASSIES
    assert h.region == Region('the_north_pacific')


def test_appoint_oficer_many_auth():
    t = '@@testlandia@@ appointed @@asdfg@@ as qwerty with authority over <i class="icon-flag-1"></i>Appearance, <i class="icon-mic"></i>Border Control, <i class="icon-building"></i>Embassies, and <i class="icon-align-left"></i>Polls in %%the_north_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerAppointment
    assert h.appointer == Nation('testlandia')
    assert h.appointee == Nation('asdfg')
    assert h.title == 'qwerty'
    assert h.authority == (Authority.BORDER_CONTROL
                           | Authority.EMBASSIES
                           | Authority.APPEARANCE
                           | Authority.POLLS)
    assert h.region == Region('the_north_pacific')


def test_dismiss_oficer():
    t = '@@testlandia@@ dismissed @@qwerty@@ as asdf of %%the_pacific%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerDismissal
    assert h.dismisser == Nation('testlandia')
    assert h.dismissee == Nation('qwerty')
    assert h.title == 'asdf'
    assert h.region == Region('the pacific')


def test_revoke_delegate_auth():
    t = '@@parse_error@@ removed <i class="icon-flag-1"></i>Appearance and <i class="icon-shield"></i>Border Control authority from the WA Delegate in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DelegateModification
    assert h.nation == Nation('parse error')
    assert h.authority_removed == (Authority.BORDER_CONTROL
                                   | Authority.APPEARANCE)
    assert h.authority_granted == Authority(0)
    assert h.region == Region('try it and see')


def test_grant_delegate_auth():
    t = '@@parse_error@@ granted <i class="icon-flag-1"></i>Appearance and <i class="icon-mic"></i>Communications authority to the WA Delegate in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DelegateModification
    assert h.nation == Nation('parse error')
    assert h.authority_granted == (Authority.COMMUNICATIONS
                                   | Authority.APPEARANCE)
    assert h.authority_removed == Authority(0)
    assert h.region == Region('try it and see')


def test_grant_remove_delegate_auth():
    t = '@@parse_error@@ granted <i class="icon-align-left"></i>Polls authority and removed <i class="icon-flag-1"></i>Appearance authority from the WA Delegate in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.DelegateModification
    assert h.nation == Nation('parse error')
    assert h.authority_granted == Authority.POLLS
    assert h.authority_removed == Authority.APPEARANCE
    assert h.region == Region('try it and see')


def test_modify_officer_grant_auth():
    t = '@@parse_error@@ granted <i class="icon-mic"></i>Communications authority to @@bathyscaphe@@ as qwerty1 in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerModification
    assert h.agent == Nation('parse error')
    assert h.patient == Nation('bathyscaphe')
    assert h.old_title is None
    assert h.title == 'qwerty1'
    assert h.authority_granted == Authority.COMMUNICATIONS
    assert h.authority_removed == Authority(0)
    assert h.region == Region('try it and see')


def test_modify_officer_remove_auth():
    t = '@@parse_error@@ removed <i class="icon-building"></i>Embassies authority from @@bathyscaphe@@ as qwerty1 in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerModification
    assert h.agent == Nation('parse error')
    assert h.patient == Nation('bathyscaphe')
    assert h.old_title is None
    assert h.title == 'qwerty1'
    assert h.authority_granted == Authority(0)
    assert h.authority_removed == Authority.EMBASSIES
    assert h.region == Region('try it and see')


def test_modify_officer_grant_remove_auth():
    t = '@@parse_error@@ granted <i class="icon-mic"></i>Communications authority and removed <i class="icon-building"></i>Embassies authority from @@bathyscaphe@@ as qwerty1 in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerModification
    assert h.agent == Nation('parse error')
    assert h.patient == Nation('bathyscaphe')
    assert h.old_title is None
    assert h.title == 'qwerty1'
    assert h.authority_granted == Authority.COMMUNICATIONS
    assert h.authority_removed == Authority.EMBASSIES
    assert h.region == Region('try it and see')


def test_modify_officer_grant_remove_auth_rename():
    t = '@@parse_error@@ granted <i class="icon-shield"></i>Border Control and <i class="icon-building"></i>Embassies authority and removed <i class="icon-flag-1"></i>Appearance and <i class="icon-mic"></i>Communications authority from @@bathyscaphe@@ and renamed the office from "qwerty" to "qwerty1" in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerModification
    assert h.agent == Nation('parse error')
    assert h.patient == Nation('bathyscaphe')
    assert h.old_title == 'qwerty'
    assert h.title == 'qwerty1'
    assert h.authority_granted == (Authority.BORDER_CONTROL
                                   | Authority.EMBASSIES)
    assert h.authority_removed == (Authority.APPEARANCE
                                   | Authority.COMMUNICATIONS)
    assert h.region == Region('try it and see')


def test_modify_officer_rename():
    t = '@@parse_error@@ renamed the office held by @@bathyscaphe@@ from "qwerty1" to "qwerty2" in %%try_it_and_see%%.'
    h = happenings.process_happening(happening_elem(t))
    assert type(h) is happenings.OfficerModification
    assert h.agent == Nation('parse error')
    assert h.patient == Nation('bathyscaphe')
    assert h.old_title == 'qwerty1'
    assert h.title == 'qwerty2'
    assert h.authority_granted == Authority(0)
    assert h.authority_removed == Authority(0)
    assert h.region == Region('try it and see')
