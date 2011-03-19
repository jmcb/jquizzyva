#!/usr/bin/env python

import sqlite3

class SearchType (object):
    negated = False

    def __init__ (self, negated=False):
        super(SearchType, self).__init__()

        self.negated = negated
        
    def clause (self):
        return ("", ())

    def __repr__ (self):
        return str(self.__class__)

class StringSearch (SearchType):
    search_string = None

    def __init__ (self, search_string="", *args, **kwargs):
        super(StringSearch, self).__init__(*args, **kwargs)

        self.search_string = search_string

    def __repr__ (self):
        return "<%s search_string:%s>" % (self.__class__.__name__, self.search_string)

class PatternMatch (StringSearch):
    column = "words.word"

    def clause (self):
        st = self.search_string.replace("?", "_").replace("*", "%")

        if self.negated:
            return ("%s LIKE ?" % self.column, (st, ))
        else:
            return ("%s NOT LIKE ?" % self.column, (st, ))

class AnagramMatch (StringSearch):
    pass # string

class SubanagramMatch (StringSearch):
    pass # string

class TakesPrefix (StringSearch):
    pass # string

class TakesSuffix (StringSearch):
    pass # string

class RangeSearch (SearchType):
    search_range_start = 0
    search_range_stop = 0

    def __init__ (self, search_range_start=0, search_range_stop=0, *args, **kwargs):
        super(RangeSearch, self).__init__(*args, **kwargs)

        self.search_range_start = search_range_start
        self.search_range_stop = search_range_stop

    def clause (self):
        rt = self.search_range_start
        rp = self.search_range_stop

        if rt == rp or rp < rt:
            return ("%s=?" % self.column, (rt, ))
        else:
            return ("%s >= ? AND %s <= ?" % (self.column, self.column), (rt, rp))

    def __repr__ (self):
        return "<%s search_range_start:%s, search_range_stop:%s>" % (self.__class__.__name__, self.search_range_start, self.search_range_stop)

class Length (RangeSearch):
    column = "words.length"

class NumberOfVowels (RangeSearch):
    column = "words.num_vowels"

class NumberOfUniqueLetters (RangeSearch):
    column = "words.num_unique_letters"

class PointValue (RangeSearch):
    column = "words.point_value"

class NumberOfAnagrams (RangeSearch):
    column = "words.num_anagrams"

class AbilitySearch (RangeSearch):
    pass

class ProbabilityOrder (AbilitySearch):
    pass

class LimitByProbabilityOrder (AbilitySearch):
    pass # int, int

class PlayabilityOrder (AbilitySearch):
    pass # int, int

class LimitByPlayabilityOrder (AbilitySearch):
    pass # int, int

class ConsistsOf (StringSearch, RangeSearch):
    def __repr__ (self):
        return "<%s search_range_start:%s, search_range_stop:%s, search_string:%s>" % (self.__class__.__name__, self.search_range_start, self.search_range_stop, self.search_string)

class StringListSearch (SearchType):
    search_string_list = None

    def __init__ (self, search_string_list=None, *args, **kwargs):
        super(StringListSearch, self).__init__(*args, **kwargs)

        self.search_string_list = search_string_list

    def __repr__ (self):
        return "<%s search_string_list:%s>" % (self.__class__.__name__, self.search_string_list)

class IncludesLetters (StringListSearch):
    column = "words.word"

    def clause (self):
        args = []
        query = ""

        if self.negated:
            like = "NOT LIKE"
        else:
            like = "LIKE"

        for character in self.search_string_list:
            query += "%s %s ?" % (self.column, like)
            args.append("%"+character+"%")

        return (query, tuple(args))

class InWordList (StringListSearch):
    column = "words.word"

    def clause (self):
        args = []
        query = ""

        if self.negated:
            query = "%s NOT IN (" % self.column
        else:
            query = "%s IN (" % self.column

        for word in self.search_string_list:
            query += "?, "
            args.append(word)

        query = query.rstrip(", ") + ")"

        return (query, tuple(args))


class BelongsToGroup (SearchType):
    column = "words.word"

    def __init__ (self, search_term_string, *args, **kwargs):
        super(BelongsToGroup, self).__init__(*args, **kwargs)

        self.search_string_list = ["Hook Words", "Front Hooks", "Back Hooks",
            "High Fives", "Type I Sevens", "Type II Sevens", "Type III Sevens",
            "Type I Eights", "Type II Eights", "Type III Eights",
            "Eights From Seven-Letter Stems"]

        assert search_term_string in self.search_string_list

        self.search_term_string = search_term_string

    def clause (self):
        args = []
        query = ""

        st = self.search_term_string

        if "Hook" in st:
            if self.negated:
                m = "0"
            else:
                m = "1"

            if "Front" in st:
                query += "words.is_front_hook=?"
                args.append(m)
            elif "Back" in st:
                query += "words.is_back_hook=?"
                args.append(m)
            elif "Words" in st:
                query += "words.is_front_hook=? AND words.is_back_hook=?"
                args.extend((m, m))

            return (query, tuple(args))
        else:
            return ("", (, ))
