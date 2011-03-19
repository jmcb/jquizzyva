#!/usr/bin/env python

import os
import sqlite3

import config

class DatabaseNotFoundError (Exception):
    """
    This exception is raised when we attempt to connect to a database, but we
    cannot do so because the database in question does not exist.
    """
    pass

class Database (object):
    db = None
    connection = None
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
        if not self.connection:
            self.connection = sqlite3.connect(self.db)
            self.connection.row_factory = sqlite3.Row

    def query (term, arguments=()):
        """
        This executes a query, fetches all results, and returns a tuple
        consisting of: (result, rowcount, lastrowid, description).

        :param term: This term consists of the entire text of the query. It is
            presumed that the number of tokens contained ('?' symbols) is
            equivalent to the number of arguments passed in.
        :param arguments: This is a tuple consisting of arguments that match
            the number of tokens contained within the query.
        """
        with self.connection:
            cursor = self.cursor.execute(term, arguments)

        self.queries.append((term, arguments))
        self.last_query = (term, arguments)

        return (cursor.fetchall(), cursor.rowcount, cursor.lastrowid, cursor.description)

def csw ():
    return Database(config.LEXICONS["CSW"])
