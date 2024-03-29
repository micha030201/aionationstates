Reference
=========

Ratelimiting
------------

Ratelimiting is handled automatically, with no (clean) way to override the
ratelimiter's behavior. The latter part may change in later versions.

Combining Shards
----------------

As you are probably aware, NationStates provides a way to request multiple
shards for the (ratelimit) cost of one. That is quite a useful feature, and this
class has been designed specifically to take full advantage of it.

.. automodule:: aionationstates

.. autoclass:: ApiQuery()


That's all well and good, but how do I actually request the shards I need?
--------------------------------------------------------------------------

Nation shards
^^^^^^^^^^^^^

.. autoclass:: Nation
   :no-members:

   .. autoattribute:: url

   .. automethod:: name

   .. automethod:: type

   .. automethod:: fullname

   .. automethod:: motto

   .. automethod:: category

   .. automethod:: region

   .. automethod:: animal

   .. automethod:: currency

   .. automethod:: demonym

   .. automethod:: demonym2

   .. automethod:: demonym2plural

   .. automethod:: flag

   .. automethod:: majorindustry

   .. automethod:: influence

   .. automethod:: leader

   .. automethod:: capital

   .. automethod:: religion

   .. automethod:: admirable

   .. automethod:: animaltrait

   .. automethod:: crime

   .. automethod:: govtdesc

   .. automethod:: industrydesc

   .. automethod:: notable

   .. automethod:: sensibilities

   .. automethod:: population

   .. automethod:: gdp

   .. automethod:: founded

   .. automethod:: firstlogin

   .. automethod:: lastlogin

   .. automethod:: wa

   .. automethod:: freedom

   .. automethod:: freedomscores

   .. automethod:: govt

   .. automethod:: deaths

   .. automethod:: endorsements

   .. automethod:: legislation

   .. automethod:: sectors

   .. automethod:: dispatchlist

   .. automethod:: policies

   .. automethod:: zombie

   .. automethod:: banners

   .. automethod:: census

   .. automethod:: censushistory

   .. automethod:: happenings

   .. automethod:: description

   .. automethod:: verification_url

   .. automethod:: verify

.. autoclass:: NationControl
   :no-members:

   .. automethod:: issues

   .. automethod:: message

Region shards
^^^^^^^^^^^^^

.. autoclass:: Region
   :no-members:

   .. autoattribute:: url

   .. automethod:: name

   .. automethod:: flag

   .. automethod:: factbook

   .. automethod:: power

   .. automethod:: delegatevotes

   .. automethod:: numnations

   .. automethod:: founded

   .. automethod:: nations

   .. automethod:: embassies

   .. automethod:: embassyrmb

   .. automethod:: delegate

   .. automethod:: delegateauth

   .. automethod:: founder

   .. automethod:: founderauth

   .. automethod:: officers

   .. automethod:: tags

   .. automethod:: zombie

   .. automethod:: poll

   .. automethod:: census

   .. automethod:: censushistory

   .. automethod:: happenings

World shards
^^^^^^^^^^^^

.. autoclass:: _World()
   :no-members:

   .. automethod:: featuredregion

   .. automethod:: newnations

   .. automethod:: nations

   .. automethod:: numnations

   .. automethod:: regions

   .. automethod:: numregions

   .. automethod:: regionsbytag

   .. automethod:: dispatch

   .. automethod:: dispatchlist

   .. automethod:: poll

   .. automethod:: banner

   .. automethod:: tgqueue

   .. automethod:: census

   .. automethod:: censushistory

   .. automethod:: happenings

   .. automethod:: new_happenings

World Assembly shards
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: _WA()
   :inherited-members:

.. autoclass:: _WACouncil()
   :inherited-members:


Data Classes
------------

.. autoclass:: CensusScaleCurrent()

.. autoclass:: CensusScaleHistory()

.. autoclass:: CensusPoint()

.. autoclass:: ScaleInfo()

.. autoclass:: DispatchThumbnail()

.. autoclass:: Dispatch()

.. autoclass:: Poll()

.. autoclass:: PollOption()

.. autoclass:: WAMembership()
   :show-inheritance:

.. autoclass:: Policy()

.. autoclass:: Banner()

.. autoclass:: Issue()

.. autoclass:: IssueOption()

.. autoclass:: IssueResult()

.. autoclass:: CensusScaleChange()

.. autoclass:: Embassies()

.. autoclass:: Officer()

.. autoclass:: Authority()
   :show-inheritance:

.. autoclass:: EmbassyPostingRights()
   :show-inheritance:

.. autoclass:: Post()

.. autoclass:: PostStatus()
   :show-inheritance:

.. autoclass:: Zombie()

.. autoclass:: TGQueue()

.. autoclass:: ArchivedHappening()

.. autoclass:: Proposal()
   :inherited-members:

.. autoclass:: Resolution()
   :inherited-members:

.. autoclass:: VoteAction
   :show-inheritance:

.. autoclass:: DelegateVoteLogEntry

.. autoclass:: VoteTrackEntry

.. autoclass:: ResolutionAtVote()
   :inherited-members:

Exceptions
----------

.. autoexception:: NationStatesError

.. autoexception:: RateLimitError

.. autoexception:: SessionConflictError

.. autoexception:: AuthenticationError

.. autoexception:: NotFound



