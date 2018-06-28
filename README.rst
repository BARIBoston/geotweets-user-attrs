geotweets-attrs
---------------

This repository contains the main script ``main.py`` for generating summary
files from user files from the geotweets database. ``main.py`` pulls attribute
functions from ``attrs.py`` and optionally any other file that you wish
to include.

Some performance sacrifices were made to maximize maintainability, i.e. in the
case of finding the most frequent values from a user's tweets. **TODO**:
address this issue

**TODO**
* Multiprocessing
* Return multiple values from attribute functions
* Maybe cluster computing with Celery

usage
-----

.. code-block:: sh

    ./main.py [list of user files]

Where *list of user files* is a list of gzip-compressed files, with each line
being the JSON of a single tweet by a user.

For programmatic usage:

.. code-block:: python

    import main

    s = main.SummaryBuilder()

    for user in list_of_user_files:
        s.process_user(user)

    df = s.to_df()      # for a Pandas DataFrame
    s.to_csv("out.csv") # to write to disk



adding attributes
-----------------

Additional attributes can be defined by attribute functions, which calculate
a single value. **TODO**: Allow attribute functions to return multiple values

Attribute functions can be specified with ``SummaryBuilder.add_attr_function``,
in which case you must supply the name of the attribute and the function used
to calculate it, or they can be automatically harvested from a module with
``SummaryBuilder.read_attrs_from_module``.

Attribute functions have the following form:

.. code-block:: python

    def attr_n_tweets(tweets):
        return len(tweets)

* The function takes a single argument, which is a list of the user's tweets
* The function returns a single value
* The function begins with ``attr_`` - **this is required for attributes that
    will be harvested using ``SummaryBuilder.read_attrs_from_module``**. This
    allows you to define intermediary functions in an attribute module without
    those functions being harvested. The name of the attribute is calculated
    by stripping ``attr_`` from the function name.
