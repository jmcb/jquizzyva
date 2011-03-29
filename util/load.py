#!/usr/bin/env python

import lxml

import util.search

SEARCH_TYPES = {
    "Pattern Match": util.search.PatternMatch,
    "Anagram Match": util.search.AnagramMatch,
    "Subanagram Match": util.search.SubanagramMatch,
    "Length": util.search.Length,
    "Takes Prefix": util.search.TakesPrefix,
    "Takes Suffix": util.search.TakesSuffix,
    "Includes Letters": util.search.IncludesLetters,
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

SEARCH_VALUE_LOOKS = {
    "string": SearchValue("search_term_string", str),
    "min": SearchValue("search_range_start", int),
    "max": SearchValue("search_range_stop", int),
    "bool": SearchValue("negated", bool, False),
    "int": SearchValue("search_range_start", int),
    "number": SearchValue("search_range_start", int),
}
