#!/usr/bin/env python3

import collections
import csv
import gzip
import ujson as json
import pandas

class SummaryBuilder(object):

    def __init__(self):
        """ Initialize SummaryBuilder object

        The SummaryBuilder object is responsible for storing summary
        information about different Twitter users and then converting this
        information into a CSV file or Pandas DataFrame on demand """

        self.attr_extractors = []
        self.results = []

    def read_attrs_from_module(self, module):
        """ Read attribute functions from a module

        :param module module: The module containing attribute functions to be
            harvested from. All attribute functions should begin with ``attr_``
            or ``attrs_`` take a list of tweets as the only argument, and
            return a dict where the keys are attribute names and the values are
            the values. See attrs.py for examples.
        """

        if (len(self.results) > 0):
            raise Exception("cannot add attributes after data has been read")

        else:
            new_extractors = [
                getattr(attrs, name)
                for name in filter(
                    lambda x: x.startswith("attr_") or x.startswith("attrs_"),
                    dir(attrs)
                )
            ]
            self.attr_extractors.extend(new_extractors)

            print("added %s new attribute extractors from %s\n=> %s" % (
                len(new_extractors), module,
                ", ".join([fn.__name__ for fn in new_extractors])
            ))

    def add_attr_function(self, function):
        """ Add a single attribute function

        :param function function: The function that is used to calculate the
            values of attributes. See read_attrs_from_module for more info.
        """

        print("added attribute extractor %s" % function.__name__)
        self.attr_extractors.append(function)

    def process_user(self, user_json_gz):
        """ Compute and store attributes for a single user

        :param str user_json_gz: A gzip-compressed file containing a user's
            tweets, in JSON format, with one tweet on each line
        """

        user_results = {}

        with gzip.open(user_json_gz) as f:
            tweets = [
                json.loads(line)
                for line in f
            ]
            for attr_extractor in self.attr_extractors:
                user_results.update(attr_extractor(tweets))

        self.results.append(user_results)

    def to_csv(self, csv_path):
        """ Convert stored attributes to a CSV file

        :param str csv_path: The path that the CSV file should be written to
        """

        columns = self.results[0].keys()
        with open(csv_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(self.results)

        print("wrote to %s" % csv_path)

    def to_df(self):
        """ Convert stored attributes to a Pandas DataFrame

        :returns: A Pandas DataFrame
        :rtype: pandas.core.frame.DataFrame
        """

        return pandas.DataFrame(self.results)

if (__name__ == "__main__"):
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

    print("")
    print(s.to_df())
    s.to_csv("temp.csv")
