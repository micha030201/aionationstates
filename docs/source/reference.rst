Reference
=========

Ratelimiting
------------

Ratelimiting is handled automatically, with no (clean) way to override the ratelimiter's behavior. The latter part will change in later versions.

Combining Shards
----------------

As you are probably aware, NationStates provides a way to request multiple shards for the (ratelimit) cost of one. That is quite a useful feature, and this class has been designed specifically to take full advantage of it.

.. automodule:: aionationstates

.. autoclass:: ApiQuery


NationStates Interaction Objects
--------------------------------

Objects to interact with NationStates web interface and API.

You should not build these objects yourself. Instead, use the following:

.. data:: world

    For the :class:`World` object;

.. autofunction:: nation

    To construct either a :class:`Nation` object, or :class:`NationControl` if `password` or `autologin` is provided; and

.. function:: region(name)

    To construct a :class:`Region` object.

------

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

.. autoclass:: World()
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

    .. automethod:: tgqueue

    .. automethod:: census

    .. automethod:: censushistory

    .. automethod:: happenings

    .. automethod:: new_happenings


Data Classes
------------

.. autoclass:: CensusScaleCurrent()

.. autoclass:: CensusScaleHistory()

.. autoclass:: CensusPoint()

.. autoclass:: ScaleInfo()

.. autoclass:: Dispatch()

.. autoclass:: Poll()

.. autoclass:: PollOption()

.. autoclass:: Freedom()

.. autoclass:: FreedomScores()

.. autoclass:: Govt()

.. autoclass:: Sectors()

.. autoclass:: Policy()

.. autoclass:: Banner()

.. autoclass:: Issue()

.. autoclass:: IssueOption()

.. autoclass:: IssueResult()

.. autoclass:: CensusScaleChange()

.. autoclass:: Reclassifications()

.. autoclass:: Reclassification()

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



.. autoclass:: UnrecognizedHappening()

.. autoclass:: Move()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: Founding()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: CTE()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: Legislation()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: FlagChange()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: SettingsChange()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: DispatchPublication()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: WorldAssemblyApplication()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: WorldAssemblyAdmission()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: WorldAssemblyResignation()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: DelegateChange()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: CategoryChange()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: BannerCreation()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyConstructionRequest()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyConstructionConfirmation()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyConstructionRequestWithdrawal()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyConstructionAbortion()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyClosureOrder()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyEstablishment()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EmbassyCancellation()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: Endorsement()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: EndorsementWithdrawal()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: PollCreation()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: PollDeletion()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: ZombieCureAction()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: ZombieKillAction()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.

.. autoclass:: ZombieInfectAction()

    This is a subclass of :class:`UnrecognizedHappening`, meaning all of the standard happening attributes are present as well.


Exceptions
----------

.. autoexception:: RateLimitError

.. autoexception:: SessionConflictError

.. autoexception:: AuthenticationError

.. autoexception:: NotFound



