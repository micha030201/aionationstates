import xml.etree.ElementTree as ET
import datetime
import datetime as dt

import pytest

from aionationstates import *


elem = ET.fromstring


def test_post():
    post = Post(elem('''
        <POST id="12345">
            <TIMESTAMP>1510000000</TIMESTAMP>
            <NATION>testlandia</NATION>
            <STATUS>0</STATUS>
            <LIKES>0</LIKES>
            <MESSAGE><![CDATA[qwerty]]></MESSAGE>
        </POST>
    '''))
    assert post.text == 'qwerty'
    assert post.id == 12345
    assert post.timestamp == datetime.datetime.utcfromtimestamp(1510000000)
    assert post.likers == []
    assert post.status == PostStatus.NORMAL
    assert post.suppressor is None
    assert post.author == Nation('testlandia')


def test_post_likers():
    post = Post(elem('''
        <POST id="12345">
            <TIMESTAMP>1510000000</TIMESTAMP>
            <NATION>testlandia</NATION>
            <STATUS>0</STATUS>
            <LIKES>4</LIKES>
            <LIKERS>aphrodite:apollo:ares:artemis</LIKERS>
            <MESSAGE><![CDATA[qwerty]]></MESSAGE>
        </POST>
    '''))
    assert post.text == 'qwerty'
    assert post.id == 12345
    assert post.timestamp == datetime.datetime.utcfromtimestamp(1510000000)
    assert post.likers == [Nation('aphrodite'), Nation('apollo'),
                           Nation('ares'), Nation('artemis')]
    assert post.status == PostStatus.NORMAL
    assert post.suppressor is None
    assert post.author == Nation('testlandia')


def test_post_quote():
    post = Post(elem('''
        <POST id="12345">
            <TIMESTAMP>1510000000</TIMESTAMP>
            <NATION>testlandia</NATION>
            <STATUS>0</STATUS>
            <LIKES>0</LIKES>
            <MESSAGE><![CDATA[qwerty]]></MESSAGE>
        </POST>
    '''))
    assert post.text == 'qwerty'
    assert post.quote() == '[quote=testlandia;12345]qwerty[/quote]'


def test_post_quote_custom():
    post = Post(elem('''
        <POST id="12345">
            <TIMESTAMP>1510000000</TIMESTAMP>
            <NATION>testlandia</NATION>
            <STATUS>0</STATUS>
            <LIKES>0</LIKES>
            <MESSAGE><![CDATA[qwerty]]></MESSAGE>
        </POST>
    '''))
    assert post.text == 'qwerty'
    assert post.quote('ytrewq') == '[quote=testlandia;12345]ytrewq[/quote]'


def test_post_quote_multilevel():
    post = Post(elem('''
        <POST id="12345">
            <TIMESTAMP>1510000000</TIMESTAMP>
            <NATION>testlandia</NATION>
            <STATUS>0</STATUS>
            <LIKES>0</LIKES>
            <MESSAGE><![CDATA[[quote=testlandia;12344]ytrewq[/quote]\nqwerty]]></MESSAGE>
        </POST>
    '''))
    assert post.text == '[quote=testlandia;12344]ytrewq[/quote]\nqwerty'
    assert post.quote() == '[quote=testlandia;12345]qwerty[/quote]'


def test_tgqueue():
    tgqueue = TGQueue(elem('''
        <TGQUEUE>
            <MANUAL>212</MANUAL>
            <MASS>56456</MASS>
            <API>2328</API>
        </TGQUEUE>
    '''))
    assert tgqueue.manual == 212
    assert tgqueue.stamp == 56456
    assert tgqueue.api == 2328


def test_policy():
    policy = Policy(elem('''
        <POLICY>
            <NAME>Devolution</NAME>
            <PIC>t64</PIC>
            <CAT>Government</CAT>
            <DESC>Government power is substantially delegated to local authorities.</DESC>
        </POLICY>
    '''))
    assert policy.name == 'Devolution'
    assert policy.category == 'Government'
    assert policy.description == 'Government power is substantially delegated to local authorities.'
    assert policy.banner == 'https://www.nationstates.net/images/banners/t64.jpg'


def test_poll():
    poll = Poll(elem('''
        <POLL id="106040">
            <TITLE><![CDATA[fgrnhnhm]]></TITLE>
            <TEXT><![CDATA[inmimimn]]></TEXT>
            <REGION>testregionia</REGION>
            <START>1513110331</START>
            <STOP>1513974331</STOP>
            <AUTHOR>testlandia</AUTHOR>
            <OPTIONS>
                <OPTION id="0">
                    <OPTIONTEXT><![CDATA[olholmjn]]></OPTIONTEXT>
                    <VOTES>1</VOTES>
                    <VOTERS>qwerty</VOTERS>
                </OPTION>
                <OPTION id="1">
                    <OPTIONTEXT><![CDATA[drthdfrgb]]></OPTIONTEXT>
                    <VOTES>0</VOTES>
                    <VOTERS></VOTERS>
                </OPTION>
                <OPTION id="2">
                    <OPTIONTEXT><![CDATA[omommmo]]></OPTIONTEXT>
                    <VOTES>2</VOTES>
                    <VOTERS>rtyu:testlandia</VOTERS>
                </OPTION>
            </OPTIONS>
        </POLL>
    '''))
    assert poll.id == 106040
    assert poll.title == 'fgrnhnhm'
    assert poll.text == 'inmimimn'
    assert poll.region == Region('testregionia')

    assert poll.start == datetime.datetime.utcfromtimestamp(1513110331)
    assert poll.stop == datetime.datetime.utcfromtimestamp(1513974331)

    assert poll.author == Nation('testlandia')

    assert poll.options[0].text == 'olholmjn'
    assert poll.options[0].voters == [Nation('qwerty')]

    assert poll.options[1].text == 'drthdfrgb'
    assert poll.options[1].voters == []

    assert poll.options[2].text == 'omommmo'
    assert poll.options[2].voters == [Nation('rtyu'), Nation('testlandia')]


def test_poll_notext():
    poll = Poll(elem('''
        <POLL id="106040">
            <TITLE><![CDATA[fgrnhnhm]]></TITLE>
            <REGION>testregionia</REGION>
            <START>1513110331</START>
            <STOP>1513974331</STOP>
            <AUTHOR>testlandia</AUTHOR>
            <OPTIONS>
                <OPTION id="0">
                    <OPTIONTEXT><![CDATA[olholmjn]]></OPTIONTEXT>
                    <VOTES>1</VOTES>
                    <VOTERS>qwerty</VOTERS>
                </OPTION>
                <OPTION id="1">
                    <OPTIONTEXT><![CDATA[drthdfrgb]]></OPTIONTEXT>
                    <VOTES>0</VOTES>
                    <VOTERS></VOTERS>
                </OPTION>
                <OPTION id="2">
                    <OPTIONTEXT><![CDATA[omommmo]]></OPTIONTEXT>
                    <VOTES>2</VOTES>
                    <VOTERS>rtyu:testlandia</VOTERS>
                </OPTION>
            </OPTIONS>
        </POLL>
    '''))
    assert poll.text is None


def test_proposal():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Environmental</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[isn&#146;t]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Trees They Are Us</NAME>
            <OPTION>All Businesses</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS/>
        </PROPOSAL>
    '''))
    assert proposal.text == 'isn’t'
    assert proposal.id == 'qwerty_1522432818'
    assert proposal.category == 'Environmental'
    assert proposal.name == 'Trees They Are Us'
    assert proposal.option == 'All Businesses'
    assert proposal.author == Nation('qwerty')
    assert proposal.approved_by == []
    assert proposal.council == 'General Assembly'
    assert proposal.submitted == datetime.datetime(2018, 3, 30, 18, 0, 18)
    assert proposal.url == 'https://www.nationstates.net/page=UN_view_proposal/id=qwerty_1522432818'


def test_proposal_approved():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Environmental</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[isn&#146;t]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Trees They Are Us</NAME>
            <OPTION>All Businesses</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.approved_by == [
        Nation('some'), Nation('body'), Nation('once'), Nation('told'),
        Nation('me')
    ]


def test_proposal_sc_liberate():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Liberation</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[haha yes]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Liberate Some Region Or Whatever</NAME>
            <OPTION>R:Some Region Or Whatever</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'Security Council'
    assert proposal.target == Region('Some Region Or Whatever')


def test_proposal_sc_commend():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Commendation</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[for being such a good boy]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Commend This Cute Dog</NAME>
            <OPTION>N:This Cute Dog</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'Security Council'
    assert proposal.target == Nation('This Cute Dog')


def test_proposal_sc_condemn():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Condemnation</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[raiders bad]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Condemn Some Raiders</NAME>
            <OPTION>R:Some Raiders</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'Security Council'
    assert proposal.target == Region('Some raiders')


def test_proposal_repeal():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Repeal</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[further research has lead us to conclude otherwise]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Repeal &quot;Trees They Are Us&quot;</NAME>
            <OPTION>9999</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'General Assembly'


def test_proposal_sc_repeal_liberate():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Repeal</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[what's the antonym for liberate? incarcerate? no reason, just curious]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Repeal &quot;Liberate Some Region Or Whatever&quot;</NAME>
            <OPTION>9999</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'Security Council'


def test_proposal_sc_repeal_condemn():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Repeal</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[raiders good]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Repeal &quot;Condemn Some Raiders&quot;</NAME>
            <OPTION>9999</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'Security Council'


def test_proposal_sc_repeal_commend():
    proposal = Proposal(elem('''
        <PROPOSAL id="qwerty_1522432818">
            <CATEGORY>Repeal</CATEGORY>
            <CREATED>1522432818</CREATED>
            <DESC><![CDATA[heck u cats are better]]></DESC>
            <ID>qwerty_1522432818</ID>
            <NAME>Repeal &quot;Commend This Cute Dog&quot;</NAME>
            <OPTION>9999</OPTION>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <APPROVALS>some:body:once:told:me</APPROVALS>
        </PROPOSAL>
    '''))
    assert proposal.council == 'Security Council'


def test_proposal_at_vote():
    proposal = ResolutionAtVote(elem('''
        <RESOLUTION>
            <CATEGORY>Liberation</CATEGORY>
            <CREATED>1521428163</CREATED>
            <DELLOG>
                <ENTRY>
                    <TIMESTAMP>1522166492</TIMESTAMP>
                    <NATION>qweqwr</NATION>
                    <ACTION>FOR</ACTION>
                    <VOTES>4</VOTES>
                </ENTRY>
                <ENTRY>
                    <TIMESTAMP>1522166559</TIMESTAMP>
                    <NATION>asd</NATION>
                    <ACTION>FOR</ACTION>
                    <VOTES>7</VOTES>
                </ENTRY>
                <ENTRY>
                    <TIMESTAMP>1522166560</TIMESTAMP>
                    <NATION>qweqwr</NATION>
                    <ACTION>AGAINST</ACTION>
                    <VOTES>4</VOTES>
                </ENTRY>
                <ENTRY>
                    <TIMESTAMP>1522166585</TIMESTAMP>
                    <NATION>bbbbb</NATION>
                    <ACTION>AGAINST</ACTION>
                    <VOTES>4</VOTES>
                </ENTRY>
                <ENTRY>
                    <TIMESTAMP>1522166622</TIMESTAMP>
                    <NATION>bbbbb</NATION>
                    <ACTION>WITHDREW</ACTION>
                    <VOTES>4</VOTES>
                </ENTRY>
            </DELLOG>
            <DESC><![CDATA[text]]></DESC>
            <ID>qwerty_1521428163</ID>
            <NAME>name</NAME>
            <OPTION>123</OPTION>
            <PROMOTED>1522166403</PROMOTED>
            <PROPOSED_BY>qwerty</PROPOSED_BY>
            <TOTAL_NATIONS_AGAINST>2060</TOTAL_NATIONS_AGAINST>
            <TOTAL_NATIONS_FOR>6202</TOTAL_NATIONS_FOR>
            <TOTAL_VOTES_AGAINST>4236</TOTAL_VOTES_AGAINST>
            <TOTAL_VOTES_FOR>13329</TOTAL_VOTES_FOR>
            <VOTE_TRACK_AGAINST>
                <N>0</N>
                <N>571</N>
                <N>772</N>
                <N>907</N>
            </VOTE_TRACK_AGAINST>
            <VOTE_TRACK_FOR>
                <N>0</N>
                <N>3644</N>
                <N>4735</N>
                <N>5141</N>
            </VOTE_TRACK_FOR>
            <VOTES_AGAINST>
                <N>zzzzzz</N>
                <N>xxxxxxx</N>
            </VOTES_AGAINST>
            <VOTES_FOR>
                <N>qqqqqqq</N>
                <N>wwwwww</N>
            </VOTES_FOR>
        </RESOLUTION>
    '''))
    proposal._council_id = 1

    assert proposal.text == 'text'
    assert proposal.id == 'qwerty_1521428163'
    assert proposal.category == 'Liberation'
    assert proposal.name == 'name'
    assert proposal.option == '123'
    assert proposal.author == Nation('qwerty')
    assert proposal.council == 'General Assembly'
    assert proposal.submitted == datetime.datetime(2018, 3, 19, 2, 56, 3)
    assert proposal.promoted == datetime.datetime(2018, 3, 27, 16, 0, 3)
    assert proposal.url == 'https://www.nationstates.net/page=ga'

    assert proposal.nation_votes_against == 2060
    assert proposal.nation_votes_for == 6202
    assert proposal.total_votes_against == 4236
    assert proposal.total_votes_for == 13329

    first_log_entry = proposal.delegate_vote_log[0]
    assert first_log_entry.nation == Nation('qweqwr')
    assert first_log_entry.votes == 4
    assert first_log_entry.timestamp == datetime.datetime(2018, 3, 27, 16, 1, 32)

    last_track_entry = proposal.vote_track[-1]
    assert last_track_entry.for_ == 5141
    assert last_track_entry.against == 907
    assert last_track_entry.timestamp == proposal.promoted + dt.timedelta(hours=3)

    assert proposal.nations_voting_for == [
        Nation('qqqqqqq'),
        Nation('wwwwww')
    ]
    assert proposal.nations_voting_against == [
        Nation('zzzzzz'),
        Nation('xxxxxxx')
    ]

    assert proposal.delegates_voting_for == [
        (Nation('asd'), 7)
    ]
    assert proposal.delegates_voting_against == [
        (Nation('qweqwr'), 4)
    ]


def test_resolution():
    resolution = Resolution(elem('''
    <RESOLUTION>
        <CATEGORY>Condemnation</CATEGORY>
        <COUNCIL>2</COUNCIL>
        <COUNCILID>52</COUNCILID>
        <CREATED>1301228591</CREATED>
        <DESC><![CDATA[aaaa]]></DESC>
        <IMPLEMENTED>1301932801</IMPLEMENTED>
        <NAME>nameeee</NAME>
        <OPTION>R:reeeeddfgidofbern</OPTION>
        <PROPOSED_BY>qweqwrt</PROPOSED_BY>
        <RESID>195</RESID>
        <TOTAL_VOTES_AGAINST>4641</TOTAL_VOTES_AGAINST>
        <TOTAL_VOTES_FOR>4960</TOTAL_VOTES_FOR>
    </RESOLUTION>
    '''))
    assert resolution.text == 'aaaa'
    assert resolution.id == 'qweqwrt_1301228591'
    assert resolution.local_index == 52
    assert resolution.global_index == 195
    assert resolution.category == 'Condemnation'
    assert resolution.name == 'nameeee'
    assert resolution.target == Region('reeeeddfgidofbern')
    assert resolution.author == Nation('qweqwrt')
    assert resolution.council == 'Security Council'
    assert resolution.submitted == datetime.datetime(2011, 3, 27, 12, 23, 11)
    assert resolution.promoted == datetime.datetime(2011, 3, 30, 16, 0, 1)
    assert resolution.implemented == datetime.datetime(2011, 4, 4, 16, 0, 1)
    assert resolution.total_votes_for == 4960
    assert resolution.total_votes_against == 4641
    assert resolution.url == 'https://www.nationstates.net/page=WA_past_resolution/id=195'


async def expand_macros(s):
    return (
        s
        .replace('@@NAME@@', 'Testlandia')
        .replace('@@FAITH@@', 'Neo-violetism')
        .replace('@@DEMONYM@@', 'Testlandish')
    )


@pytest.mark.asyncio
async def test_issueresult_invalid_option():
    with pytest.raises(ValueError):
        await IssueResult(elem('''
        <ISSUE id="365" choice="42">
            <ERROR>Invalid choice.</ERROR>
        </ISSUE>
        '''), expand_macros)


@pytest.mark.asyncio
async def test_issueresult_invalid_issue():
    with pytest.raises(ValueError):
        await IssueResult(elem('''
        <ISSUE id="365456" choice="42">
            <ERROR>Issue already processed!</ERROR>
        </ISSUE>
        '''), expand_macros)


@pytest.mark.asyncio
async def test_issueresult():
    issueresult = await IssueResult(elem('''
      <ISSUE id="365" choice="2">
        <OK>1</OK>
        <DESC>qwerty</DESC>
        <RANKINGS>
          <RANK id="0">
            <SCORE>65.53</SCORE>
            <CHANGE>4.46</CHANGE>
            <PCHANGE>7.303095</PCHANGE>
          </RANK>
          <RANK id="36">
            <SCORE>23.87</SCORE>
            <CHANGE>0.93</CHANGE>
            <PCHANGE>4.054054</PCHANGE>
          </RANK>
          <RANK id="37">
            <SCORE>18.85</SCORE>
            <CHANGE>-1.20</CHANGE>
            <PCHANGE>-5.985037</PCHANGE>
          </RANK>
        </RANKINGS>
        <RECLASSIFICATIONS>
          <RECLASSIFY type="0">
            <FROM>Good</FROM>
            <TO>Very Good</TO>
          </RECLASSIFY>
        </RECLASSIFICATIONS>
        <HEADLINES>
          <HEADLINE>srrgbrgbrgb</HEADLINE>
          <HEADLINE>mniomnthnmith</HEADLINE>
        </HEADLINES>
      </ISSUE>
    '''), expand_macros)
    assert issueresult.effect_line == 'qwerty'

    assert issueresult.census[0].info.title == 'Civil Rights'
    assert issueresult.census[0].score == 65.53
    assert issueresult.census[0].change == 4.46
    assert issueresult.census[0].pchange == 7.303095

    assert issueresult.census[1].score == 23.87
    assert issueresult.census[1].change == 0.93
    assert issueresult.census[1].pchange == 4.054054

    assert issueresult.census[2].score == 18.85
    assert issueresult.census[2].change == -1.20
    assert issueresult.census[2].pchange == -5.985037

    assert issueresult.reclassifications == [
        'Testlandia\'s Civil Rights rose from Good to Very Good']
    assert issueresult.headlines == ['srrgbrgbrgb', 'mniomnthnmith']


@pytest.mark.asyncio
async def test_issueresult_no_reclassifications():
    issueresult = await IssueResult(elem('''
      <ISSUE id="365" choice="2">
        <OK>1</OK>
        <DESC>qwerty</DESC>
        <RANKINGS>
          <RANK id="0">
            <SCORE>65.53</SCORE>
            <CHANGE>4.46</CHANGE>
            <PCHANGE>7.303095</PCHANGE>
          </RANK>
          <RANK id="36">
            <SCORE>23.87</SCORE>
            <CHANGE>0.93</CHANGE>
            <PCHANGE>4.054054</PCHANGE>
          </RANK>
          <RANK id="37">
            <SCORE>18.85</SCORE>
            <CHANGE>-1.20</CHANGE>
            <PCHANGE>-5.985037</PCHANGE>
          </RANK>
        </RANKINGS>
        <HEADLINES>
          <HEADLINE>srrgbrgbrgb</HEADLINE>
          <HEADLINE>mniomnthnmith</HEADLINE>
        </HEADLINES>
      </ISSUE>
    '''), expand_macros)
    assert issueresult.reclassifications == []


@pytest.mark.asyncio
async def test_issueresult_reclassifications():
    issueresult = await IssueResult(elem('''
      <ISSUE id="365" choice="2">
        <OK>1</OK>
        <DESC>qwerty</DESC>
        <RANKINGS>
          <RANK id="0">
            <SCORE>65.53</SCORE>
            <CHANGE>4.46</CHANGE>
            <PCHANGE>7.303095</PCHANGE>
          </RANK>
          <RANK id="1">
            <SCORE>65.53</SCORE>
            <CHANGE>-4.46</CHANGE>
            <PCHANGE>-7.303095</PCHANGE>
          </RANK>
          <RANK id="2">
            <SCORE>65.53</SCORE>
            <CHANGE>-4.46</CHANGE>
            <PCHANGE>-7.303095</PCHANGE>
          </RANK>
          <RANK id="36">
            <SCORE>23.87</SCORE>
            <CHANGE>0.93</CHANGE>
            <PCHANGE>4.054054</PCHANGE>
          </RANK>
          <RANK id="37">
            <SCORE>18.85</SCORE>
            <CHANGE>-1.20</CHANGE>
            <PCHANGE>-5.985037</PCHANGE>
          </RANK>
        </RANKINGS>
        <RECLASSIFICATIONS>
          <RECLASSIFY type="0">
            <FROM>Good</FROM>
            <TO>Very Good</TO>
          </RECLASSIFY>
          <RECLASSIFY type="1">
            <FROM>Very Good</FROM>
            <TO>Good</TO>
          </RECLASSIFY>
          <RECLASSIFY type="2">
            <FROM>Excellent</FROM>
            <TO>Below Average</TO>
          </RECLASSIFY>
          <RECLASSIFY type="govt">
            <FROM>Inoffensive Centrist Democracy</FROM>
            <TO>Democratic Socialists</TO>
          </RECLASSIFY>
        </RECLASSIFICATIONS>
        <HEADLINES>
          <HEADLINE>srrgbrgbrgb</HEADLINE>
          <HEADLINE>mniomnthnmith</HEADLINE>
        </HEADLINES>
      </ISSUE>
    '''), expand_macros)
    assert issueresult.reclassifications == [
        'Testlandia\'s Civil Rights rose from Good to Very Good',
        'Testlandia\'s Economy fell from Very Good to Good',
        'Testlandia\'s Political Freedom fell from Excellent to Below Average',
        'Testlandia was reclassified from Inoffensive Centrist Democracy to Democratic Socialists'
    ]


@pytest.mark.asyncio
async def test_issueresult_policies():
    issueresult = await IssueResult(elem('''
      <ISSUE id="365" choice="2">
        <OK>1</OK>
        <DESC>qwerty</DESC>
        <RANKINGS>
          <RANK id="0">
            <SCORE>65.53</SCORE>
            <CHANGE>4.46</CHANGE>
            <PCHANGE>7.303095</PCHANGE>
          </RANK>
          <RANK id="36">
            <SCORE>23.87</SCORE>
            <CHANGE>0.93</CHANGE>
            <PCHANGE>4.054054</PCHANGE>
          </RANK>
          <RANK id="37">
            <SCORE>18.85</SCORE>
            <CHANGE>-1.20</CHANGE>
            <PCHANGE>-5.985037</PCHANGE>
          </RANK>
        </RANKINGS>
        <NEW_POLICIES>
          <POLICY>
            <NAME>Devolution</NAME>
            <PIC>t64</PIC>
            <CAT>Government</CAT>
            <DESC>Government power is substantially delegated to local authorities.</DESC>
          </POLICY>
          <POLICY>
            <NAME>Native Representation</NAME>
            <PIC>t42</PIC>
            <CAT>Government</CAT>
            <DESC>Only native-born citizens may hold elected office.</DESC>
          </POLICY>
        </NEW_POLICIES>
        <REMOVED_POLICIES>
          <POLICY>
            <NAME>Marriage Equality</NAME>
            <PIC>p25</PIC>
            <CAT>Society</CAT>
            <DESC>Citizens of the same sex may marry.</DESC>
          </POLICY>
        </REMOVED_POLICIES>
        <HEADLINES>
          <HEADLINE>srrgbrgbrgb</HEADLINE>
          <HEADLINE>mniomnthnmith</HEADLINE>
        </HEADLINES>
      </ISSUE>
    '''), expand_macros)
    assert issueresult.new_policies[0].name == 'Devolution'
    assert issueresult.new_policies[1].name == 'Native Representation'
    assert issueresult.removed_policies[0].name == 'Marriage Equality'
