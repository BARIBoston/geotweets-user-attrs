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

def attr_user_id(tweets):
    id_ = next(iter(tweets))["user"]["id"]

    # MongoDB uses $numberLong to represent long integers
    if (type(id_) is dict):
        return int(id_["$numberLong"])

    else:
        return id_

def attr_n_tweets(tweets):
    return len(tweets)

def attr_most_frequent_name(tweets):
    counts = collections.defaultdict(int)
    for tweet in tweets:
        counts[tweet["user"]["name"]] += 1
    return _most_frequent(counts)
