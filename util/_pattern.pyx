#!/usr/bin/env python

#def try_word (object pattern, char* word):
#    return _try_word(pattern, word)

cdef class CPattern (object):
    cdef int blanks
    cdef int length
    cdef int num_letters
    cdef int num_sets
    cdef int num_neg_sets
    cdef bint subanagram
    cdef bint wildcard
    cdef char* chr_letters
    cdef list sets
    cdef list neg_sets
    cdef list letters

    def __init__ (CPattern self, int blanks, int length, int num_letters, char* chr_letters, list letters, int num_sets, list sets, int num_neg_sets, list neg_sets, bint subanagram, bint wildcard):
        self.blanks = blanks
        self.length = length
        self.num_letters = num_letters
        self.num_sets = num_sets
        self.num_neg_sets = num_neg_sets
        self.subanagram = subanagram
        self.wildcard = wildcard
        self.chr_letters = chr_letters
        self.sets = sets
        self.neg_sets = neg_sets
        self.letters = letters

def try_word (CPattern pattern, char* word):
    return _try_word(pattern, word)

cdef int _try_word (CPattern pattern, char* word):
    cdef int blanks = pattern.blanks
    cdef int length = pattern.length
    cdef int wordlen = len(word)
    cdef int num_sets = pattern.num_sets
    cdef int num_neg_sets = pattern.num_neg_sets
    cdef int letterslen = pattern.num_letters
    cdef char* cletters = pattern.chr_letters

    cdef list letters = pattern.letters[:]
    cdef list sets = pattern.sets[:]
    cdef list nsets = pattern.neg_sets[:]

    cdef bint subanagram = pattern.subanagram
    cdef bint wildcard = pattern.wildcard

    cdef int nset_count = 0
    cdef int set_count = 0
    cdef int let_count = 0
    cdef int got_set = -1
    cdef int got_nset = -1
    cdef int got_let = -1

    cdef int let
    cdef int let2

    cdef char letter

    if not wildcard and wordlen > length:
        return 0

    if wordlen < length and not subanagram:
        return 0

    for let from 0 <= let < wordlen:
        letter = word[let]

        if letter in cletters:
            if letter in letters:
                index = letters.index(letter)
                del letters[index]
                continue

        got_nset = -1

        for nind from 0 <= nind < num_neg_sets:
            nset = nsets[nind]

            if letter in nset:
                return 0
            else:
                got_nset = nind
                break

        if got_nset > -1:
            del nsets[got_nset]
            num_neg_sets -= 1
            continue

        got_set = -1

        for cind from 0 <= cind < num_sets:
            cset = sets[cind]

            if letter in cset:
                got_set = cind
                break
            else:
                continue

        if got_set > -1:
            del sets[got_set]
            num_sets -= 1
            continue

        if blanks > 0:
            blanks -= 1
            continue

        if wildcard:
            continue

        return 0

    if letters and sets and blanks and not subanagram:
        return 0

    return 1
