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

    # XXX Having this code run every time we *try* to parse a happening, not
    # just once per a *successful* parsing operation, MAY be a performance
    # concern.  Some benchmarking is required.
    def __init__(self, elem):
        try:
            self.id = int(elem.get('id'))
        except TypeError:
            self.id = None
        self.timestamp = timestamp(elem.find('TIMESTAMP').text)
        self.text = elem.findtext('TEXT')

    def __repr__(self):
        return f'<Happening #{self.id}>'


class Move(UnrecognizedHappening):
    """A nation moving regions."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match(
            r'@@(.+?)@@ relocated from %%(.+?)%% to %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region_from = aionationstates.Region(match.group(2))
        self.region_to = aionationstates.Region(match.group(3))


class Founding(UnrecognizedHappening):
    """A nation being founded."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match('@@(.+?)@@ was founded in %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region = aionationstates.Region(match.group(2))


class CTE(UnrecognizedHappening):
    """A nation ceasing to exist."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match('@@(.+?)@@ ceased to exist in %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region = aionationstates.Region(match.group(2))


class Legislation(UnrecognizedHappening):
    """A nation answering an issue."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match(
            r'Following new legislation in @@(.+?)@@, (.+)\.', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.effect_line = match.group(2)


class FlagChange(UnrecognizedHappening):
    """A nation altering its flag."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match('@@(.+?)@@ altered its national flag', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class SettingsChange(UnrecognizedHappening):
    """A nation modifying its customizeable fields."""

    def __init__(self, elem):
        super().__init__(elem)
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

    def __init__(self, elem):
        super().__init__(elem)
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

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match(
            '@@(.+?)@@ applied to join the World Assembly.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class WorldAssemblyAdmission(UnrecognizedHappening):
    """A nation being admitted to the World Assembly."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match(
            '@@(.+?)@@ was admitted to the World Assembly.',
            self.text
        )
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class WorldAssemblyResignation(UnrecognizedHappening):
    """A nation resigning from World Assembly."""

    def __init__(self, elem):
        super().__init__(elem)
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

    def __init__(self, elem):
        super().__init__(elem)
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



def process(elem):
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
    )
    for cls in possible_classes:
        with suppress(ValueError):
            return cls(elem)
    # TODO logging
    return UnrecognizedHappening(elem)
