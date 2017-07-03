# TODO slots
# TODO split into submodules?

from contextlib import suppress
from collections import namedtuple
from html import unescape
from enum import Flag, Enum, auto
from functools import reduce, total_ordering
from operator import or_
# Needed for type annotations
import datetime
from typing import List, Optional, Awaitable

from aionationstates.utils import timestamp
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


class CensusPoint:  # TODO make a namedtuple
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


class Dispatch(DispatchThumbnail):  # TODO join with DispatchThumbnail
    def __init__(self, elem):
        super().__init__(elem)
        self.text = elem.find('TEXT').text

    def __repr__(self):
        return f'<Dispatch id={self.id}>'



class PollOption:
    """An option in a poll.

    Attributes:
        text: Text of the option.
        voters: Nations that picked this option.  Not normalized.
    """
    text: str
    voters: List[str]

    def __init__(self, elem):
        self.text = elem.find('OPTIONTEXT').text
        voters = elem.find('VOTERS').text  # TODO normalize?
        self.voters = voters.split(':') if voters else []


class Poll:
    """A regional poll.

    Attributes:
        id: The poll id.
        title: The poll title.  May contain HTML elements and character
            references.
        text: The poll text.  May contain HTML elements and character
            references.
        region: Region the poll was posted in.  Not normalized.
        author: Nation that posted the poll.  Not normalized.
        options: The poll options.
    """
    id: int
    title: str
    text: str
    region: str
    author: str
    start: datetime.datetime
    stop: datetime.datetime
    options: List[PollOption]

    def __init__(self, elem):
        self.id = int(elem.get('id'))
        self.title = elem.find('TITLE').text  # TODO HTML mess
        self.text = elem.find('TEXT').text  # TODO HTML mess
        self.region = elem.find('REGION').text  # TODO normalize?
        self.author = elem.find('AUTHOR').text  # TODO normalize?
        self.start = timestamp(elem.find('START').text)
        self.stop = timestamp(elem.find('STOP').text)
        self.options = [PollOption(option_elem)
                        for option_elem in elem.find('OPTIONS')]

    def __repr__(self):
        return f'<Poll id={self.id}>'



class Freedom:
    """Nation's `Freedoms`: three basic indicators of the nation's
    Civil Rights, Economy, and Political Freedom, as expressive
    adjectives.

    Attributes:
        civilrights: Nation's Civil Rights.
        economy: Nation's Economic Prosperity.
        politicalfreedom: Nation's Political Freedom.
    """
    civilrights: str
    economy: str
    politicalfreedom: str

    def __init__(self, elem):
        self.civilrights = elem.find('CIVILRIGHTS').text
        self.economy = elem.find('ECONOMY').text
        self.politicalfreedom = elem.find('POLITICALFREEDOM').text


class FreedomScores:
    """Nation's `Freedoms`: three basic indicators of the nation's
    Civil Rights, Economy, and Political Freedom, as percentages.

    Attributes:
        civilrights: Nation's Civil Rights.
        economy: Nation's Economic Prosperity.
        politicalfreedom: Nation's Political Freedom.
    """
    civilrights: int
    economy: int
    politicalfreedom: int

    def __init__(self, elem):
        self.civilrights = int(elem.find('CIVILRIGHTS').text)
        self.economy = int(elem.find('ECONOMY').text)
        self.politicalfreedom = int(elem.find('POLITICALFREEDOM').text)


class Govt:
    """Nation's government expenditure, as percentages.

    Attributes:
        administration: The percentage of nation's budget spent on
            Administration.
        defence: The percentage of nation's budget spent on
            Defence.
        education: The percentage of nation's budget spent on
            Public Education.
        environment: The percentage of nation's budget spent on
            Enviromental Protection.
        healthcare: The percentage of nation's budget spent on
            Public Healthcare.
        commerce: The percentage of nation's budget spent on
            Industry.
        internationalaid: The percentage of nation's budget spent on
            International Aid.
        lawandorder: The percentage of nation's budget spent on
            Law & Order.
        publictransport: The percentage of nation's budget spent on
            Public Transportation.
        socialequality: The percentage of nation's budget spent on
            Social Policy.
        spirituality: The percentage of nation's budget spent on
            Spirituality.
        welfare: The percentage of nation's budget spent on
            Welfare.
    """
    administration: float
    defence: float
    education: float
    environment: float
    healthcare: float
    commerce: float
    internationalaid: float
    lawandorder: float
    publictransport: float
    socialequality: float
    spirituality: float
    welfare: float

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
    """Components of a nation's economy.

    Attributes:
        blackmarket: Part of the economy taken up by Black Market.
        government: Part of the economy taken up by Government.
        industry: Part of the economy taken up by Private Industry.
        public: Part of the economy taken up by State-Owned Industry.
    """
    blackmarket: float
    government: float
    industry: float
    public: float

    def __init__(self, elem):
        self.blackmarket = float(elem.find('BLACKMARKET').text)
        self.government = float(elem.find('GOVERNMENT').text)
        self.industry = float(elem.find('INDUSTRY').text)
        self.public = float(elem.find('PUBLIC').text)


class Banner:
    """A Rift banner.

    Attributes:
        id: The banner id.
        name: The banner name.
        validity: A requirement the nation has to meet in order to get
            the banner.
    """
    id: str
    name: str
    validity: str

    def __init__(self, elem):
        self.id = elem.get('id')
        self.name = elem.find('NAME').text
        self.validity = elem.find('VALIDITY').text

    @property
    def url(self) -> str:
        """Link to the banner image."""
        return f'https://www.nationstates.net/images/banners/{self.id}.jpg'

    # TODO repr

class CustomBanner(Banner):  # TODO join with Banner
    def __init__(self, id):
        self.id = id
        self.name = 'Custom'
        self.validity = 'Reach a certain population threshold'



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
    """Change in one of the World Census scales of a nation

    Attributes:
        score: The scale score, after the change.
        change: Change of the score.
        pchange: The semi-user-friendly percentage change NationStates
            shows by default.
    """
    score: float
    change: float
    pchange: float

    def __init__(self, elem):
        super().__init__(elem)
        self.score = float(elem.find('SCORE').text)  # TODO docs score *after*
        self.change = float(elem.find('CHANGE').text)
        self.pchange = float(elem.find('PCHANGE').text)


class IssueResult:
    """Result of an issue.

    Attributes:
        happening: The issue effect line.  Not a sentence, mind you --
            it's uncapitalized and does not end with a period.
            ``None`` if the issue was dismissed.
        census: Changes in census scores of the nation.
        banners: The banners unlocked by answering the issue.
        reclassifications: WA Category and Freedoms reclassifications.
        headlines: Newspaper headlines.  NationStates returns this
            field with unexpanded macros.  I did my best to try and
            expand them all client-side, however there does not exist
            a document in which they are formally defined (that is
            sort of a pattern throughout NationStates, maybe you've
            noticed), so I can only do so much.  Please report any
            unexpanded macros you encounter as bugs.
    """
    happening: Optional[str]
    census: List[CensusScaleChange]
    banners: List[Banner]
    reclassifications: Reclassifications
    headlines: List[str]

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

        self.happening = getattr(elem.find('DESC'), 'text', None)
        self.census = [
            CensusScaleChange(sub_elem) for sub_elem
            in elem.find('RANKINGS') or ()
        ]
        self.banners = [
            # A list of ids here, but gets updated down the line to
            # contain full-blown Banner objects.
            # I don't like this design either.
            sub_elem.text for sub_elem  # TODO make less terrible
            in elem.find('UNLOCKS') or ()
        ]
        self.reclassifications = Reclassifications(
            elem.find('RECLASSIFICATIONS'))
        self.headlines = [
            sub_elem.text for sub_elem
            in elem.find('HEADLINES') or ()
        ]



class IssueOption:
    """An option of an issue.

    Attributes:
        text: The option text. May contain HTML elements and character
            references.
    """
    text: str

    def __init__(self, elem, issue):
        self._issue = issue
        self._id = int(elem.get('id'))
        self.text = elem.text

    def accept(self) -> Awaitable[IssueResult]:
        return self._issue._nation._accept_issue(self._issue.id, self._id)

    # TODO repr


class Issue:
    """An issue.

    Attributes:
        id: The issue id.
        title: The issue title.  May contain HTML elements and
            character references.
        text: The issue text.  May contain HTML elements and character
            references.
        author: Author of the issue, usually a nation.
        editor: Editor of the issue, usually a nation.
        options: Issue options.
        banners: Issue banners.
    """
    id: int
    title: str
    text: str
    author: Optional[str]
    editor: Optional[str]
    options: List[IssueOption]
    banners: List[Banner]

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
                    yield elem.find(f'PIC{x}').text
                except AttributeError:
                    break
        self.banners = list(issue_banners(elem))

    def dismiss(self) -> Awaitable[IssueResult]:
        """Dismiss the issue."""
        return self._nation._accept_issue(self.id, -1)

    # TODO repr



class Embassies:
    """Embassies of a region.

    Attributes:
        active: Normal, alive embassies.
        closing: Embassies the demolition of which has been initiated,
            but did not yet finish.
        pending: Embassies the creation of which has been initiated,
            but did not yet finish.
        invited: Embassy invitations that have not yet been processed.
        rejected: Embassy invitations that have been denied.
    """
    active: List[str]
    closing: List[str]
    pending: List[str]
    invited: List[str]
    rejected: List[str]

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
    """Authority of a Regional Officer."""
    EXECUTIVE      = X = auto()
    WORLD_ASSEMBLY = W = auto()
    APPEARANCE     = A = auto()
    BORDER_CONTROL = B = auto()
    COMMUNICATIONS = C = auto()
    EMBASSIES      = E = auto()
    POLLS          = P = auto()

    def __repr__(self):
        return f'<OfficerAuthority.{self.name}>'

def _officer_auth(string):
    """This is the best way I could find to make Flag enums work with
    individual characters as flags.
    """
    return reduce(or_, (OfficerAuthority[char] for char in string))


class RegionalOfficer:
    def __init__(self, *, nation, authority, office):
        # Not using elem here because founder/delegate stuff is spread
        # across multiple shards.
        self.nation = nation
        self.office = office
        self.authority = _officer_auth(authority)


class AppointedRegionalOfficer(RegionalOfficer):  # TODO join with RegionalOfficer
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

EmbassyPostingRights = _EmbassyPostingRightsParent(  # TODO create with a function instead
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
    """Status of a post on a Regional Message Board.

    Attributes:
        NORMAL: A regular post.
        SUPPRESSED: The post got suppressed by a regional official.
        DELETED: The post got deleted by its author.
        MODERATED: The post got suppressed by a game moderator.
    """
    NORMAL     = 0
    SUPPRESSED = 1
    DELETED    = 2
    MODERATED  = 9

    @property
    def viewable(self) -> bool:
        """Whether the post content can still be accessed.  Shortcut
        for ``PostStatus.NORMAL or PostStatus.SUPPRESSED``.
        """
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

    # TODO repr



class RegionZombie:
    def __init__(self, elem):
        self.survivors = int(elem.find('SURVIVORS').text)
        self.zombies = int(elem.find('ZOMBIES').text)
        self.dead = int(elem.find('DEAD').text)


class NationZombie:  # TODO join with RegionZombie
    def __init__(self, elem):
        super().__init__(elem)
        self.action = elem.find('ZACTION').text


# TODO gavote, scvote



