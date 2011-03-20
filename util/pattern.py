#!/usr/bin/env python

import re

SET_FINDER = re.compile("\[([A-Z]+)\]")

MAX_WORD_LENGTH = 16

class Pattern (object):
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

        super(Pattern, self).__init__()

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
        return len(self.letters) + len(self.sets) + self.blanks

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

        pattern = pattern.replace("?", "").replace("*", "")

        sets = SET_FINDER.findall(pattern)

        for set in sets:
            pattern = pattern.replace("[%s]" % set, "")
            self.sets.append(list(set))

        self.letters = list(pattern)

        self.length = self.calc_length()

        return self

    @classmethod
    def fromvalues (cls, pattern, blanks, wildcard, sets, letters, subanagram):
        """
        Create a new pattern based on pre-parsed values.

        :param pattern: The original pattern.
        :param blanks: The number of 'blank' placeholders.
        :param wildcard: Whether or not a wildcard is found within the pattern.
        :param sets: A list containing character sets.
        :param letters: A list containing required letters.
        :param subanagram: See the subanagram paramter of the Pattern __init__
            function.
        """

        self = cls()

        self.pattern = pattern
        self.blanks = blanks
        self.wildcard = wildcard
        self.sets = [cset[:] for cset in sets]
        self.letters = letters[:]
        self.subanagram = subanagram

        self.length = self.calc_length()

        return self

    @classmethod
    def frompattern (cls, pattern):
        """
        Create a new pattern from another pattern.
        """

        return pattern.clone()

    def clone (self):
        """
        Create a new pattern using the values of the current pattern.
        """

        return self.fromvalues(self.pattern, self.blanks, self.wildcard, self.sets, self.letters, self.subanagram)

    def try_letter (self, letter):
        """
        Determine if a letter is acceptable within the current bounds of the
        Pattern.

        :param letter: The letter to test.
        """

        assert len(letter) == 1

        letter = letter.upper()

        try:
            index = self.letters.index(letter)
        except ValueError:
            index = -1

        if index > -1:
            self.letters.pop(index)
            return True

        set_index = -1

        if self.sets:
            for cind, cset in enumerate(self.sets):
                try:
                    cset.index(letter)
                except ValueError:
                    continue
                else:
                    set_index = cind
                    break

        if set_index > -1:
            self.sets.pop(set_index)
            return True

        if self.blanks > 0:
            self.blanks -= 1
            return True

        if self.wildcard:
            return True

        return False

    def try_word (self, word):
        """
        Statefully determine if a word matches the current pattern; this method
        clones the current pattern object and performs a letter-by-letter
        comparison.

        :param word: The word to be checked against the current pattern.
        """

        clone = self.clone()

        word = word.upper()

        wordlen = len(word)

        if wordlen > len(clone):
            return False

        if wordlen < clone.length and not self.subanagram:
            return False

        for letter in word:
            if not clone.try_letter(letter):
                return False

        if clone.calc_length() > 0 and not self.subanagram:
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

class SubPattern (Pattern):
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

        super(SubPattern, self).__init__(subanagram=True)
