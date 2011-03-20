#!/usr/bin/env python

import unittest

import util.search, util.db

class TestZ___Anagram (unittest.TestCase):

    def setUp (self):
        with open("test/z___.txt") as f:
            self.acceptable = set([line.strip() for line in f])

        self.search = util.search.AnagramMatch("Z[AEIOU][AEIOU]?")
        self.db = util.db.csw()

    def test_search (self):
        results = self.db.search(self.search)

        for result in results:
            word = result["word"]
            self.assertIn(word, self.acceptable)

class TestZ___SubAnagram (unittest.TestCase):

    def setUp (self):
        with open("test/sub_z___.txt") as f:
            self.acceptable = set([line.strip() for line in f])

        self.search = util.search.SubanagramMatch("Z[AEIOU][AEIOU]?")
        self.db = util.db.csw()

    def test_search (self):
        results = self.db.search(self.search)

        for result in results:
            word = result["word"]
            self.assertIn(word, self.acceptable)
