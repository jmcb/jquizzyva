#!/usr/bin/env python

import functools
import re

SET_FINDER = re.compile("\[(\^?:?[A-Z]+)\]")

MAX_WORD_LENGTH = 16

try:
    from util._pattern import try_word, CAnagramPattern
except ImportError:
    try_word = None
    CAnagramPattern = None

class AnagramPattern (object):
    """
    A pattern consists primarily of a series of letters, placeholders,
    wildcards and sets of characters, which represents a variety of possible
    words by way of an expression. It also provides an interface for testing
    whether or not a letter matches the current pattern: if the letter matches,
    the pattern is modified and a true value is return. Thus, letter-by-letter
    testing of words can take place. For convenience, there exists an interface
    for testing a word, which clones the object and performs a letter-by-letter
    check of the word, returning a boolean value whenever one is available. The
    length of the incoming word is also compared against the "length" of the
    pattern (which is defined by a number of variables; see calc_length), and
    if it fails to meet these initial constraints, no checking of the word is
    needed and a False value is returned.

    For the most part, outside of the cloning of the object, the interface
    would appear to be very quick: the more 'different' a word is to our
    pattern, the sooner we are likely to encounter something that doesn't
    match, and thus the sooner we'll return a False value.
    """

    pattern = None
    blanks = 0
    wildcard = False
    sets = None
    letters = None
    cpattern = None

    length = 0

    def __init__ (self, subanagram=False):
        """
        Create a new pattern. It is possible to define a subanagram by passing
        True to the subanagram parameter, but for the most part it would be
        better to use the derivative class, SubPattern, instead.

        :param subanagram: Denote that this pattern's length constraints are
            flexible. Thus, if we reach the end of a pattern and we still have
            'letters left', and this value is True, we accept the word; if we
            reach the end and this value is False, we reject the word as not
            fully meeting the pattern criteria.
        """

        super(AnagramPattern, self).__init__()

        self.sets = []
        self.letters = []

        self.subanagram = subanagram

    def __len__ (self):
        """
        Determine the "virtual" length of the pattern. If we contain wildcards,
        then the length of the is always 15 -- there is always the capacity to
        have more letters added when a wildcard is in play.
        """

        if self.wildcard:
            return MAX_WORD_LENGTH
        else:
            return self.length

    def calc_length (self):
        """
        Determine the "actual" length of the pattern, disregarding any
        wildcards that may be contained. This consists of the number of sets of
        letters, the number of "blank" placeholders, and the number of required
        letters still available.
        """
        return len(self.letters) + len(self.sets) + len(self.neg_sets) + self.blanks

    @classmethod
    def fromstring (cls, pattern, subanagram=False):
        """
        Create a new pattern based on a string.

        :param pattern: A pattern consists of any number of letters from A to
            Z, any number of placeholder ? symbols, any number of wildcard *
            symbols (though due to the nature of the pattern, only the first
            matters; multiple wildcards are redundant), and any number of sets,
            defined as a series of letters enclosed with brackets.
        :param subanagram: See the subanagram parameter of the Pattern __init__
            function.
        """
        pattern = pattern.upper()

        self = cls(subanagram=subanagram)

        self.pattern = pattern
        self.blanks = self.pattern.count("?")
        if self.pattern.count("*"):
            self.wildcard = True

        self.sets = []
        self.neg_sets = []

        pattern = pattern.replace("?", "").replace("*", "")

        for cset in SET_FINDER.findall(pattern):
            pattern = pattern.replace("[%s]" % cset, "")

            nset = None
            neg = False

            if "^" in cset:
                neg = True
                cset = cset[1:]

            if ":" in cset:
                if cset[1] == "C": # Consonants
                    nset = set("BCDFGHJKLMNPQRSTVWXYZ")
                elif cset[1] == "V": # Vowels
                    nset = set("AEIOU")
                elif cset[1] == "H": # Heavies
                    nset = set("JKZQX")
                elif cset[1] == "M": # Mediums
                    nset = set("HFVWY")
                elif cset[1] == "L": # Lights
                    nset = set("PCMB")
                elif cset[1] == "T" or cset[1] == "P": # Twos and "Pips"
                    nset = set("AEIOUDGLNRST")
            else:
                nset = set(cset)

            if neg:
                self.neg_sets.append(nset)
            else:
                self.sets.append(nset)

        self.letters = list(pattern)

        self.length = self.calc_length()

        return self

    def as_cpattern (self):
        if self.cpattern is not None:
            return self.cpattern

        if CAnagramPattern is None:
            return None

        self.cpattern = CAnagramPattern(self.blanks, self.length, len(self.letters), [ord(l) for l in self.letters], len(self.sets), [[ord(l) for l in s] for s in self.sets], len(self.neg_sets), [[ord(l) for l in s] for s in self.neg_sets], self.subanagram, self.wildcard)

        return self.cpattern

    def try_word (self, word):
        """
        Statefully determine if a word matches the current pattern; this method
        clones the current pattern object and performs a letter-by-letter
        comparison.

        :param word: The word to be checked against the current pattern.
        """
        if try_word is not None:
            return bool(try_word(self.as_cpattern(), word))

        blanks = self.blanks
        letters = self.letters[:]
        sets = self.sets[:]
        nsets = self.neg_sets[:]
        length = self.length
        subanagram = self.subanagram
        wildcard = self.wildcard

        wordlen = len(word)

        if not wildcard and wordlen > length:
            return False

        if wordlen < length and not subanagram:
            return False

        for letter in word:
            if letter in letters:
                del letters[letters.index(letter)]
                continue

            got_nset = None

            for nind, nset in enumerate(nsets):
                if letter in nset:
                    return False
                else:
                    got_nset = nind
                    continue

            if got_nset is not None:
                del nsets[got_nset]
                continue

            got_set = None

            for cind, cset in enumerate(sets):
                if letter in cset:
                    got_set = cind
                else:
                    continue

            if got_set is not None:
                del sets[got_set]
                continue

            if blanks > 0:
                blanks -= 1
                continue

            if wildcard:
                continue

            return False

        if letters and sets and blanks and not subanagram:
            return False

        return True

    def bounds (self):
        """
        Represent the bounds of this parameter as an SQLite statement.
        """

        if self.subanagram:
            return "words.length<=%s" % len(self)

        if self.length != len(self):
            return "words.length BETWEEN %s AND %s" % (self.length, len(self))
        else:
            return "words.length=%s" % len(self)

    def __repr__ (self):
        return "<%s '%s' wildcard=%s blanks=%s sets=%s letters=%s>" % (self.__class__.__name__, self.pattern, self.wildcard, self.blanks, self.sets, self.letters)

class SubAnagramPattern (AnagramPattern):
    """
    This pattern is a convenience subclass of Pattern; the usage,
    initialisation, etc, are identical to Pattern, but it automatically sets
    subanagram=True to all of these.
    """

    subanagram = True

    def __init__ (self, subanagram=True):
        """
        Create a new SubPattern. The subanagram parameter for this function is
        ignored, but exists in order to provide compatability of signatures.

        :param subanagram: Ignored.
        """

        super(SubAnagramPattern, self).__init__(subanagram=True)

class Pattern (AnagramPattern):
    """
    This is a simple parser that converts a pattern string into a regular expression.
    """
    _regexp = None

    def __init__ (self, subanagram=False):
        super(Pattern, self).__init__(subanagram=False)

    def as_regexp (self):
        if self._regexp is not None:
            return self._regexp

        pat = self.pattern.replace("?", ".").replace("*", ".*")
        if not pat.endswith("$"):
            pat = pat + "$"

        self._regexp = re.compile(pat)

        return self._regexp
