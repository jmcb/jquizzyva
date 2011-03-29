#!/usr/bin/env python

import json
import sqlite3

import util.pattern

CALLBACK_FUNCTION = "callback"

class SearchError (Exception):
    """
    This error is raised whenever a search fails.
    """
    pass

def alphagram (string):
    """
    This converts a string into an 'alphagram': an alphabetically sorted string.
    """
    return "".join(sorted(list(string.upper())))

class SearchType (object):
    """
    This is the basic search type object from which all of our search types
    derive. Primarily they provide a way of automatically generating SQL WHERE
    clauses for searching, but in a secondary manner provide limiting and
    filtering of results.
    """

    negated = False

    def __init__ (self, negated=False):
        """
        Create a new search type. This provides access for negation of search
        terms on a general basis, but otherwise all search terms created should
        be derivatives of this class; it should never be insantiated directly.

        :param negated: If True, the search term will be negated. Default False.
        """

        super(SearchType, self).__init__()

        self.negated = negated

    def negate (self):
        """
        Manually mark the search term as being negated.
        """

        self.negated = True

    def clause (self):
        """
        Generate a clause or series of clauses to be appended to an SQL
        statement. It returns False to denote that there is no clause for this
        constraint.
        """

        return False

    def limit (result):
        """
        Limit returned results by filtering them according to some specific
        pattern. It is expected that the limiting will be in-place, and that
        the new "limited" result list will be returned by this function.

        :param result: This consists of the list of results from the database;
            note that this result list may have already been limited by a
            previous query.
        """

        return result

    def __repr__ (self):
        return str(self.__class__)

    def asdict (self):
        result = {"search_type": self.__class__.__name__, "negated": self.negated}

        for key, value in self.__dict__.iteritems():
            if key.startswith("search"):
                result[key] = value

        return result

    def asjson (self):
        return json.dumps(self.asdict())

    @classmethod
    def fromdict (cls, ddict):
        ddict = dict(ddict)
        st = ddict.pop("search_type")

        if not st == cls.__class__.__name__:
            cls = globals()[st]

        return cls(**ddict)

    @classmethod
    def fromjson (cls, jsond):
        return cls.fromdict(json.loads(jsond))

class StringSearch (SearchType):
    """
    This is another base-type for string-based searches, and should not be
    instantiated directly.
    """

    search_string = None

    def __init__ (self, search_string="", *args, **kwargs):
        """
        Create a new string-based search.

        :param search_string: This string is the parameter that is stored and
            is then used when generating WHERE clauses.
        """
        super(StringSearch, self).__init__(*args, **kwargs)

        self.search_string = search_string

    def __repr__ (self):
        return "<%s search_string:%s>" % (self.__class__.__name__, self.search_string)

try:
    from util._search import AnagramMatchBase, SubanagramMatchBase, PatternMatchBase
except:
    class PatternMatch (StringSearch):
        """
        A derivative of StringSearch, this search applies a pattern specifically to
        the database.
        """

        column = "words.word"

        def clause (self):
            if "[" in self.search_string:
                return CALLBACK_FUNCTION

            st = self.search_string.replace("?", ".").replace("*", ".*")

            if self.negated:
                return ("%s LIKE ?" % self.column, (st, ))
            else:
                return ("%s NOT LIKE ?" % self.column, (st, ))

        def pattern (self):
            if self.patternobj is None:
                self.patternobj = util.pattern.Pattern.fromstring(self.search_string).as_regexp()

            def search_function (word):
                return bool(self.patternobj.match(word))

            return search_function

        def bounds (self):
            return self.patternobj.bounds()

    class AnagramMatch (StringSearch):
        """
        A derivative of StringSearch, this search looks for anagrams of the string
        provided.
        """

        patternobj = None
        column = "words.alphagram"

        def clause (self):
            if "?" in self.search_string or "[" in self.search_string or "*" in self.search_string:
                return CALLBACK_FUNCTION

            ag = alphagram(self.search_string)

            return ("words.alphagram=?", (ag, ))

        def pattern (self):
            if self.patternobj is None:
                self.patternobj = util.pattern.AnagramPattern.fromstring(self.search_string)

            def search_function (word):
                return self.patternobj.try_word(word)

            return search_function

        def bounds (self):
            return self.patternobj.bounds()

    class SubanagramMatch (AnagramMatch):
        """
        A derivative of StringSearch, this search, like AnagramMatch, searches for
        anagrams of the string provided. However, it will search for anagrams of
        any length, of any combination of the contained string.
        """

        def clause (self):
            return CALLBACK_FUNCTION

        def pattern (self):
            if self.patternobj is None:
                self.patternobj = util.pattern.SubAnagramPattern.fromstring(self.search_string)

            def search_function (word):
                return self.patternobj.try_word(word)

            return search_function
else:
    class _SimplePatternMatch (StringSearch):
        column = "words.word"

        def clause (self):
            st = self.search_string.replace("?", ".").replace("*", ".*")

            if self.negated:
                return ("%s LIKE ?" % self.column, (st, ))
            else:
                return ("%s NOT LIKE ?" % self.column, (st, ))

        def asdict (self):
            return {"search_type": "PatternMatch", "search_string": self.search_string, "negated": self.negated}

    class _PatternMatch (PatternMatchBase, StringSearch):
        column = "words.word"

        def asdict (self):
            return {"search_type": "PatternMatch", "search_string": self.search_string, "negated": self.negated}

        @classmethod
        def fromdict (cls, my_dict):
            my_dict = dict(my_dict)
            my_dict.pop("search_type")
            return cls(**my_dict)

        def asjson (self):
            return json.dumps(self.as_dict())

        @classmethod
        def fromjson (cls, data):
            return cls.fromdict(json.loads(data))

    def PatternMatch (search_string, negated=False):
        if "[" in search_string:
            return _PatternMatch(search_string=search_string, negated=negated)
        else:
            return _SimplePatternMatch(search_string=search_string, negated=negated)

    class _AlphagramMatch (StringSearch):
        column = "words.alphagram"

        def clause (self):

            ag = alphagram(self.search_string)

            return ("words.alphagram=?", (ag, ))

        def asdict (self):
            return {"search_type": "AnagramMatch", "search_string": self.search_string, "negated": self.negated}

    class _AnagramMatch (AnagramMatchBase, StringSearch):
        column = "words.alphagram"

        def asdict (self):
            return {"search_type": "AnagramMatch", "search_string": self.search_string, "negated": self.negated}

        @classmethod
        def fromdict (cls, my_dict):
            my_dict = dict(my_dict)
            my_dict.pop("search_type")
            return cls(**my_dict)

        def asjson (self):
            return json.dumps(self.as_dict())

        @classmethod
        def fromjson (cls, data):
            return cls.fromdict(json.loads(data))

    def AnagramMatch (search_string, negated=False):
        if "?" in search_string or "[" in search_string or "*" in search_string:
            return _AnagramMatch(search_string=search_string, negated=negated)
        else:
            return _AlphagramMatch(search_string=search_string, negated=negated)

    class SubanagramMatch (SubanagramMatchBase, StringSearch):
        column = "words.alphagram"

        def as_dict (self):
            return {"search_type": "SubanagramMatch", "search_string": self.search_string, "negated": self.negated}

        @classmethod
        def from_dict (cls, my_dict):
            my_dict = dict(my_dict)
            my_dict.pop("search_type")
            return cls(**my_dict)

        def as_json (self):
            return json.dumps(self.as_dict())

        @classmethod
        def from_json (cls, data):
            return cls.from_dict(json.loads(data))

class TakesPrefix (StringSearch):
    """
    This is a limiting search that ensures that the words returned are only
    words which take a specific prefix.
    """
    column = "words.word"

    def clause (self):
        return ("?||words.word IN (SELECT word AS pos_word FROM words WHERE pos_word=?||MYWORD)", (self.search_string, self.search_string))

class TakesSuffix (StringSearch):
    """
    As per TakesPrefix, only apply to words which take a specific suffix
    instead.
    """
    column = "words.word"

    def clause (self):
        return ("words.word||? IN (SELECT word AS pos_word FROM words WHERE pos_word=MYWORD||?)", (self.search_string, self.search_string))

class RangeSearch (SearchType):
    """
    This search specifies integer "start" and "stop" values, and limits results
    to those whose specific column value falls between these two values; if the
    "start" and "stop" parameters are the same, or the stop value is less than
    the start value, only results whose column value matches the "start" value
    will be returned.
    """

    search_range_start = 0
    search_range_stop = 0

    def __init__ (self, search_range_start=0, search_range_stop=0, *args, **kwargs):
        """
        Create a new RangeSearch.

        :param search_range_start: The starting range limiter.
        :param search_range_stop: The stopping range limiter.
        """

        super(RangeSearch, self).__init__(*args, **kwargs)

        try:
            self.search_range_start = int(search_range_start)
        except ValueError:
            raise SearchError("%s is invalid start" % search_range_start)

        try:
            self.search_range_stop = int(search_range_stop)
        except ValueError:
            raise SearchError("%s is invalid stop" % search_range_stop)

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
    """
    This search limits results to words of a specific length -- either within a
    range or or a certain value.
    """
    column = "words.length"

class NumberOfVowels (RangeSearch):
    """
    This search limits results to words which contain either a specific number
    of vowels, or a number of vowels that falls between a specified range.
    """
    column = "words.num_vowels"

class NumberOfUniqueLetters (RangeSearch):
    """
    This search limits results to words which container either a specific
    number of unique letters, or whose number of unique letters falls between a
    specified range.
    """
    column = "words.num_unique_letters"

class PointValue (RangeSearch):
    """
    This search limits results to words who have either a specific 'point'
    value, or whose 'point' value falls between a specified range.
    """
    column = "words.point_value"

class NumberOfAnagrams (RangeSearch):
    """
    This search limits results to words who either have a specific number of
    anagrams possible, or whose number of possible anagrams falls between a
    specified range.
    """
    column = "words.num_anagrams"

class ConsistsOf (StringSearch, RangeSearch):
    def __repr__ (self):
        return "<%s search_range_start:%s, search_range_stop:%s, search_string:%s>" % (self.__class__.__name__, self.search_range_start, self.search_range_stop, self.search_string)

class StringListSearch (SearchType):
    search_string_list = None

    def __init__ (self, search_string_list=None, search_string=None, *args, **kwargs):
        super(StringListSearch, self).__init__(*args, **kwargs)

        self.search_string_list = search_string_list

        if self.search_string_list is None:
            self.search_string_list = []

        if search_string is not None:
            self.search_string_list.extend(search_string)

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
            return False

class SearchList (object):
    searches = None

    def __init__ (self, *searches):
        super(SearchList, self).__init__()

        self.searches = []

        if searches:
            self.searches.extend(searches)

    def append (self, item):
        self.searches.append(item)

    def query (self):
        args = []
        functions = {}
        query = "SELECT alphagram, front_hooks, word as MYWORD, back_hooks, definition FROM words WHERE "

        maybe_query = None

        for constraint in self.searches:
            try:
                squery, subargs = constraint.clause()
            except ValueError:
                ind = len(functions)+1
                squery = "anagrammer%s(%s)" % (ind, constraint.column)
                subargs = []
                functions["anagrammer%s" % ind] = constraint.pattern()
                bounds = constraint.bounds()
                if (maybe_query and int(maybe_query[-1]) < int(bounds[-1])) or not maybe_query:
                    maybe_query = bounds

            if not query.endswith("WHERE "):
                query += " AND "

            query += squery

            args.extend(subargs)

        if "words.length" not in query and maybe_query:
            query += " AND " + maybe_query

        query += " LIMIT 100"

        return (query, args, functions)

    def __repr__ (self):
        return "<SearchList %s>" % self.searches

    def asdicts (self):
        return [item.asdict() for item in self.searches]

    def asjson (self):
        return json.dumps(self.asdicts())

    @classmethod
    def fromdicts (cls, items):
        try:
            return cls(*[SearchType.fromdict(item) for item in items])
        except:
            return cls(SearchType.fromdict(items))

    @classmethod
    def fromjson (cls, jsond):
        return cls.fromdicts(json.loads(jsond))
