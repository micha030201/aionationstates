Happenings
==========

.. module:: aionationstates.happenings

This module contains a parser of NationStates' Happenings, with the strong
intention of being both complete and convenient.

This page describes how happenings are parsed and processed; to subscribe to the
happening feeds use the World methods :meth:`~aionationstates.World.happenings`
and :meth:`~aionationstates.World.new_happenings`.

Examples
--------

Greet every nation that moves to a new region::

    async for happening in \
            aionationstates.world.new_happenings(filters=['move']):
        if type(happening) is aionationstates.happenings.Move:
            region_name = await happening.new_region.name()
            nation_name = await happening.agent.name()
            print(f'Welcome to {region_name}, {nation_name}!')

Detect regional currency adoption::

    region_name = 'the pacific'
    regional_currency = 'Denarius'

    async for happening in aionationstates.world.new_happenings(
            filters=['change'], regions=[region_name]):
        if type(happening) is aionationstates.happenings.SettingsChange:
            if happening.changes.get('currency') == regional_currency:
                nation_name = await happening.agent.name()
                print(f'{nation_name} has adopted {regional_currency}!')

Detect embassies built and closed::

    async for happening in \
            aionationstates.world.new_happenings(filters=['embassy']):
        region_names = await asyncio.gather(*[
            region.name() for region in happening.regions])
        if type(happening) is aionationstates.happenings.EmbassyEstablishment:
            print('{} ❤️ {}'.format(*region_names))
        elif type(happening) is aionationstates.happenings.EmbassyCancellation:
            print('{} 💔 {}'.format(*region_names))


Design considerations
---------------------

Parsing happenings can serve a variety of use-cases. You may want to maintain an
endorsement graph for your region, which would require very specific handling of
a handful of happening types (notably :class:`Endorsement`,
:class:`EndorsementWithdrawal`, :class:`Move`, and :class:`CTE`) or you might be
after graphing game activity over time, and thus need to process a broad
spectrum of happenings very generically. This module seeks to accomodate both
the precise and broad use-cases.

Base classes
------------

Starting with the cold hard truth--

.. autoclass:: UnrecognizedHappening()

Now let's look at how this module functions when it works as intended, shall we?

On the most basic level, all happenings divide into two groups:

.. autoclass:: Action()
   :show-inheritance:

.. autoclass:: Consequence()
   :show-inheritance:

The rest of data classes in this module inherit from the classes above.

Additionally, there are generalizable characteristics some happenings share,
that can't be separated well into categories:

.. autoclass:: Regional()
   :show-inheritance:

.. autoclass:: Affecting()
   :show-inheritance:

Base classes unifying a set of caracteristics like these can be seen throughout
the rest of the module.

Categories of happenings
------------------------

Embassies
^^^^^^^^^

.. autoclass:: Embassy()
   :show-inheritance:

.. autoclass:: EmbassyEstablishment()
   :show-inheritance:

.. autoclass:: EmbassyCancellation()
   :show-inheritance:

.. autoclass:: EmbassyOrder()
   :show-inheritance:

.. autoclass:: EmbassyConstructionRequest()
   :show-inheritance:

.. autoclass:: EmbassyConstructionConfirmation()
   :show-inheritance:

.. autoclass:: EmbassyConstructionRequestWithdrawal()
   :show-inheritance:

.. autoclass:: EmbassyConstructionAbortion()
   :show-inheritance:

.. autoclass:: EmbassyClosureOrder()
   :show-inheritance:

Administration of a region
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: RegionalAdministrative()
   :show-inheritance:

.. autoclass:: DelegateChange()
   :show-inheritance:

.. autoclass:: OfficerAppointment()
   :show-inheritance:

.. autoclass:: OfficerDismissal()
   :show-inheritance:

.. autoclass:: DelegateModification()
   :show-inheritance:

.. autoclass:: OfficerModification()
   :show-inheritance:

.. autoclass:: PollCreation()
   :show-inheritance:

.. autoclass:: PollDeletion()
   :show-inheritance:

Z-Day
^^^^^

.. autoclass:: Zombie()
   :show-inheritance:

.. autoclass:: ZombieCure()
   :show-inheritance:

.. autoclass:: ZombieKill()
   :show-inheritance:

.. autoclass:: ZombieInfect()
   :show-inheritance:

.. autoclass:: ZombieBorderControlActivation()
   :show-inheritance:

.. autoclass:: ZombieBorderControlDeactivation()
   :show-inheritance:

World Assembly
^^^^^^^^^^^^^^

.. autoclass:: WorldAssembly()
   :show-inheritance:

.. autoclass:: WorldAssemblyApplication()
   :show-inheritance:

.. autoclass:: WorldAssemblyAdmission()
   :show-inheritance:

.. autoclass:: WorldAssemblyResignation()
   :show-inheritance:

The rest
^^^^^^^^

.. autoclass:: Move()
   :show-inheritance:

.. autoclass:: Founding()
   :show-inheritance:

.. autoclass:: Refounding()
   :show-inheritance:

.. autoclass:: CTE()
   :show-inheritance:

.. autoclass:: Legislation()
   :show-inheritance:

.. autoclass:: FlagChange()
   :show-inheritance:

.. autoclass:: SettingsChange()
   :show-inheritance:

.. autoclass:: DispatchPublication()
   :show-inheritance:

.. autoclass:: CategoryChange()
   :show-inheritance:

.. autoclass:: BannerCreation()
   :show-inheritance:

.. autoclass:: Endorsement()
   :show-inheritance:

.. autoclass:: EndorsementWithdrawal()
   :show-inheritance:

