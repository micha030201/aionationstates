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
    assert post.author == nation('testlandia')
