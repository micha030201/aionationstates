import html
from itertools import count
from asyncio import sleep
from contextlib import suppress

from aionationstates.utils import normalize, timestamp
from aionationstates.types import (
    EmbassyPostingRights, Officer, Authority, Embassies, Poll, Post)
from aionationstates.session import Session, api_query
from aionationstates.shards import NationRegion
import aionationstates


class Region(NationRegion, Session):
    """A class to interact with the NationStates Region API.

    Attributes
    ----------
    id : str
        The defining characteristic of a region, its normalized name.
        No two regions share the same id, and no one id is shared by
        multiple regions.
    """

    def __init__(self, name):
        self.id = normalize(name)

    def _call_api(self, params, *args, **kwargs):
        params['region'] = self.id
        return super()._call_api(*args, params=params, **kwargs)


    @property
    def url(self):
        """str: URL of the region."""
        return f'https://www.nationstates.net/region={self.id}'

    @api_query('name')
    async def name(self, root):
        """Name of the region, with proper capitalization.

        Returns
        -------
        an :class:`ApiQuery` of str
        """
        return root.find('NAME').text

    @api_query('flag')
    async def flag(self, root):
        """URL of the region's flag.

        Returns
        -------
        an :class:`ApiQuery` of str
        """
        return root.find('FLAG').text

    @api_query('factbook')
    async def factbook(self, root):
        """Region's World Factbook Entry.

        Returns
        -------
        an :class:`ApiQuery` of str
        """
        # This lib might have been a mistake, but the line below
        # definitely isn't.
        return html.unescape(html.unescape(root.find('FACTBOOK').text))

    @api_query('power')
    async def power(self, root):
        """An adjective describing region's power on the interregional
        scene.

        Returns
        -------
        an :class:`ApiQuery` of str
        """
        return root.find('POWER').text

    @api_query('delegatevotes')
    async def delegatevotes(self, root):
        """Number of the World Assembly votes the region's Delegate
        has.

        Returns
        -------
        an :class:`ApiQuery` of int
        """
        return int(root.find('DELEGATEVOTES').text)

    @api_query('numnations')
    async def numnations(self, root):
        """The number of nations in the region.

        Returns
        -------
        an :class:`ApiQuery` of int
        """
        return int(root.find('NUMNATIONS').text)

    @api_query('foundedtime')
    async def founded(self, root):
        """When the region was founded.

        Returns
        -------
        an :class:`ApiQuery` of a naive UTC :class:`datetime.datetime`
        """
        return timestamp(root.find('FOUNDEDTIME'))

    @api_query('nations')
    async def nations(self, root):
        """All the nations in the region.

        Returns
        -------
        an :class:`ApiQuery` of a list of :class:`Nation` objects
        """
        text = root.find('NATIONS').text
        return ([aionationstates.Nation(n) for n in text.split(':')]
                if text else [])

    @api_query('embassies')
    async def embassies(self, root):
        """Embassies the region has.

        Returns
        -------
        an :class:`ApiQuery` of :class:`Embassies`
        """
        return Embassies(root.find('EMBASSIES'))

    @api_query('embassyrmb')
    async def embassyrmb(self, root):
        """Posting rights for members the of embassy regions.

        Returns
        -------
        an :class:`ApiQuery` of :class:`EmbassyPostingRights`
        """
        return EmbassyPostingRights._from_ns(root.find('EMBASSYRMB').text)

    @api_query('delegate')
    async def delegate(self, root):
        """Regional World Assembly Delegate.

        Returns
        -------
        an :class:`ApiQuery` of :class:`Nation`
        an :class:`ApiQuery` of None
            If the region has no delegate.
        """
        nation = root.find('DELEGATE').text
        if nation == '0':
            return None
        return aionationstates.Nation(nation)

    @api_query('delegateauth')
    async def delegateauth(self, root):
        """Regional World Assembly Delegate's authority.  Always set,
        no matter if the region has a delegate or not.

        Returns
        -------
        an :class:`ApiQuery` of :class:`Authority`
        """
        return Authority._from_ns(root.find('DELEGATEAUTH').text)

    @api_query('founder')
    async def founder(self, root):
        """Regional Founder.  Returned even if the nation has ceased to
        exist.

        Returns
        -------
        an :class:`ApiQuery` of :class:`Nation`
        an :class:`ApiQuery` of None
          If the region is Game-Created and doesn't have a founder.
        """
        nation = root.find('FOUNDER').text
        if nation == '0':
            return None
        return aionationstates.Nation(nation)

    @api_query('founderauth')
    async def founderauth(self, root):
        """Regional Founder's authority.  Always set,
        no matter if the region has a founder or not.

        Returns
        -------
        an :class:`ApiQuery` of :class:`Authority`
        """
        return Authority._from_ns(root.find('FOUNDERAUTH').text)

    @api_query('officers')
    async def officers(self, root):
        """Regional Officers.  Does not include the Founder or
        the Delegate, unless they have additional litles as Officers.
        In the correct order.

        Returns
        -------
        an :class:`ApiQuery` of a list of :class:`Officer`
        """
        officers = sorted(
            root.find('OFFICERS'),
            # I struggle to say what else this tag would be useful for.
            key=lambda elem: int(elem.find('ORDER').text)
        )
        return [Officer(elem) for elem in officers]

    @api_query('tags')
    async def tags(self, root):
        """Tags the region has.

        Returns
        -------
        an :class:`ApiQuery` of a list of str
        """
        return [elem.text for elem in root.find('TAGS')]

    @api_query('poll')
    async def poll(self, root):
        """Current regional poll.

        Returns
        -------
        an :class:`ApiQuery` of :class:`Poll`
        """
        elem = root.find('POLL')
        return Poll(elem) if elem else None

    # Messages interface:

    def _get_messages(self, *, limit=100, offset=0, fromid=None):
        params = {'limit': str(limit), 'offset': str(offset)}
        if fromid is not None:
            params['fromid'] = str(fromid)

        @api_query('messages', **params)
        async def result(_, root):
            return [Post(elem) for elem in root.find('MESSAGES')]
        return result(self)

    async def messages(self):
        """Iterate through RMB posts from newest to oldest.

        Returns
        -------
        an asynchronous generator that yields :class:`Post`
        """
        # Messages may be posted on the RMB while the generator is running.
        oldest_id_seen = float('inf')
        for offset in count(step=100):
            posts_bunch = await self._get_messages(offset=offset)
            for post in reversed(posts_bunch):
                if post.id < oldest_id_seen:
                    yield post
            oldest_id_seen = posts_bunch[0].id
            if len(posts_bunch) < 100:
                break

    async def new_messages(self, poll_period=30, *, fromid=None):
        """New messages on the Regional Message Board::

            tnp = region('The North Pacific')
            async for post in tnp.new_messages():
                # Your processing code here
                print(post.text)  # As an example

        Guarantees that:

        * Every post is generated from the moment the generator is started;
        * No post is generated more than once;
        * Posts are generated in order from oldest to newest.

        Parameters
        ----------
        poll_period : int
            How long to wait between requesting the next bunch of
            posts, in seconds.  Ignored while catching up to the end
            of the Message Board, meaning that no matter how long of a
            period you set you will never encounter a situation where
            posts are made faster than the generator can deliver them.

            Note that, regardless of the ``poll_period`` you set, all
            of the code in your loop body still has to execute (possibly
            several times) before a new bunch of posts can be
            requested.  Consider wrapping your post-processing code
            in a coroutine and launching it as a task from the loop body
            if you suspect this might be an issue.
        fromid : int
            Request posts starting with the one with this id, as
            as opposed to the last one at the time.  Useful if you
            need to avoid losing posts between restarts.  Set to `1`
            to request the entire RMB history chronologically.

        Returns
        -------
        an asynchronous generator that yields :class:`Post`
        """
        if fromid is not None:
            # fromid of 0 gets ignored by NS
            fromid = 1 if fromid == 0 else fromid
        else:
            try:
                # We only need the posts from this point forwards
                fromid = (await self._get_messages(limit=1))[0].id + 1
            except IndexError:
                # Empty RMB
                fromid = 1
            # Sleep before the loop body to avoid wasting the first request.
            # We only want to apply this "optimization" if fromid was not
            # specified, as only then we know for sure we're at the end of the
            # RMB.
            await sleep(poll_period)

        while True:
            posts = await self._get_messages(fromid=fromid)

            with suppress(IndexError):
                fromid = posts[-1].id + 1

            for post in posts:
                yield post

            if len(posts) < 100:
                await sleep(poll_period)

    # TODO: history, messages
