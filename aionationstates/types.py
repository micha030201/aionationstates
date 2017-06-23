# TODO slots
# TODO split into submodules?

from contextlib import suppress
from collections import namedtuple
from html import unescape
from enum import Flag, Enum, auto
from functools import reduce, total_ordering
from operator import or_

from aionationstates.utils import timestamp, banner_url
from aionationstates.ns_to_human import census_info


class RateLimitError(Exception):
    pass


class SessionConflictError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class NotFound(Exception):
    pass



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
        self.timestamp = timestamp(elem.find('TIMESTAMP').text)
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
        self.views = int(elem.find('VIEWS').text)
        self.score = int(elem.find('SCORE').text)

        created = int(elem.find('CREATED').text)
        # Otherwise it's 0 for dispatches that were never edited
        edited = int(elem.find('EDITED').text) or created
        self.created = timestamp(created)
        self.edited = timestamp(edited)

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
        self.text = elem.find('OPTIONTEXT').text
        voters = elem.find('VOTERS').text
        self.voters = voters.split(':') if voters else ()


class Poll:
    def __init__(self, elem):
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text
        self.text = elem.find('TEXT').text
        self.region = elem.find('REGION').text
        self.author = elem.find('AUTHOR').text
        self.start = timestamp(elem.find('START').text)
        self.stop = timestamp(elem.find('STOP').text)
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
        self.administration = float(elem.find('ADMINISTRATION').text)
        self.defence = float(elem.find('DEFENCE').text)
        self.education = float(elem.find('EDUCATION').text)
        self.environment = float(elem.find('ENVIRONMENT').text)
        self.healthcare = float(elem.find('HEALTHCARE').text)
        self.commerce = float(elem.find('COMMERCE').text)
        self.internationalaid = float(elem.find('INTERNATIONALAID').text)
        self.lawandorder = float(elem.find('LAWANDORDER').text)
        self.publictransport = float(elem.find('PUBLICTRANSPORT').text)
        self.socialequality = float(elem.find('SOCIALEQUALITY').text)
        self.spirituality = float(elem.find('SPIRITUALITY').text)
        self.welfare = float(elem.find('WELFARE').text)


class Sectors:
    def __init__(self, elem):
        self.blackmarket = float(elem.find('BLACKMARKET').text)
        self.government = float(elem.find('GOVERNMENT').text)
        self.industry = float(elem.find('INDUSTRY').text)
        self.public = float(elem.find('PUBLIC').text)


class Banner:
    def __init__(self, elem):
        self.id = elem.get('id')
        self.name = elem.find('NAME').text
        self.validity = elem.find('VALIDITY').text

    @property
    def url(self):
        return f'https://www.nationstates.net/images/banners/{self.id}.jpg'



class IssueOption:
    def __init__(self, elem, issue):
        self._issue = issue
        self.id = int(elem.get('id'))
        self.text = elem.text

    def accept(self):
        return self._issue._nation._accept_issue(self._issue.id, self.id)


class Issue:
    def __init__(self, elem, nation):
        self._nation = nation
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text
        self.text = elem.find('TEXT').text
        self.author = getattr(elem.find('AUTHOR'), 'text', None)
        self.editor = getattr(elem.find('EDITOR'), 'text', None)
        self.options = [
            IssueOption(sub_elem, self)
            for sub_elem in elem.findall('OPTION')
        ]
        def issue_banners(elem):
            for x in range(1, 10):  # Should be more than enough.
                try:
                    yield banner_url(elem.find(f'PIC{x}').text)
                except AttributeError:
                    break
        self.banners = list(issue_banners(elem))

    def dismiss(self):
        return self._nation._accept_issue(self.id, -1)


Reclassification = namedtuple('Reclassification', 'before after')

class Reclassifications:
    def __init__(self, elem):
        self.civilrights = self.economy = \
            self.politicalfreedom = self.govt = None
        if elem is None:
            return
        attr_names = {
            '0': 'civilrights',
            '1': 'economy',
            '2': 'politicalfreedom',
            'govt': 'govt'
        }
        for sub_elem in elem:
            setattr(
                self, attr_names[sub_elem.get('type')],
                Reclassification(
                    before=sub_elem.find('FROM').text,
                    after=sub_elem.find('TO').text
                )
            )


class CensusScaleChange(CensusScale):
    def __init__(self, elem):
        super().__init__(elem)
        self.score = float(elem.find('SCORE').text)  # TODO docs score *after*
        self.change = float(elem.find('CHANGE').text)
        self.pchange = float(elem.find('PCHANGE').text)


class IssueResult:
    def __init__(self, elem):
        with suppress(AttributeError):
            error = elem.find('ERROR').text
            if error == 'Invalid choice.':
                raise ValueError('invalid option')
            elif error == 'Issue already processed!':
                # I know it may not be obvious, but that's exactly
                # what NS is trying to say here.
                raise ValueError('invalid issue')
        assert elem.find('OK').text == '1'  # honestly no idea

        self.desc = getattr(elem.find('DESC'), 'text', None)  # TODO rename?
        self.rankings = [  # TODO rename?
            CensusScaleChange(sub_elem) for sub_elem
            in elem.find('RANKINGS') or ()
        ]
        self.unlocks = [  # TODO rename?
            banner_url(sub_elem.text) for sub_elem
            in elem.find('UNLOCKS') or ()
        ]
        self.reclassifications = Reclassifications(
            elem.find('RECLASSIFICATIONS'))
        self.headlines = [
            sub_elem.text for sub_elem
            in elem.find('HEADLINES') or ()
        ]



class Embassies:
    def __init__(self, elem):
        # I know I'm iterating through them five times; I don't care.
        self.active = [sub_elem.text for sub_elem in elem
                       if sub_elem.get('type') is None]
        self.closing = [sub_elem.text for sub_elem in elem
                        if sub_elem.get('type') == 'closing']
        self.pending = [sub_elem.text for sub_elem in elem
                        if sub_elem.get('type') == 'pending']
        self.invited = [sub_elem.text for sub_elem in elem
                        if sub_elem.get('type') == 'invited']
        self.rejected = [sub_elem.text for sub_elem in elem
                         if sub_elem.get('type') == 'rejected']



class OfficerAuthority(Flag):
    EXECUTIVE      = X = auto()
    WORLD_ASSEMBLY = W = auto()
    APPEARANCE     = A = auto()
    BORDER_CONTROL = B = auto()
    COMMUNICATIONS = C = auto()
    EMBASSIES      = E = auto()
    POLLS          = P = auto()

    def __repr__(self):
        return f'<{self.__class__.__name__}.{self.name}>'

def _officer_auth(string):
    """This is he best way I could find to make Flag enums work with
    individual characters as flags.
    """
    reduce(or_, (OfficerAuthority[char] for char in string))


class RegionalOfficer:
    def __init__(self, *, nation, authority, office):
        # Not using elem here because founder/delegate stuff is spread
        # across multiple shards.
        self.nation = nation
        self.office = office
        self.authority = _officer_auth(authority)


class AppointedRegionalOfficer(RegionalOfficer):
    def __init__(self, elem):
        self.nation = elem.find('NATION').text
        self.office = elem.find('OFFICE').text
        self.authority = _officer_auth(elem.find('AUTHORITY').text)
        self.time = self.appointed_at = timestamp(elem.find('TIME').text)
        self.by = self.appointed_by = elem.find('BY').text



@total_ordering
class _EmbassyPostingRightsParent(Enum):
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

EmbassyPostingRights = _EmbassyPostingRightsParent(
    value='EmbassyPostingRights',
    names=(
        ('NOBODY',                  1),
        # Why must you be like this NS? Why?
        # Could you not have gone for 'none'? 'dis'? 'zero'?
        # Why does it have to be '0'? Why?
        ('0',                       1),
        # '0' is not a valid identifier, and we need the values as
        # integers for comparison operations to work.
        # *sigh*
        ('DELEGATES_AND_FOUNDERS',  2),
        ('con',                     2),
        ('COMMUNICATIONS_OFFICERS', 3),
        ('com',                     3),
        ('OFFICERS',                4),
        ('off',                     4),
        ('EVERYBODY',               5),
        ('all',                     5),
    )
)



class PostStatus(Enum):
    NORMAL     = 0
    SUPPRESSED = 1
    DELETED    = 2
    MODERATED  = 9
    @property
    def viewable(self):
        return self.value in (0, 1)


class Post:
    def __init__(self, elem):
        self.id = int(elem.get('id'))
        self.timestamp = timestamp(elem.find('TIMESTAMP').text)
        self.nation = self.author = elem.find('NATION').text
        self.status = PostStatus(int(elem.find('STATUS').text))
        self.message = self.text = elem.find('MESSAGE').text

        likers_elem = elem.find('LIKERS')
        self.likers = likers_elem.text.split(':') if likers_elem else ()
        suppressor_elem = elem.find('SUPPRESSOR')
        self.suppressor = suppressor_elem.text if suppressor_elem else None



class RegionZombie:
    def __init__(self, elem):
        self.survivors = int(elem.find('SURVIVORS').text)
        self.zombies = int(elem.find('ZOMBIES').text)
        self.dead = int(elem.find('DEAD').text)


class NationZombie(RegionZombie):
    def __init__(self, elem):
        super().__init__(elem)
        self.action = elem.find('ZACTION').text


# TODO gavote, scvote



