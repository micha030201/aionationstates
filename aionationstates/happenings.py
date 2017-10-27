"""Digest all NationStates happenings, extracting their type and useful data.

A great undertaking to be sure.
"""

import re
import html
import datetime
from contextlib import suppress

from aionationstates.utils import timestamp, unscramble_encoding
import aionationstates


class UnrecognizedHappening:
    """A happening that wasn't recognized by the system.

    Most likely cause of this is the futility of this measly effort
    against the inescapable and ever-growing chaos of our Universe.

    Not necessarily an error in the parsing system, rather an indicator
    of its incompleteness.

    Note that all the other classes in the `happenings` module inherit
    from this import class, so all the attributes listed below are
    present on them as well.

    Attributes:
        id: The happening id.  `None` if the happening is from a national or
            regional archive.
        timestamp: Time of the happening.
        text: The happening text.
    """

    def __init__(self, params):
        self.id, self.timestamp, self.text = params

    def __repr__(self):
        return f'<Happening #{self.id}>'


class Move(UnrecognizedHappening):
    """A nation moving regions."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            r'@@(.+?)@@ relocated from %%(.+?)%% to %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region_from = aionationstates.Region(match.group(2))
        self.region_to = aionationstates.Region(match.group(3))


class Founding(UnrecognizedHappening):
    """A nation being founded."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match('@@(.+?)@@ was founded in %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region = aionationstates.Region(match.group(2))


class CTE(UnrecognizedHappening):
    """A nation ceasing to exist."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match('@@(.+?)@@ ceased to exist in %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region = aionationstates.Region(match.group(2))


class Legislation(UnrecognizedHappening):
    """A nation answering an issue."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            r'Following new legislation in @@(.+?)@@, (.+)\.', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.effect_line = match.group(2)


class FlagChange(UnrecognizedHappening):
    """A nation altering its flag."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match('@@(.+?)@@ altered its national flag', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class SettingsChange(UnrecognizedHappening):
    """A nation modifying its customizeable fields."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ changed its national', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.changes = {}

        # If you harbor any sort of motivation to refactor this, feel free.
        index = self.text.index('@@ changed its national') + 23
        text = 'its' + self.text[index:]

        for substr in text.split(','):
            # none of the fields are supposed to contain quotes
            match = re.search('its (.+?) to "(.+?)"', substr)
            value = unscramble_encoding(html.unescape(match.group(2)))
            self.changes[match.group(1)] = value


class DispatchPublication(UnrecognizedHappening):
    """A dispatch being published.

    In case you're wondering, deleting a dispatch doesn't produce a happening.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            r'@@(.+?)@@ published "<a href="page=dispatch/id=(.+?)">(.+?)</a>" \((.+?): (.+?)\).',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.dispatch_id = int(match.group(2))
        self.title = unscramble_encoding(html.unescape(match.group(3)))
        self.category = match.group(4)
        self.subcategory = match.group(5)

    def dispatch(self):
        """Request the full dispatch."""
        return aionationstates.world.dispatch(self.dispatch_id)


class WorldAssemblyApplication(UnrecognizedHappening):
    """A nation applying to join the World Assembly."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ applied to join the World Assembly.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class WorldAssemblyAdmission(UnrecognizedHappening):
    """A nation being admitted to the World Assembly."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ was admitted to the World Assembly.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class WorldAssemblyResignation(UnrecognizedHappening):
    """A nation resigning from World Assembly."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ resigned from the World Assembly.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class DelegateChange(UnrecognizedHappening):
    """A region changing World Assembly Delegates.

    Note that NationStates spreads this out to three distinct happenings:
        - delegates changing;
        - a nation taking the free delegate position; and
        - a delegate being removed, leaving the position empty.

    As I believe this to be superfluous, this class represents all three.
    In case either the old of new delegate is missing, the corresponding
    attribute will ne `None`.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ seized the position of %%(.+?)%% WA Delegate from @@(.+?)@@.',
            self.text
        )
        if match:
            self.new_delegate = aionationstates.Nation(match.group(1))
            self.region = aionationstates.Region(match.group(2))
            self.old_delegate = aionationstates.Nation(match.group(3))
            return

        match = re.match(
            '@@(.+?)@@ became WA Delegate of %%(.+?)%%.',
            self.text
        )
        if match:
            self.new_delegate = aionationstates.Nation(match.group(1))
            self.region = aionationstates.Region(match.group(2))
            self.old_delegate = None
            return

        match = re.match(
            '@@(.+?)@@ lost WA Delegate status in %%(.+?)%%.',
            self.text
        )
        if match:
            self.old_delegate = aionationstates.Nation(match.group(1))
            self.region = aionationstates.Region(match.group(2))
            self.new_delegate = None
            return

        raise ValueError


class CategoryChange(UnrecognizedHappening):
    """A nation being reclassified to a different WA Category."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ was reclassified from "(.+?)" to "(.+?)".',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.category_before = match.group(2)
        self.category_after = match.group(3)


class BannerCreation(UnrecognizedHappening):
    """A nation creating a custom banner."""

    def __init__(self, params):
        super().__init__(params)
        match = re.match('@@(.+?)@@ created a custom banner.', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class EmbassyConstructionRequest(UnrecognizedHappening):
    """A nation proposing construction of embassies between two regions.

    Attributes
    ----------
    nation : :class:`Nation`
        Nation performing the action.
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening, but the
        first one appears to be one the request was sent from.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ proposed constructing embassies between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.regions = (
            aionationstates.Region(match.group(2)),
            aionationstates.Region(match.group(3))
        )


class EmbassyConstructionConfirmation(UnrecognizedHappening):
    """A nation accepting a request to construct embassies between two regions.

    Attributes
    ----------
    nation : :class:`Nation`
        Nation performing the action.
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening, but the
        first one appears to be one the request was accepted from.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ agreed to construct embassies between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.regions = (
            aionationstates.Region(match.group(2)),
            aionationstates.Region(match.group(3))
        )


class EmbassyConstructionRequestWithdrawal(UnrecognizedHappening):
    """A nation withdrawing a request to construct embassies between two regions.

    Attributes
    ----------
    nation : :class:`Nation`
        Nation performing the action.
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ withdrew a request for embassies between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.regions = (
            aionationstates.Region(match.group(2)),
            aionationstates.Region(match.group(3))
        )


class EmbassyConstructionAbortion(UnrecognizedHappening):
    """A nation aborting construction of embassies between two regions.

    Attributes
    ----------
    nation : :class:`Nation`
        Nation performing the action.
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ aborted construction of embassies between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.regions = (
            aionationstates.Region(match.group(2)),
            aionationstates.Region(match.group(3))
        )


class EmbassyClosureOrder(UnrecognizedHappening):
    """A nation ordering closure of embassies between two regions.

    Attributes
    ----------
    nation : :class:`Nation`
        Nation performing the action.
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            '@@(.+?)@@ ordered the closure of embassies between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.regions = (
            aionationstates.Region(match.group(2)),
            aionationstates.Region(match.group(3))
        )


class EmbassyEstablishment(UnrecognizedHappening):
    """Embassy being established between two regions.

    Attributes
    ----------
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            'Embassy established between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.regions = (
            aionationstates.Region(match.group(1)),
            aionationstates.Region(match.group(2))
        )


class EmbassyCancellation(UnrecognizedHappening):
    """Embassy being cancelled between two regions.

    Attributes
    ----------
    regions : tuple of two :class:`Region` objects
        Regions involved in the embassy request.  The order is not
        guaranteed, as it mimics the one from the happening.
    """

    def __init__(self, params):
        super().__init__(params)
        match = re.match(
            'Embassy cancelled between %%(.+?)%% and %%(.+?)%%.',
            self.text
        )
        if not match:
            raise ValueError
        self.regions = (
            aionationstates.Region(match.group(1)),
            aionationstates.Region(match.group(2))
        )



def process(params):
    # Call ElementTree methods only once, to get a bit of extra performance.
    try:
        params_id = int(params.get('id'))
    except TypeError:
        params_id = None
    params_timestamp = timestamp(params.find('TIMESTAMP').text)
    params_text = params.findtext('TEXT')
    params = (params_id, params_timestamp, params_text)

    possible_classes = (
        Move,
        Founding,
        CTE,
        Legislation,
        FlagChange,
        SettingsChange,
        DispatchPublication,
        WorldAssemblyApplication,
        WorldAssemblyAdmission,
        WorldAssemblyResignation,
        DelegateChange,
        CategoryChange,
        BannerCreation,
        EmbassyConstructionRequest,
        EmbassyConstructionConfirmation,
        EmbassyConstructionRequestWithdrawal,
        EmbassyConstructionAbortion,
        EmbassyClosureOrder,
        EmbassyEstablishment,
        EmbassyCancellation,
    )
    for cls in possible_classes:
        with suppress(ValueError):
            return cls(params)
    # TODO logging
    return UnrecognizedHappening(params)
