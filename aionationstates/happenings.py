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
    """A happening of a nation moving regions."""

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
    """A happening of a nation being founded."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match('@@(.+?)@@ was founded in %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region = aionationstates.Region(match.group(2))


class CTE(UnrecognizedHappening):
    """A happening of a nation ceasing to exist."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match('@@(.+?)@@ ceased to exist in %%(.+?)%%', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.region = aionationstates.Region(match.group(2))


class Legislation(UnrecognizedHappening):
    """A happening of a nation answering an issue."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match(
            r'Following new legislation in @@(.+?)@@, (.+)\.', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))
        self.effect_line = match.group(2)


class FlagChange(UnrecognizedHappening):
    """A happening of a nation altering its flag."""

    def __init__(self, elem):
        super().__init__(elem)
        match = re.match('@@(.+?)@@ altered its national flag', self.text)
        if not match:
            raise ValueError
        self.nation = aionationstates.Nation(match.group(1))


class SettingsChange(UnrecognizedHappening):
    """A happening of a nation modifying its customizeable fields."""

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


def process(elem):
    with suppress(ValueError):
        return Move(elem)
    with suppress(ValueError):
        return Founding(elem)
    with suppress(ValueError):
        return CTE(elem)
    with suppress(ValueError):
        return Legislation(elem)
    with suppress(ValueError):
        return FlagChange(elem)
    with suppress(ValueError):
        return SettingsChange(elem)
    # TODO logging
    return UnrecognizedHappening(elem)

