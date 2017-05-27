# TODO slots

from contextlib import suppress
from collections import namedtuple
from html import unescape

from aionationstates.ns_to_human import census_info


class NationStatesHTMLMess:
    """In some cases, such as with poll and issue options,
    NS returns weird sorta-HTML data instead of plain text.

    While it is understandable that they just wanted fancy font styles,
    like italics or bold, and couldn't come up with a better alternative
    to embedding pieces of HTML here and there, having tags and entities
    sprinkled throughout your text is often undesirable, and getting rid
    of them properly can be a nuisance.

    However, we do not want to lose font styles by presenting the data
    as a string; and converting it to another, more forgiving markup
    language would just be silly.
    Hence the need for this class. It stores the raw weirdness as returned
    by NS, but lets you painlessly convert it to plain text and a few other
    formats, or deal with it directly, should you so desire.
    """
    def __init__(self, raw):
        self.raw = raw

    def __str__(self):
        return unescape(re.sub('<.+?>', '', self.raw))

    def md(self):
        return unescape(self.raw.replace('<i>', '*').replace('</i>', '*'))


class CensusScale:
    def __init__(self, elem):
        self.info = census_info[int(elem.get('id'))]


class CensusScaleCurrent(CensusScale):
    def __init__(self, elem):
        super().__init__(elem)
        # For recently-founded nations (and maybe in other cases as well, who
        # knows) the ranks & percentages may not show up even if requested.
        self.score = self.rank = self.prank = self.rrank = self.prrank = None
        with suppress(AttributeError, TypeError):
            self.score = float(elem.find('SCORE').text)
        with suppress(AttributeError, TypeError):
            self.rank = int(elem.find('RANK').text)
        with suppress(AttributeError, TypeError):
            self.prank = float(elem.find('PRANK').text)
        with suppress(AttributeError, TypeError):
            self.rrank = int(elem.find('RRANK').text)
        with suppress(AttributeError, TypeError):
            self.prrank = float(elem.find('PRRANK').text)

    def __repr__(self):
        return f'<CensusScaleCurrent #{self.info.id} "{self.info.title}">'


class CensusPoint:
    def __init__(self, elem):
        super().__init__(elem)
        self.timestamp = int(elem.find('TIMESTAMP').text)
        self.score = float(elem.find('SCORE').text)

    def __repr__(self):
        return f'<CensusPoint timestamp={self.timestamp}>'


class CensusScaleHistory(CensusScale):
    def __init__(self, elem):
        super().__init__(elem)
        self.history = [CensusPoint(sub_elem) for sub_elem in elem]

    def __repr__(self):
        return f'<CensusScaleHistory #{self.info.id} "{self.info.title}">'



class DispatchThumbnail:
    def __init__(self, elem):
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text
        self.author = elem.find('AUTHOR').text
        self.category = elem.find('CATEGORY').text
        self.subcategory = elem.find('SUBCATEGORY').text
        self.created = int(elem.find('CREATED').text)
        self.edited = int(elem.find('EDITED').text)
        self.views = int(elem.find('VIEWS').text)
        self.score = int(elem.find('SCORE').text)

    def __repr__(self):
        return f'<DispatchThumbnail id={self.id}>'


class Dispatch(DispatchThumbnail):
    def __init__(self, elem):
        super().__init__(elem)
        self.text = elem.find('TEXT').text

    def __repr__(self):
        return f'<Dispatch id={self.id}>'



class PollOption:
    def __init__(self, elem):
        self.text = NationStatesHTMLMess(elem.find('OPTIONTEXT').text)
        voters = elem.find('VOTERS').text
        self.voters = voters.split(':') if voters else ()


class Poll:
    def __init__(self, elem):
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text  # XXX html?
        self.text = NationStatesHTMLMess(elem.find('TEXT').text)
        self.region = elem.find('REGION').text
        self.author = elem.find('AUTHOR').text
        self.start = int(elem.find('START').text)
        self.stop = int(elem.find('STOP').text)
        self.options = [PollOption(option_elem)
                        for option_elem in elem.find('OPTIONS')]

    def __repr__(self):
        return f'<Poll id={self.id}>'



class Freedom:
    def __init__(self, elem):
        self.civilrights = elem.find('CIVILRIGHTS').text
        self.economy = elem.find('ECONOMY').text
        self.politicalfreedom = elem.find('POLITICALFREEDOM').text


class FreedomScores:
    def __init__(self, elem):
        self.civilrights = int(elem.find('CIVILRIGHTS').text)
        self.economy = int(elem.find('ECONOMY').text)
        self.politicalfreedom = int(elem.find('POLITICALFREEDOM').text)


class Govt:
    def __init__(self, elem):
        self.administration = float(govt.find('ADMINISTRATION').text)
        self.defence = float(govt.find('DEFENCE').text)
        self.education = float(govt.find('EDUCATION').text)
        self.environment = float(govt.find('ENVIRONMENT').text)
        self.healthcare = float(govt.find('HEALTHCARE').text)
        self.commerce = float(govt.find('COMMERCE').text)
        self.internationalaid = float(govt.find('INTERNATIONALAID').text)
        self.lawandorder = float(govt.find('LAWANDORDER').text)
        self.publictransport = float(govt.find('PUBLICTRANSPORT').text)
        self.socialequality = float(govt.find('SOCIALEQUALITY').text)
        self.spirituality = float(govt.find('SPIRITUALITY').text)
        self.welfare = float(govt.find('WELFARE').text)


class Sectors:
    def __init__(self, elem):
        self.blackmarket = float(elem.find('BLACKMARKET').text)
        self.government = float(elem.find('GOVERNMENT').text)
        self.industry = float(elem.find('INDUSTRY').text)
        self.public = float(elem.find('PUBLIC').text)



class IssueOption:
    def __init__(self, elem, issue):
        self._issue = issue
        self.id = int(option.get('id'))
        self.text = NationStatesHTMLMess(option.text)

    def accept(self):
        return self._issue._nation._accept_issue(self._issue.id, self.id)


class Issue:
    def __init__(self, elem, nation):
        self._nation = nation
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text  # XXX html?
        self.text = NationStatesHTMLMess(elem.find('TEXT').text)
        self.author = getattr(elem.find('AUTHOR'), 'text', None)
        self.editor = getattr(elem.find('EDITOR'), 'text', None)
        self.options = [
            IssueOption(sub_elem)
            for sub_elem in elem.findall('OPTION')
        ]

    def dismiss(self):
        return self._nation._dismiss_issue(self.id)



# TODO gavote, scvote


