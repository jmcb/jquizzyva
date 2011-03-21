#!/usr/bin/env python

cpdef bint try_word (object pattern, char* word):
    cdef int blanks = pattern.blanks
    cdef int length = pattern.length
    cdef int wordlen = len(word)
    cdef list letters = pattern.letters[:]
    cdef list sets = pattern.sets[:]
    cdef list nsets = pattern.neg_sets[:]
    cdef bint subanagram = pattern.subanagram
    cdef bint wildcard = pattern.wildcard

    cdef int nset_count = 0
    cdef int set_count = 0

    cdef int got_set = -1
    cdef int got_nset = -1

    if not wildcard and wordlen > length:
        return 0

    if wordlen < length and not subanagram:
        return 0

    cdef int let = 0

    for let from 0 <= let < wordlen:
        letter = chr(let)

        if letter in letters:
            del letters[letters.index(letter)]
            continue

        got_nset = -1

        nset_count = len(nsets)

        for nind from 0 <= nind < nset_count:
            nset = nsets[nind]

            if letter in nset:
                return 0
            else:
                got_nset = nind
                break

        if got_nset > -1:
            del nsets[got_nset]
            continue

        got_set = -1

        set_count = len(sets)

        for cind from 0 <= cind < set_count:
            cset = sets[cind]

            if letter in cset:
                got_set = cind
                break
            else:
                continue

        if got_set > -1:
            del sets[got_set]
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
