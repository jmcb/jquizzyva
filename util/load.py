#!/usr/bin/env python

import os

import lxml.etree
import lxml.cssselect

import util.search

class UnsupportedSearchType (Exception):
    pass

class UnsupportedSearchArgument (Exception):
    pass

SEARCH_TYPES = {
    "Pattern Match": util.search.PatternMatch,
    "Anagram Match": util.search.AnagramMatch,
    "Subanagram Match": util.search.SubanagramMatch,
    "Length": util.search.Length,
    "Exact Length": util.search.Length,
    "Takes Prefix": util.search.TakesPrefix,
    "Takes Suffix": util.search.TakesSuffix,
    "Includes Letters": util.search.IncludesLetters,
    "Must Include": util.search.IncludesLetters,
    "Consists of": util.search.ConsistsOf,
    "Belongs to Group": util.search.BelongsToGroup,
    "In Word List": util.search.InWordList,
    "Number of Vowels": util.search.NumberOfVowels,
    "Number of Anagrams": util.search.NumberOfAnagrams,
    "Number of Unique Letters": util.search.NumberOfUniqueLetters,
    "Point Value": util.search.PointValue
}

class SearchValue (object):
    def __init__ (self, attribute, type, default=None):
        self.attribute = attribute
        self.type = type
        self.default = default

    def value (self, mvalue=None):
        if mvalue is None:
            mvalue = self.default

        try:
            return {self.attribute: self.type(mvalue)}
        except:
            return {self.attribute: mvalue}

SEARCH_VALUES = {
    "string": SearchValue("search_string", str),
    "min": SearchValue("search_range_start", int),
    "max": SearchValue("search_range_stop", int),
    "bool": SearchValue("negated", bool, False),
    "int": SearchValue("search_range_start", int),
    "number": SearchValue("search_range_start", int),
}

def parse_condition (condition):
    args = {}

    condition = dict(condition.items())

    type = condition.pop("type")

    if not SEARCH_TYPES.has_key(type):
        raise UnsupportedSearchType(type)

    type = SEARCH_TYPES[type]

    for key, value in condition.iteritems():
        if not SEARCH_VALUES.has_key(key):
            raise UnsupportedSearchArgument(key)

        args.update(SEARCH_VALUES[key].value(value))

    return type(**args)

def parse_search (document_text):
    try:
        document_text = document_text.read()
    except:
        if os.path.exists(document_text):
            document_text = open(document_text).read()

    document = lxml.etree.fromstring(document_text)

    conditions = lxml.cssselect.CSSSelector("and > condition")(document)

    search_list = util.search.SearchList()

    for condition in conditions:
        search_list.append(parse_condition(condition))

    return search_list
