#!/usr/bin/env python

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

select_schema = ['alphagram', 'front_hooks', 'word', 'back_hooks', 'definition']

def dict_factory (cursor, row):
    return dict(zip(select_schema, row))

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
            self._connection.row_factory = dict_factory

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
            for fname, fn in functions.items():
                if DO_MEMOIZE:
                    self.register(fname, util.memoize.Memoizer(fn))
                else:
                    self.register(fname, fn)

        if show_query:
            print query.replace("?", "%s") % args

        return self.query(query, args)

    connection = property(connect)

def csw ():
    return Database(util.config.LEXICONS["CSW"])

def lexicon (lex):
    if util.config.LEXICONS.has_key(lex):
        return Database(util.config.LEXICONS[lex])

    return None
