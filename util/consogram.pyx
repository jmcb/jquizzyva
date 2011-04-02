#!/usr/bin/env python
"""
An implementation of "consograms": this converts alphagrams into "consograms",
similar to an alphagram but placing alphabetically ordered consonants first,
followed by alphabetically ordered vowels.
"""

cpdef object consogram (char* word):
    cdef char[7] consonants
    cdef char[7] vowels
    cdef num_consonants = 0
    cdef num_vowels = 0
    cdef int wordlen = len(word)

    cdef char cur_char
    cdef int let

    for let from 0 <= let < wordlen:
        cur_char = word[let]

        if cur_char == 'A' or cur_char == 'E' or cur_char == 'I' or cur_char == 'O' or cur_char == 'U':
            vowels[num_vowels] = cur_char
            num_vowels += 1
        else:
            consonants[num_consonants] = cur_char
            num_consonants += 1

    return consonants[:num_consonants] + "+" + vowels[:num_vowels]
