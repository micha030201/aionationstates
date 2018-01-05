.. intro:

Introduction
============

Installation
------------

It's literally just

.. code-block:: none

   pip install aionationstates

I hope that's exactly what you expected.

Basic usage
-----------

Here's a quick introduction to get you started

Basic initialization::

    import aionationstates
    aionationstates.set_user_agent('look ma no hands')

Nation API::

    testlandia = aionationstates.Nation('testlandia')

    await testlandia.fullname()
    # 'The Hive Mind of Testlandia'

    await testlandia.population()
    # 30087

    await testlandia.deaths()
    # {'Acts of God': 0.5,
    #  'Old Age': 93.2,
    #  'Heart Disease': 0.3,
    #  'Lost in Wilderness': 5.8,
    #  'War': 0.2}

    await testlandia.wa()
    # True

    await testlandia.lastlogin()
    # datetime.datetime(2017, 7, 14, 4, 37, 27)

    aionationstates.datetime_to_ns(await testlandia.lastlogin())
    # '2 days 11 hours ago'

    # *gasp*
    await (testlandia.leader()
           + testlandia.demonym()
           + testlandia.religion())
    # ('Meridian Zero', 'Testlandish', 'Neo-Violetism')

The Region API is quite similar::

    tnp = aionationstates.Region('the north pacific')

    await tnp.numnations()
    # 8380

    await tnp.embassyrmb()
    # <EmbassyPostingRights.EVERYBODY: 5>

