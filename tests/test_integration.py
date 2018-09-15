"""Particularly nasty edge cases as well as some simple sanity checks."""

import pytest

import utils
import aionationstates


class Nation(utils.SessionTestMixin, aionationstates.Nation):
    pass


class NationControl(utils.SessionTestMixin, aionationstates.NationControl):
    pass


aionationstates.world_._World._base_call_api = utils.SessionTestMixin._base_call_api


@pytest.mark.asyncio
async def test_name():
    nation = Nation('testLandia')
    nation._responses = {
        utils.get({'nation': 'testlandia', 'q': 'name'}):
        utils.response('''
        <NATION id="testlandia">
            <NAME>Testlandia</NAME>
        </NATION>
        ''')
    }
    name = await nation.name()
    assert name == 'Testlandia'


@pytest.mark.asyncio
async def test_issue():
    nation = NationControl('testLandia', password='hunter2')
    nation._responses = {
        utils.get({'nation': 'testlandia', 'q': 'issues'}):
        utils.response('''
        <NATION id="testlandia">
            <ISSUES>
                <ISSUE id="111">
                    <TITLE>Issue Title</TITLE>
                    <TEXT>issue text</TEXT>
                    <AUTHOR>author</AUTHOR>
                    <EDITOR>editor</EDITOR>
                    <OPTION id="0">qwerty</OPTION>
                    <OPTION id="1">asdfg</OPTION>
                    <OPTION id="2">ytrewq</OPTION>
                    <OPTION id="3">gfdsa</OPTION>
                </ISSUE>
            </ISSUES>
        </NATION>
        '''),

        utils.post({'nation': 'testlandia', 'c': 'issue',
                    'issue': '111', 'option': '2'}):
        utils.response('''
        <NATION id="testlandia">
        <ISSUE id="111" choice="2">
            <OK>1</OK>
            <DESC>qwerty</DESC>
            <RANKINGS>
                <RANK id="5">
                    <SCORE>108.18</SCORE>
                    <CHANGE>-0.83</CHANGE>
                    <PCHANGE>-0.761398</PCHANGE>
                </RANK>
                <RANK id="79">
                    <SCORE>31.26</SCORE>
                    <CHANGE>-4.41</CHANGE>
                    <PCHANGE>-12.363331</PCHANGE>
                </RANK>
            </RANKINGS>
            <HEADLINES>
                <HEADLINE>headline1</HEADLINE>
                <HEADLINE>headline2</HEADLINE>
            </HEADLINES>
            <UNLOCKS>
                <BANNER>t19</BANNER>
                <BANNER>r8</BANNER>
            </UNLOCKS>
        </ISSUE>
        </NATION>
        '''),

        utils.get({'nation': 'testlandia', 'q': 'demonym+name+religion'}):
        utils.response('''
        <NATION id="testlandia">
            <NAME>Testlandia</NAME>
            <DEMONYM>Testlandian</DEMONYM>
            <RELIGION>Neo-Violetism</RELIGION>
        </NATION>
        '''),
    }

    aionationstates.world._responses = {
        utils.get({'q': 'banner', 'banner': 't19,r8'}):
        utils.response('''
        <WORLD>
            <BANNERS>
                <BANNER id="t19">
                    <NAME>Father Knows Best</NAME>
                    <VALIDITY>Become a Father Knows Best state</VALIDITY>
                </BANNER>
                <BANNER id="r8">
                    <NAME>Icy Gaze</NAME>
                    <VALIDITY>test @@NAME@@ qwerty</VALIDITY>
                </BANNER>
            </BANNERS>
        </WORLD>
        '''),
    }

    issues = await nation.issues()
    assert issues[0].id == 111
    assert issues[0].title == 'Issue Title'
    assert issues[0].options[0].text == 'qwerty'

    issueresult = await issues[0].options[2].accept()
    assert issueresult.effect_line == 'qwerty'
    assert issueresult.banners[0].name == 'Father Knows Best'
    assert issueresult.banners[1].name == 'Icy Gaze'
    assert issueresult.banners[1].validity == 'test Testlandia qwerty'
