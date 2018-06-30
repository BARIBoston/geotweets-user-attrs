geotweets-attrs
---------------

This repository contains the main script ``main.py`` for generating summary
files from user files from the geotweets database. ``main.py`` pulls attribute
functions from ``attrs.py`` and optionally any other file that you wish
to include.

**TODO**
* Multiprocessing
* Maybe cluster computing with Celery

usage
-----

.. code-block:: sh

    ./main.py [list of user files]

Where *list of user files* is a list of gzip-compressed files, with each line
being the JSON of a single tweet by a user.

For programmatic usage:

.. code-block:: python

    import sys
    import attrs

    s = SummaryBuilder()

    # automatically load attribute extractors from a module
    s.read_attrs_from_module(attrs)

    # add a custom attribute extractor
    attrs_most_frequent_multiple = attrs.setup_most_frequent({
        "name": ["user", "name"],
        "username": ["user", "screen_name"],
    })
    s.add_attr_function(attrs_most_frequent_multiple)

    for user in sys.argv[1:]:
        s.process_user(user)

    df = s.to_df()      # for a Pandas DataFrame
    s.to_csv("out.csv") # to write to disk

adding attributes
-----------------

Additional attributes can be defined by attribute functions, which calculate
values and return a dict where the keys are the names of the attributes and
the values are the values of the attributes. For example:

.. code-block:: python

    {
        "user": "TestUser",
        "n_tweets": 1234,
        "first_tweet_timestamp": 1530389606.048026
    }

Attribute functions can be added with ``SummaryBuilder.add_attr_function``.
Alternatively, they can be automatically harvested from a module with
``SummaryBuilder.read_attrs_from_module``, which automatically adds all
functions that begin with ``attr_`` and ``attrs_``

Attribute functions have the following form:

.. code-block:: python

    def attr_n_tweets(tweets):
        return {"n_tweets": len(tweets)}

* The function takes a single argument, which is a list of the user's tweets
* The function returns a dict of attributes and values
* The function begins with ``attr_`` - this is required for attributes that
    will be harvested using ``SummaryBuilder.read_attrs_from_module``. This
    allows you to define intermediary functions in an attribute module without
    those functions being harvested.
