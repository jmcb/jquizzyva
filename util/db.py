#!/usr/bin/env python

import itertools
import os
import sqlite3

import util.config
import util.memoize

try:
    import util._pattern
except ImportError:
    DO_MEMOIZE = True
else:
    DO_MEMOIZE = False

class DatabaseNotFoundError (Exception):
    """
    This exception is raised when we attempt to connect to a database, but we
    cannot do so because the database in question does not exist.
    """
    pass

class Database (object):
    db = None
    _connection = None
    last_query = None
    queries = None

    def __init__ (self, lexicon):
        if not os.path.exists(lexicon):
            raise DatabaseNotFoundError, lexicon

        self.db = lexicon

        self.queries = []

    def connect (self):
        """
        If not already connected, connect to the database.
        """
        if not self._connection:
            self._connection = sqlite3.connect(self.db)

        return self._connection

    def query (self, term, arguments=()):
        """
        This executes a query, fetches all results, and returns a list if
        dictionaries consisting of the result.

        :param term: This term consists of the entire text of the query. It is
            presumed that the number of tokens contained ('?' symbols) is
            equivalent to the number of arguments passed in.
        :param arguments: This is a tuple consisting of arguments that match
            the number of tokens contained within the query.
        """
        if not self.connection:
            self.connect()

        with self.connection:
            cursor = self.connection.execute(term, arguments)

        self.queries.append((term, arguments))
        self.last_query = (term, arguments)

        return cursor.fetchall()

    def register (self, function_name, function):
        self.connection.create_function(function_name, 1, function)

    def search (self, searchlist, show_query=False):
        try:
            query, args, functions = searchlist.query()
        except AttributeError:
            searchlist = util.search.SearchList(searchlist)
            query, args, functions = searchlist.query()

        if functions:
            for fname, (fn, pat) in functions.items():
                if DO_MEMOIZE:
                    self.register(fname, util.memoize.Memoizer(fn, pat))
                else:
                    self.register(fname, fn)

        if show_query:
            print query.replace("?", "%s") % tuple(args)

        result = self.query(query, tuple(args))

        used_blanks = [''] * len(result)

        if functions:
            for fname, (fn, pat) in functions.items():
                if hasattr(pat, "cpattern") and pat.cpattern:
                    bs = pat.cpattern.used_blanks()
                else:
                    bs = pat.blank_store
                used_blanks = ["".join(itertools.chain(*x)) for x in zip(used_blanks, bs)]

        return [(a, ) + b for a, b in zip(used_blanks, result)]

    def challenge (self, words):
        query = "SELECT word FROM words WHERE " + " OR ".join(["word=?" for word in words])
        args = tuple(word.upper() for word in words)

        results = self.query(query, args)
        if len(results) != len(words):
            return "no"

        return "yes"

    connection = property(connect)

def csw ():
    return Database(util.config.LEXICONS["CSW"])

def cd ():
    return Database(util.config.LEXICONS["CD"])

def ods4 ():
    return Database(util.config.LEIXCONS["ODS4"])

def ods5 ():
    return Database(util.config.LEIXCONS["ODS5"])

def oswi ():
    return Database(util.config.LEXICONS["OSWI"])

def ospd4_lwl ():
    return Database(util.config.LEXICONS["OSPD4+LWL"])

def owl_lwl ():
    return Database(util.config.LEXICONS["OWL+LWL"])

def owl2_lwl ():
    return Database(util.config.LEXICONS["OWL2+LWL"])

def swl ():
    return Database(util.config.LEXICONS["SWL"])

def volost ():
    return Database(util.config.LEXICONS["Volost"])

def wwf ():
    return Database(util.config.LEXICONS["WWF"])

def zinga ():
    return Database(util.config.LEXICONS["Zinga"])

def lexicon (lex):
    if util.config.LEXICONS.has_key(lex):
        return Database(util.config.LEXICONS[lex])

    return None
