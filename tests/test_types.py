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
