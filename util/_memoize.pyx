#!/usr/bin/env python

cdef class Memoizer (object):
    cdef object function
    cdef dict hash
    cdef object __name__
    cdef object __doc__

    def __init__ (Memoizer self, object function):
        self.hash = {}

        self.function = function

        self.__name__ = function.__name__
        self.__doc__ = function.__doc__

    def __get__ (Memoizer self, object obj, object objtype):
        def partial (object function, char* word):
            return function(obj, word)

        return partial

    def __call__ (Memoizer self, char* word):
        cdef bint result

        try:
            return self.hash[word]
        except KeyError:
            result = self.function(word)
            self.hash[word] = result
            return result
