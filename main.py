#!/usr/bin/env python3

import collections
import csv
import gzip
import ujson as json
import pandas

import attrs

class SummaryBuilder(object):

    def __init__(self):
        """ Initialize SummaryBuilder object

        The SummaryBuilder object is responsible for storing summary
        information about different Twitter users and then converting this
        information into a CSV file or Pandas DataFrame on demand """

        self.attrs = {}
        self.attrs_order = None
        self.results = []

        self.read_attrs_from_module(attrs)

    def read_attrs_from_module(self, module):
        """ Read attribute functions from a module

        :param module module: The module containing attribute functions to be
            harvested from. All attribute functions should begin with ``attr``,
            take a list of tweets as the only argument, and return a single
            value. See attrs.py for examples.
        """

        if (len(self.results) > 0):
            raise Exception("cannot add attributes after data has been read")

        else:
            new_attrs = {
                name.replace("attr_", ""): getattr(attrs, name)
                for name in filter(
                    lambda x: x.startswith("attr_"),
                    dir(attrs)
                )
            }
            self.attrs.update(new_attrs)
            self.attrs_order = sorted(self.attrs.keys())

            print("added %s new attrs from %s\n=> %s" % (
                len(new_attrs), module, list(new_attrs.keys())
            ))

    def add_attr_function(self, name, function):
        """ Add a single attribute function

        :param str name: The name of the attribute
        :param function function: The function that is used to calculate the
            value of the attribute. See read_attrs_from_module for more info.
        """

        self.attrs[name] = function

    def set_attr_order(self, order):
        """ Change the order of attributes in the output or select specific
        ones

        :param list order: A list of attributes, in the order that they should
            be displayed. This list should only consider attributes loaded
            by read_attrs_from_module or add_attr_function.
        """

        for attr in order:
            if (not attr in self.attrs):
                raise Exception("no function for attribute %s is defined" % attr)
        self.attrs_order = order

    def process_user(self, user_json_gz):
        """ Compute and store attributes for a single user

        :param str user_json_gz: A gzip-compressed file containing a user's
            tweets, in JSON format, with one tweet on each line
        """

        user_results = []

        with gzip.open(user_json_gz) as f:
            tweets = [
                json.loads(line)
                for line in f
            ]
            for attr in self.attrs_order:
                user_results.append(self.attrs[attr](tweets))

        self.results.append(user_results)

    def to_csv(self, csv_path):
        """ Convert stored attributes to a CSV file

        :param str csv_path: The path that the CSV file should be written to
        """

        with open(csv_path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(self.attrs_order)
            writer.writerows(self.results)

        print("wrote to %s" % csv_path)

    def to_df(self):
        """ Convert stored attributes to a Pandas DataFrame

        :returns: A Pandas DataFrame
        :rtype: pandas.core.frame.DataFrame
        """

        return pandas.DataFrame(self.results, columns = self.attrs_order)

if (__name__ == "__main__"):
    import sys
    s = SummaryBuilder()
    for user in sys.argv[1:]:
        s.process_user(user)
    print("")
    print(s.to_df())
    s.to_csv("temp.csv")
