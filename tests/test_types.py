import xml.etree.ElementTree as ET
import datetime

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
    assert post.author == nation('testlandia')


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
    assert post.likers == [nation('aphrodite'), nation('apollo'),
                           nation('ares'), nation('artemis')]
    assert post.status == PostStatus.NORMAL
    assert post.suppressor is None
    assert post.author == nation('testlandia')


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
