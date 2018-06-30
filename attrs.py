#!/usr/bin/env python3

""" This module contains example attribute functions for use in calculating
attributes from Twitter users in the geotweets database. """

import collections

def _most_frequent(dict_):
    most_frequent_key = None
    most_frequent_count = 0
    for (key, count) in dict_.items():
        if (count > most_frequent_count):
            most_frequent_count = count
            most_frequent_key = key
    return key

def _recursive_getitem(obj, keys):
    next_keys = keys[1:]
    next_obj = obj[keys[0]]
    if (len(next_keys) == 0):
        return next_obj
    else:
        return _recursive_getitem(next_obj, next_keys)

def attr_user_id(tweets):
    """ Find the user ID """

    id_ = next(iter(tweets))["user"]["id"]

    # MongoDB uses $numberLong to represent long integers
    if (type(id_) is dict):
        id_ = int(id_["$numberLong"])

    return {"user_id": id_}

def attr_n_tweets(tweets):
    """ Count the number of tweets """

    return {"n_tweets": len(tweets)}

def setup_most_frequent(attrs):
    """ Set up a function to find the most frequent attributes

    Example usage:
    find_most_common = setup_most_frequent({
        "name": ["user", "name"],
        "username": ["user", "screen_name"],
    })

    :param dict attrs: A dict of attributes to track where the keys are the
        names of the attributes and the values are a list of keys to be
        fetched, in the order that they should be fetched
    :returns: An attribute extractor
    :rtype: functio
    """

    def attrs_most_frequent(tweets):
        """ Find the most frequently occurring values of an attribute """

        counts = {
            attr: collections.defaultdict(int)
            for attr in attrs.keys()
        }

        for tweet in tweets:
            for (attr, keys) in attrs.items():
                counts[attr][_recursive_getitem(tweet, keys)] += 1

        return {
            attr: _most_frequent(counts[attr])
            for attr in attrs.keys()
        }

    return attrs_most_frequent
