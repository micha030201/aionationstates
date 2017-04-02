#TODO: move test data into separate files?

from aionationstates import parse_api
from aionationstates.core import Govt, Dispatch, CensusPoint, CensusScale


def test_str():
    d = dict(parse_api(
        ('name', 'region', 'type', 'fullname', 'motto', 'category', 'animal', 
         'lastactivity', 'influence', 'leader', 'capital', 'religion'),
        standard
    ))
    assert d == {
        'name': 'Testlandia',
        'region': 'Testregionia',
        'type': 'Hive Mind',
        'fullname': 'The Hive Mind of Testlandia',
        'motto': 'Grr. Arg.',
        'category': 'Left-Leaning College State',
        'animal': '★★★ nautilus ★★★',
        'lastactivity': '2 hours ago',
        'influence': 'Superpower',
        'leader': 'Meridian Zero',
        'capital': 'Test City',
        'religion': 'Neo-Violetism'
    }

def test_int():
    d = dict(parse_api(
        ('population', 'firstlogin', 'lastlogin', 'factbooks', 'dispatches'),
        standard
    ))
    assert d == {
        'population': 29574,
        'firstlogin': 0,
        'lastlogin': 1490992918,
        'factbooks': 0,
        'dispatches': 3
    }

def test_wa():
    d = dict(parse_api(('unstatus',), standard))
    assert d == {'wa': True}

def test_govt():
    d = dict(parse_api(('govt',), standard))
    assert d == {
        'govt': Govt(
            administration=5.4,
            defence=14.9,
            education=10.7,
            environment=12.5,
            healthcare=12.0,
            commerce=6.8,
            internationalaid=5.6,
            lawandorder=7.8,
            publictransport=6.8,
            socialequality=5.0,
            spirituality=5.9,
            welfare=6.9
        )
    }

def test_deaths():
    d = dict(parse_api(('deaths',), standard))
    assert d == {
        'deaths': {
            'Acts of God': 0.6,
            'Lost in Wilderness': 5.8,
            'Heart Disease': 0.8,
            'Old Age': 92.5,
            'War': 0.2
        }
    }


standard = '''
<NATION>
<NAME>Testlandia</NAME>
<TYPE>Hive Mind</TYPE>
<FULLNAME>The Hive Mind of Testlandia</FULLNAME>
<MOTTO>Grr. Arg.</MOTTO>
<CATEGORY>Left-Leaning College State</CATEGORY>
<UNSTATUS>WA Member</UNSTATUS>
<FREEDOM>
 <CIVILRIGHTS>Excellent</CIVILRIGHTS>
 <ECONOMY>Very Strong</ECONOMY>
 <POLITICALFREEDOM>Good</POLITICALFREEDOM>
</FREEDOM>
<REGION>Testregionia</REGION>
<POPULATION>29574</POPULATION>
<TAX>91.6</TAX>
<ANIMAL>★★★ nautilus ★★★</ANIMAL>
<CURRENCY>denarius</CURRENCY>
<DEMONYM>Testlandish</DEMONYM>
<DEMONYM2>Testlandian</DEMONYM2>
<DEMONYM2PLURAL>Testlandians</DEMONYM2PLURAL>
<FLAG>https://www.nationstates.net/images/flags/Switzerland.png</FLAG>
<MAJORINDUSTRY>Arms Manufacturing</MAJORINDUSTRY>
<GOVTPRIORITY>Defence</GOVTPRIORITY>
<GOVT>
 <ADMINISTRATION>5.4</ADMINISTRATION>
 <DEFENCE>14.9</DEFENCE>
 <EDUCATION>10.7</EDUCATION>
 <ENVIRONMENT>12.5</ENVIRONMENT>
 <HEALTHCARE>12.0</HEALTHCARE>
 <COMMERCE>6.8</COMMERCE>
 <INTERNATIONALAID>5.6</INTERNATIONALAID>
 <LAWANDORDER>7.8</LAWANDORDER>
 <PUBLICTRANSPORT>6.8</PUBLICTRANSPORT>
 <SOCIALEQUALITY>5.0</SOCIALEQUALITY>
 <SPIRITUALITY>5.9</SPIRITUALITY>
 <WELFARE>6.9</WELFARE>
</GOVT>
<FOUNDED>0</FOUNDED>
<FIRSTLOGIN>0</FIRSTLOGIN>
<LASTLOGIN>1490992918</LASTLOGIN>
<LASTACTIVITY>2 hours ago</LASTACTIVITY>
<INFLUENCE>Superpower</INFLUENCE>
<FREEDOMSCORES>
 <CIVILRIGHTS>73</CIVILRIGHTS>
 <ECONOMY>78</ECONOMY>
 <POLITICALFREEDOM>63</POLITICALFREEDOM>
</FREEDOMSCORES>
<PUBLICSECTOR>90.9</PUBLICSECTOR>
<DEATHS>
 <CAUSE type="Acts of God">0.6</CAUSE>
 <CAUSE type="Lost in Wilderness">5.8</CAUSE>
 <CAUSE type="Heart Disease">0.8</CAUSE>
 <CAUSE type="Old Age">92.5</CAUSE>
 <CAUSE type="War">0.2</CAUSE>
</DEATHS>
<LEADER>Meridian Zero</LEADER>
<CAPITAL>Test City</CAPITAL>
<RELIGION>Neo-Violetism</RELIGION>
<FACTBOOKS>0</FACTBOOKS>
<DISPATCHES>3</DISPATCHES>

</NATION>
'''

def test_dispatch():
    xml = (
        '<WORLD>'
        '<DISPATCH id="1">'
        '<TITLE><![CDATA[How to Write a Dispatch]]></TITLE>'
        '<AUTHOR>testlandia</AUTHOR>'
        '<CATEGORY>Meta</CATEGORY>'
        '<SUBCATEGORY>Reference</SUBCATEGORY>'
        '<CREATED>1332332021</CREATED>'
        '<EDITED>1415948041</EDITED>'
        '<VIEWS>19523</VIEWS>'
        '<SCORE>486</SCORE>'
        '<TEXT><![CDATA[Lorem Ipsum]]></TEXT>'
        '</DISPATCH>'
        '</WORLD>'
    )
    d = dict(parse_api(('dispatch',), xml))
    assert d == {
        'dispatch': Dispatch(
            id=1,
            title='How to Write a Dispatch',
            author='testlandia',
            category='Meta',
            subcategory='Reference',
            created=1332332021,
            edited=1415948041,
            views=19523,
            score=486,
            text='Lorem Ipsum'
        )
    }

def test_dispatchlist():
    xml = (
        '<NATION id="testlandia">'
        '<DISPATCHLIST>'
        '<DISPATCH id="1">'
        '<TITLE><![CDATA[How to Write a Dispatch]]></TITLE>'
        '<AUTHOR>testlandia</AUTHOR>'
        '<CATEGORY>Meta</CATEGORY>'
        '<SUBCATEGORY>Reference</SUBCATEGORY>'
        '<CREATED>1332332021</CREATED>'
        '<EDITED>1415948041</EDITED>'
        '<VIEWS>19523</VIEWS>'
        '<SCORE>486</SCORE>'
        '</DISPATCH>'
        '<DISPATCH id="347510">'
        '<TITLE><![CDATA[Test]]></TITLE>'
        '<AUTHOR>testlandia</AUTHOR>'
        '<CATEGORY>Bulletin</CATEGORY>'
        '<SUBCATEGORY>Opinion</SUBCATEGORY>'
        '<CREATED>1419925409</CREATED>'
        '<EDITED>1480535821</EDITED>'
        '<VIEWS>979</VIEWS>'
        '<SCORE>30</SCORE>'
        '</DISPATCH>'
        '</DISPATCHLIST>'
        '</NATION>'
    )
    d = dict(parse_api(('dispatchlist',), xml))
    assert d == {
        'dispatchlist':
        [
            Dispatch(
                id=1,
                title='How to Write a Dispatch',
                author='testlandia',
                category='Meta',
                subcategory='Reference',
                created=1332332021,
                edited=1415948041,
                views=19523,
                score=486,
                text=None
            ),
            Dispatch(
                id=347510,
                title='Test',
                author='testlandia',
                category='Bulletin',
                subcategory='Opinion',
                created=1419925409,
                edited=1480535821,
                views=979,
                score=30,
                text=None
            )
        ]
    }

def test_censushistory():
    xml = (
        '<NATION id="testlandia">'
        '<CENSUS>'
        '<SCALE id="22">'
        '<POINT><TIMESTAMP>1490943600</TIMESTAMP>'
        '<SCORE>-10.2</SCORE>'
        '</POINT>'
        '<POINT><TIMESTAMP>1491030000</TIMESTAMP>'
        '<SCORE>55.4</SCORE>'
        '</POINT>'
        '<POINT><TIMESTAMP>1491116400</TIMESTAMP>'
        '<SCORE>-1444</SCORE>'
        '</POINT>'
        '</SCALE>'
        '<SCALE id="44">'
        '<POINT><TIMESTAMP>1490943600</TIMESTAMP>'
        '<SCORE>844.46</SCORE>'
        '</POINT>'
        '<POINT><TIMESTAMP>1491030000</TIMESTAMP>'
        '<SCORE>84.46</SCORE>'
        '</POINT>'
        '<POINT><TIMESTAMP>1491116400</TIMESTAMP>'
        '<SCORE>8.46</SCORE>'
        '</POINT>'
        '</SCALE>'
        '</CENSUS>'
        '</NATION>'
    )
    d = dict(parse_api(('census',), xml))
    assert d == {
        'censushistory':
        {22: [CensusPoint(
                  id=22,
                  timestamp=1490943600,
                  score=-10.2
              ), CensusPoint(
                  id=22,
                  timestamp=1491030000,
                  score=55.4
              ), CensusPoint(
                  id=22,
                  timestamp=1491116400,
                  score=-1444
              )],
         44: [CensusPoint(
                  id=44,
                  timestamp=1490943600,
                  score=844.46
              ), CensusPoint(
                  id=44,
                  timestamp=1491030000,
                  score=84.46
              ), CensusPoint(
                  id=44,
                  timestamp=1491116400,
                  score=8.46
              )],
         }
    }

def test_census():
    xml = (
        '<NATION id="testlandia">'
        '<CENSUS>'
        '<SCALE id="22">'
        '<SCORE>-10.20</SCORE>'
        '<RANK>170139</RANK>'
        '<PRANK>97</PRANK>'
        '<RRANK>19</RRANK>'
        '<PRRANK>100</PRRANK>'
        '</SCALE>'
        '<SCALE id="44">'
        '<SCORE>84.46</SCORE>'
        '<RANK>9297</RANK>'
        '<PRANK>6</PRANK>'
        '<RRANK>4</RRANK>'
        '<PRRANK>22</PRRANK>'
        '</SCALE>'
        '</CENSUS>'
        '</NATION>'
    )
    d = dict(parse_api(('census',), xml))
    assert d == {
        'census':
        {22: CensusScale(
                 id=22,
                 score=-10.2,
                 rank=170139,
                 prank=97,
                 rrank=19,
                 prrank=100
             ),
         44: CensusScale(
                 id=44,
                 score=84.46,
                 rank=9297,
                 prank=6,
                 rrank=4,
                 prrank=22
             )

         }
    }

def test_census_partial():
    xml = (
        '<NATION id="testlandia">'
        '<CENSUS>'
        '<SCALE id="22">'
        '<SCORE>-10.20</SCORE>'
        '<PRRANK>100</PRRANK>'
        '</SCALE>'
        '<SCALE id="44">'
        '<SCORE>84.46</SCORE>'
        '<PRRANK>22</PRRANK>'
        '</SCALE>'
        '</CENSUS>'
        '</NATION>'
    )
    d = dict(parse_api(('census',), xml))
    assert d == {
        'census':
        {22: CensusScale(
                 id=22,
                 score=-10.2,
                 rank=None,
                 prank=None,
                 rrank=None,
                 prrank=100
             ),
         44: CensusScale(
                 id=44,
                 score=84.46,
                 rank=None,
                 prank=None,
                 rrank=None,
                 prrank=22
             )

         }
    }



