import xml.etree.ElementTree as ET
import datetime

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
